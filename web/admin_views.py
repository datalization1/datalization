"""Eigenständige Datalization-Admin (unabhängig von der Django-Admin).

Passwort-Login (settings.ADMIN_PASSWORD, aus der Umgebung) → Session. Verwaltet
Kontaktanfragen, Buchungen, Referenzen (Case Studies, voll bearbeitbar) und
generische Inhalts-Blöcke. GUI im Datalization-Design (templates/custom_admin/).
"""
import csv
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _

from .forms import CaseStudyForm, ContentBlockForm
from .models import CaseStudy, ContactMessage, ContentBlock, StartRequest


def _is_admin(request):
    return request.session.get("custom_admin") is True


def admin_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not _is_admin(request):
            return redirect("web:admin_login")
        return view(request, *args, **kwargs)
    return wrapper


# --- Auth -------------------------------------------------------------------
def admin_login(request):
    if _is_admin(request):
        return redirect("web:custom_admin")
    if request.method == "POST":
        pw = getattr(settings, "ADMIN_PASSWORD", "")
        if pw and request.POST.get("password") == pw:
            request.session["custom_admin"] = True
            return redirect("web:custom_admin")
        messages.error(request, _("Falsches Passwort."))
    return render(request, "custom_admin/login.html")


def admin_logout(request):
    request.session.pop("custom_admin", None)
    return redirect("web:admin_login")


# --- Helpers ----------------------------------------------------------------
def _export_csv(model, fields, filename):
    resp = HttpResponse(content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = f"attachment; filename={filename}.csv"
    resp.write("﻿")  # BOM für Excel
    w = csv.writer(resp, delimiter=";")
    w.writerow(fields)
    for obj in model.objects.all().order_by("-created"):
        w.writerow([getattr(obj, f) for f in fields])
    return resp


def _submission_action(request, model, redirect_name):
    action = request.POST.get("action")
    obj = get_object_or_404(model, pk=request.POST.get("id"))
    if action == "handle":
        obj.handled = True
        obj.save(update_fields=["handled"])
        messages.success(request, _("Als erledigt markiert."))
    elif action == "unhandle":
        obj.handled = False
        obj.save(update_fields=["handled"])
        messages.success(request, _("Als offen markiert."))
    elif action == "delete":
        obj.delete()
        messages.success(request, _("Gelöscht."))
    return redirect(redirect_name)


# --- Dashboard --------------------------------------------------------------
@admin_required
def admin_dashboard(request):
    return render(request, "custom_admin/dashboard.html", {
        "nav": "dashboard",
        "contacts_open": ContactMessage.objects.filter(handled=False).count(),
        "contacts_total": ContactMessage.objects.count(),
        "bookings_open": StartRequest.objects.filter(handled=False).count(),
        "bookings_total": StartRequest.objects.count(),
        "cases_published": CaseStudy.objects.filter(published=True).count(),
        "cases_total": CaseStudy.objects.count(),
        "blocks_total": ContentBlock.objects.count(),
        "recent_contacts": ContactMessage.objects.order_by("-created")[:6],
        "recent_bookings": StartRequest.objects.order_by("-created")[:6],
    })


# --- Kontaktanfragen --------------------------------------------------------
@admin_required
def admin_contacts(request):
    if request.method == "POST":
        return _submission_action(request, ContactMessage, "web:admin_contacts")
    if request.GET.get("export"):
        return _export_csv(ContactMessage,
                           ["created", "first_name", "last_name", "company", "email",
                            "phone", "service", "message", "language", "handled"],
                           "kontaktanfragen")
    return render(request, "custom_admin/contacts.html", {
        "nav": "contacts",
        "items": ContactMessage.objects.order_by("-created"),
    })


# --- Buchungen --------------------------------------------------------------
@admin_required
def admin_bookings(request):
    if request.method == "POST":
        return _submission_action(request, StartRequest, "web:admin_bookings")
    if request.GET.get("export"):
        return _export_csv(StartRequest,
                           ["created", "first_name", "last_name", "company", "email",
                            "phone", "branches", "pains", "start_mode", "notes",
                            "language", "handled"],
                           "buchungen")
    return render(request, "custom_admin/bookings.html", {
        "nav": "bookings",
        "items": StartRequest.objects.order_by("-created"),
    })


# --- Referenzen / Case Studies ----------------------------------------------
@admin_required
def admin_cases(request):
    if request.method == "POST":
        action = request.POST.get("action")
        case = get_object_or_404(CaseStudy, pk=request.POST.get("id"))
        if action == "toggle_publish":
            case.published = not case.published
            case.save(update_fields=["published"])
            messages.success(request, _("Sichtbarkeit geändert."))
        elif action == "delete":
            case.delete()
            messages.success(request, _("Referenz gelöscht."))
        return redirect("web:admin_cases")
    return render(request, "custom_admin/cases.html", {
        "nav": "cases",
        "items": CaseStudy.objects.order_by("-date"),
    })


@admin_required
def admin_case_edit(request, pk=None):
    case = get_object_or_404(CaseStudy, pk=pk) if pk else None
    if request.method == "POST":
        form = CaseStudyForm(request.POST, request.FILES, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, _("Referenz gespeichert."))
            return redirect("web:admin_cases")
    else:
        form = CaseStudyForm(instance=case)
    return render(request, "custom_admin/case_form.html", {
        "nav": "cases", "form": form, "case": case,
    })


# --- Inhalts-Blöcke (CMS-lite) ----------------------------------------------
@admin_required
def admin_content(request):
    if request.method == "POST":
        if request.POST.get("action") == "delete":
            get_object_or_404(ContentBlock, pk=request.POST.get("id")).delete()
            messages.success(request, _("Inhalts-Block gelöscht."))
        return redirect("web:admin_content")
    return render(request, "custom_admin/content.html", {
        "nav": "content",
        "items": ContentBlock.objects.all(),
    })


@admin_required
def admin_content_edit(request, pk=None):
    block = get_object_or_404(ContentBlock, pk=pk) if pk else None
    if request.method == "POST":
        form = ContentBlockForm(request.POST, request.FILES, instance=block)
        if form.is_valid():
            form.save()
            messages.success(request, _("Inhalts-Block gespeichert."))
            return redirect("web:admin_content")
    else:
        form = ContentBlockForm(instance=block)
    return render(request, "custom_admin/content_form.html", {
        "nav": "content", "form": form, "block": block,
    })
