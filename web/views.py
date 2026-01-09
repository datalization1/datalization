from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from .models import CaseStudy, ContactMessage, StartRequest
from .forms import ContactForm, StartForm
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

@ensure_csrf_cookie
def home(request):
    case_studies = CaseStudy.objects.filter(published=True).order_by("-date")[:6]
    return render(request, "home.html", {"case_studies": case_studies})


def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")


def service_data_analytics(request):
    return render(request, "services/data_analytics.html")


def service_software(request):
    return render(request, "services/softwareentwicklung.html")


def service_digitalisierung(request):
    return render(request, "services/digitalisierung.html")


def service_beratung(request):
    return render(request, "services/beratung_strategie.html")


def start(request):
    # Weiterleitung auf die neue Booking-Seite
    return redirect("web:booking")

def booking(request):
    return render(request, "booking.html", {"form": StartForm(initial={"language": request.LANGUAGE_CODE})})


def match(request):
    return render(request, "match.html")


@require_http_methods(["POST"])
@ensure_csrf_cookie
def start_submit(request):
    form = StartForm(request.POST)
    if form.is_valid():
        req = form.save()
        # Admin-Mail
        try:
            ctx = {"req": req}
            subject_admin = f"[Datalization] Neue Start-Anfrage von {req.first_name} {req.last_name}"
            text_admin = render_to_string("emails/start_admin.txt", ctx)
            email_admin = EmailMessage(
                subject=subject_admin,
                body=text_admin,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                to=[getattr(settings, "CONTACT_RECEIVER_EMAIL", "info@datalization.ch")],
            )
            email_admin.send(fail_silently=True)
        except Exception:
            pass

        # User-Bestätigung
        try:
            ctx_u = {"req": req}
            subject_user = "Danke für deine Anfrage" if req.language == "de" else "Thank you for your request"
            text_user = render_to_string("emails/start_user.txt", ctx_u)
            email_user = EmailMessage(
                subject=subject_user,
                body=text_user,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                to=[req.email],
            )
            email_user.send(fail_silently=True)
        except Exception:
            pass

        messages.success(request, _("Danke! Wir melden uns in Kürze."))
        return redirect("web:start")

    messages.error(request, _("Bitte prüfe deine Eingaben."))
    return render(request, "start.html", {"form": form})


def case_list(request):
    qs = CaseStudy.objects.filter(published=True).order_by("-date")[:4]
    return render(request, "cases_list.html", {"cases": qs})


from django.shortcuts import render, get_object_or_404
from .models import CaseStudy

def case_detail(request, slug):
    case = get_object_or_404(CaseStudy, slug=slug, published=True)

    # Results as list via model helper
    results_list = case.result_list()

    return render(request, "case_detail.html", {
        "case": case,
        "results_list": results_list,
    })


def _admin_authorized(request):
    return request.session.get("custom_admin") is True


def custom_admin(request):
    admin_password = getattr(settings, "ADMIN_PASSWORD", None)

    # Handle logout
    if request.GET.get("logout"):
        request.session.pop("custom_admin", None)
        return redirect("web:custom_admin")

    # Handle login POST
    if request.method == "POST" and not _admin_authorized(request):
        provided = request.POST.get("password", "")
        if admin_password and provided == admin_password:
            request.session["custom_admin"] = True
            messages.success(request, _("Erfolgreich angemeldet."))
            return redirect("web:custom_admin")
        messages.error(request, _("Falsches Passwort."))

    if not _admin_authorized(request):
        return render(request, "custom_admin_login.html")

    # Simple actions
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "toggle_publish":
            case_id = request.POST.get("case_id")
            case = get_object_or_404(CaseStudy, id=case_id)
            case.published = not case.published
            case.save()
            messages.success(request, _("Status geändert für %(title)s") % {"title": case.title})
        elif action == "handle_contact":
            contact_id = request.POST.get("contact_id")
            msg = get_object_or_404(ContactMessage, id=contact_id)
            msg.handled = True
            msg.save(update_fields=["handled"])
            messages.success(request, _("Kontakt markiert als erledigt."))
        elif action == "handle_start":
            start_id = request.POST.get("start_id")
            start = get_object_or_404(StartRequest, id=start_id)
            start.handled = True
            start.save(update_fields=["handled"])
            messages.success(request, _("Start-Anfrage markiert als erledigt."))
        return redirect("web:custom_admin")

    cases_qs = CaseStudy.objects.all().order_by("-date")
    contacts_qs = ContactMessage.objects.all().order_by("-created")
    starts_qs = StartRequest.objects.all().order_by("-created")

    # Counts auf Basis der vollen QuerySets, nicht der gesliceten
    contacts_open = contacts_qs.filter(handled=False).count()
    contacts_done = contacts_qs.filter(handled=True).count()
    starts_open = starts_qs.filter(handled=False).count()
    starts_done = starts_qs.filter(handled=True).count()
    cases_published = cases_qs.filter(published=True).count()
    cases_hidden = cases_qs.filter(published=False).count()

    # Anzeige nur der neuesten 50
    cases = cases_qs
    contacts = contacts_qs[:50]
    starts = starts_qs[:50]

    return render(request, "custom_admin.html", {
        "cases": cases,
        "contacts": contacts,
        "starts": starts,
        "contacts_open": contacts_open,
        "contacts_done": contacts_done,
        "starts_open": starts_open,
        "starts_done": starts_done,
        "cases_published": cases_published,
        "cases_hidden": cases_hidden,
    })


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # De-Dup: gleiche Email + gleicher Text innerhalb von 20 Sekunden
            window_start = timezone.now() - timedelta(seconds=20)
            exists = ContactMessage.objects.filter(
                email=cd["email"],
                message=cd["message"],
                created__gte=window_start,
            ).exists()

            msg = None
            if not exists:
                msg = form.save()

                # ---------- Admin-Mail ----------
                try:
                    context = {"msg": msg}
                    subject_admin = f"[Datalization] Neue Kontaktanfrage von {msg.first_name} {msg.last_name}"

                    text_admin = render_to_string("emails/contact_admin.txt", context)
                    html_admin = render_to_string("emails/contact_admin.html", context)

                    email_admin = EmailMultiAlternatives(
                        subject=subject_admin,
                        body=text_admin,
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                        to=[getattr(settings, "CONTACT_RECEIVER_EMAIL", "info@datalization.ch")],
                    )
                    email_admin.attach_alternative(html_admin, "text/html")
                    email_admin.send(fail_silently=True)
                except Exception:
                    # Wir loggen nur – die Anfrage soll trotzdem durchgehen
                    pass

                # ---------- Bestätigungs-Mail an User ----------
                try:
                    context_u = {"msg": msg}
                    subject_user = (
                        "Vielen Dank für Ihre Anfrage bei datalization"
                        if msg.language == "de"
                        else "Thank you for contacting datalization"
                    )

                    text_user = render_to_string("emails/contact_user.txt", context_u)
                    html_user = render_to_string("emails/contact_user.html", context_u)

                    email_user = EmailMultiAlternatives(
                        subject=subject_user,
                        body=text_user,
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                        to=[msg.email],
                    )
                    email_user.attach_alternative(html_user, "text/html")
                    email_user.send(fail_silently=True)
                except Exception:
                    pass

            # Erfolgsmeldung Richtung Browser
            success_text = (
                "Danke! Wir melden uns in Kürze."
                if request.LANGUAGE_CODE == "de"
                else "Thank you! We'll get back to you soon."
            )

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"ok": True, "message": success_text})

            messages.success(request, _("Ihre Nachricht wurde erfolgreich gesendet."))
            return redirect("web:contact")

        # Form invalid
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)

        messages.error(
            request,
            "Bitte prüfen Sie Ihre Eingaben."
            if request.LANGUAGE_CODE == "de"
            else "Please check your input."
        )
        return redirect("web:home")

    # GET
    form = ContactForm(initial={"language": request.LANGUAGE_CODE})
    return render(request, "contact.html", {"form": form})

def impressum(request):
    return render(request, "impressum.html")

def privacy(request):
    return render(request, "privacy.html")
