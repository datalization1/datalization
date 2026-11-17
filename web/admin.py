# web/admin.py — Admin für die Website-Daten (Case Studies, Kontaktanfragen, Buchungen).
# Die CRM-/Lead-Models liegen in leadgen/admin.py.
import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from .models import CaseStudy, ContactMessage, StartRequest

admin.site.site_header = "Datalization – Verwaltung"
admin.site.site_title = "Datalization Admin"
admin.site.index_title = _("Übersicht")


# --- Gemeinsame Aktionen -----------------------------------------------------
@admin.action(description=_("Als CSV exportieren (Excel)"))
def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    fields = [f.name for f in meta.fields]
    resp = HttpResponse(content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = f"attachment; filename={meta.model_name}.csv"
    resp.write("﻿")  # BOM, damit Excel Umlaute korrekt zeigt
    writer = csv.writer(resp, delimiter=";")
    writer.writerow(fields)
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in fields])
    return resp


@admin.action(description=_("Als erledigt markieren"))
def mark_handled(modeladmin, request, queryset):
    n = queryset.update(handled=True)
    modeladmin.message_user(request, _("%(n)d als erledigt markiert.") % {"n": n})


@admin.action(description=_("Als offen markieren"))
def mark_unhandled(modeladmin, request, queryset):
    n = queryset.update(handled=False)
    modeladmin.message_user(request, _("%(n)d als offen markiert.") % {"n": n})


# --- Case Studies (Texte + Bild) --------------------------------------------
@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date", "published")
    list_filter = ("published", "category", "date")
    search_fields = ("title", "summary", "summary_en",
                     "client_brief", "problem_brief", "problem_brief_en", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("published",)
    date_hierarchy = "date"
    ordering = ("-date",)
    fieldsets = (
        (None, {"fields": ("title", "category", "slug", "preview_animation", "image", "date", "published")}),
        (_("Client"), {"fields": ("client_brief",)}),
        (_("Deutsche Version"), {
            "fields": ("problem_brief", "summary", "result_points"),
            "description": _("Beim Result jeweils eine Aussage pro Zeile.")}),
        (_("English Version"), {
            "fields": ("problem_brief_en", "summary_en", "result_points_en"),
            "description": _("Optional. Falls leer, wird auf die deutsche Version zurückgegriffen.")}),
        (_("KPIs & Tech"), {"fields": ("kpis", "tech_stack")}),
    )


# --- Kontaktanfragen (Kontaktformular) --------------------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("created", "first_name", "last_name", "company", "service", "email", "language", "handled")
    list_filter = ("handled", "service", "language", "created")
    search_fields = ("first_name", "last_name", "company", "email", "message", "service")
    readonly_fields = ("created", "first_name", "last_name", "company", "email", "phone", "service", "message", "language")
    date_hierarchy = "created"
    ordering = ("-created",)
    list_per_page = 50
    actions = (mark_handled, mark_unhandled, export_as_csv)
    fieldsets = (
        (_("Kontakt"), {"fields": ("created", ("first_name", "last_name"), "company", "email", "phone", "language")}),
        (_("Anliegen & Nachricht"), {"fields": ("service", "message")}),
        (_("Status"), {"fields": ("handled",)}),
    )


# --- Buchungen / Erstgespräch-Anfragen (Booking-Formular) -------------------
@admin.register(StartRequest)
class StartRequestAdmin(admin.ModelAdmin):
    list_display = ("created", "first_name", "last_name", "company", "anliegen", "email", "handled")
    list_filter = ("handled", "language", "created", "branches")
    search_fields = ("first_name", "last_name", "company", "email", "notes")
    readonly_fields = ("created", "first_name", "last_name", "company", "email", "phone",
                       "branches", "pains", "start_mode", "notes", "language")
    date_hierarchy = "created"
    ordering = ("-created",)
    list_per_page = 50
    actions = (mark_handled, mark_unhandled, export_as_csv)
    fieldsets = (
        (_("Kontakt"), {"fields": ("created", ("first_name", "last_name"), "company", "email", "phone", "language")}),
        (_("Anfrage"), {
            "fields": ("branches", "pains", "start_mode", "notes"),
            "description": _("Hinweis zu den Feldnamen: branches = Thema/Anliegen · "
                             "pains = Wunschdatum · start_mode = Wunschzeit.")}),
        (_("Status"), {"fields": ("handled",)}),
    )

    @admin.display(description=_("Anliegen"))
    def anliegen(self, obj):
        return obj.branches or "–"
