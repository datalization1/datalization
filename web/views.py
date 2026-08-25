import logging
import json
from datetime import timedelta
from urllib import error, parse, request as urllib_request
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from django.conf import settings
from django.core import signing
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from .models import CaseStudy, ContactMessage, StartRequest
from .forms import ContactForm, StartForm
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

CONTACT_FORM_TOKEN_SALT = "web.contact_form"
CONTACT_FORM_MIN_SECONDS = 3
CONTACT_FORM_MAX_AGE_SECONDS = 3600

# --- SEO: Titel und Beschreibung je Seite ---------------------------------
# base.html liest page_title / page_description aus dem Kontext. Damit haben
# alle Seiten eigene Suchergebnis-Texte und behalten gleichzeitig Canonical,
# OpenGraph-Bild und JSON-LD aus dem Basistemplate.

SEO = {
    "home": {
        "de": ("IT, Daten und Software für KMU | datalization Zofingen",
               "IT-Support für Microsoft 365 und Azure, individuelle Software- und Datenprojekte sowie Monekey, unsere Dokumentenplattform – für Schweizer KMU."),
        "en": ("IT, data and software for SMEs | datalization Zofingen",
               "IT support for Microsoft 365 and Azure, custom software and data projects, plus Monekey, our document platform – for Swiss SMEs."),
    },
    "services": {
        "de": ("Lösungen: Software, Daten & Digitalisierung | datalization",
               "Softwareentwicklung, Datenanalyse und Business Intelligence, Digitalisierung und Data-Science-Beratung – von der Analyse über die Entwicklung bis zum Betrieb."),
        "en": ("Solutions: software, data & digitalization | datalization",
               "Software development, data analytics and business intelligence, digitalization and data science consulting – from analysis through development to operation."),
    },
    "about": {
        "de": ("Über uns – wer hinter Datalization steht",
               "Datalization ist ein inhabergeführtes Daten- und IT-Unternehmen aus Zofingen. Loyalität, Einfachheit und Qualität – daran messen wir uns in jedem Projekt."),
        "en": ("About us – the people behind Datalization",
               "Datalization is an owner-led data and IT company based in Zofingen, Switzerland. Loyalty, simplicity and quality guide every project we take on."),
    },
    "cases": {
        "de": ("Projekte und Referenzen | Datalization",
               "Projekte von Datalization: von der Ausgangslage über die Lösung bis zum messbaren Ergebnis – Software, Datenanalyse und Digitalisierung für Schweizer KMU."),
        "en": ("Projects and references | Datalization",
               "Projects by Datalization: from the initial situation through the solution to measurable results – software, data analytics and digitalization for Swiss SMEs."),
    },
    "contact": {
        "de": ("Kontakt | Datalization, Zofingen",
               "Schreiben Sie uns zu IT-Support, Cloud, Datenanalyse, Softwareentwicklung oder Digitalisierung. Wir melden uns persönlich – Datalization, 4800 Zofingen."),
        "en": ("Contact | Datalization, Zofingen",
               "Get in touch about IT support, cloud, data analytics, software development or digitalization. We reply personally – Datalization, 4800 Zofingen, Switzerland."),
    },
    "booking": {
        "de": ("Kurz-Check buchen – 20 Minuten, unverbindlich | Datalization",
               "Kostenloses 20-Minuten-Gespräch: Wir klären unverbindlich, ob unsere Leistungen zu Ihrer Situation passen – mit Einschätzung und nächsten Schritten."),
        "en": ("Book a short check – 20 minutes | datalization",
               "A free 20-minute conversation: we clarify whether and how our services fit your situation – with a concrete assessment and clear next steps."),
    },
    "match": {
        "de": ("Was passt zu Ihnen? Der 3-Fragen-Check | Datalization",
               "Drei kurze Fragen – danach wissen Sie, welche Lösung von Datalization zu Ihrer Ausgangslage passt. Ohne Anmeldung und unverbindlich."),
        "en": ("Which solution fits you? The 3-question check | Datalization",
               "Three short questions – then you know which Datalization solution fits your situation. No sign-up, no obligation."),
    },
    "monekey": {
        "de": ("Monekey – Dokumentenplattform für Treuhand & Immobilien",
               "Die digitale Dokumentenplattform für Immobilienverwaltung, Treuhand und Brokerage – mit Kundenportal, Berechtigungen und zentraler Ablage."),
        "en": ("Monekey – Document platform for trust & real estate",
               "The digital document platform for real estate management, trust and brokerage – with client portals, role-based permissions and central storage."),
    },
    "service_it_support": {
        "de": ("IT-Support & Cloud für KMU – Datalization",
               "Wir übernehmen Ihren IT-Betrieb: Microsoft 365, Azure, Datenmigration und laufender Support für KMU – zuverlässig, persönlich und mit festem Ansprechpartner."),
        "en": ("IT Support & Cloud for SMEs – Datalization",
               "We run your IT: Microsoft 365, Azure, data migration and ongoing support for SMEs – reliable, personal and with a named contact."),
    },
    "service_data_analytics": {
        "de": ("Datenanalyse & Data Science – Datalization",
               "Aus Zahlen wird Klarheit: Dashboards, KPI-Monitoring und Prognosen. Wir helfen KMU, den Überblick zu gewinnen und aus Erfahrung zu lernen – ohne Daten-Chaos."),
        "en": ("Data Analytics & Data Science – Datalization",
               "Turning numbers into clarity: dashboards, KPI monitoring and forecasting. We help SMEs gain an overview and learn from experience – without the data chaos."),
    },
    "service_software": {
        "de": ("Softwareentwicklung – Datalization",
               "Software, die mitdenkt: massgeschneiderte Web- und Datenapplikationen, API-Integrationen und skalierbare Architekturen – passend zu Ihren Prozessen."),
        "en": ("Software Development – Datalization",
               "Software that fits: custom web and data applications, API integrations and scalable architectures – built around your processes."),
    },
    "service_digitalisierung": {
        "de": ("Digitalisierung & Automatisierung – Datalization",
               "Weniger manuelle Arbeit, mehr Übersicht: Prozesse modernisieren, Systeme verbinden und Mitarbeitende befähigen – pragmatisch und in machbaren Schritten."),
        "en": ("Digitalization & Automation – Datalization",
               "Less manual work, more overview: modernize processes, connect systems and enable your team – pragmatic and in achievable steps."),
    },
    "service_beratung": {
        "de": ("Beratung & Strategie – Datalization",
               "Klarheit im Kopf und ein Plan, der sich lohnt: Use-Case-Scoping, Technologiebewertung und Roadmaps – Orientierung, bevor Sie investieren."),
        "en": ("Consulting & Strategy – Datalization",
               "Clarity and a plan worth following: use case scoping, technology assessment and roadmaps – orientation before you invest."),
    },
}


def seo(key, **extra):
    """Kontext mit Titel und Beschreibung fuer die aktuelle Sprache."""
    from django.utils.translation import get_language

    lang = (get_language() or "de").split("-")[0]
    title, desc = SEO[key].get(lang, SEO[key]["de"])
    ctx = {"page_title": title, "page_description": desc}
    ctx.update(extra)
    return ctx


@ensure_csrf_cookie
def home(request):
    case_studies = CaseStudy.objects.filter(published=True).order_by("-date")[:6]
    return render(request, "home.html", seo("home", case_studies=case_studies))


def about(request):
    return render(request, "about.html", seo("about"))

def services(request):
    return render(request, "services.html", seo("services"))


def service_data_analytics(request):
    return render(request, "services/data_analytics.html", seo("service_data_analytics"))


def service_software(request):
    return render(request, "services/softwareentwicklung.html", seo("service_software"))


def service_digitalisierung(request):
    return render(request, "services/digitalisierung.html", seo("service_digitalisierung"))


def service_beratung(request):
    return render(request, "services/beratung_strategie.html", seo("service_beratung"))


def service_it_support(request):
    return render(request, "services/it_support.html", seo("service_it_support"))


def monekey(request):
    return render(request, "monekey.html", seo("monekey"))


def start(request):
    # Weiterleitung auf die neue Booking-Seite
    return redirect("web:booking")

def booking(request):
    return render(request, "booking.html", seo("booking", form=StartForm(initial={"language": request.LANGUAGE_CODE})))


def match(request):
    return render(request, "match.html", seo("match"))


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
    return render(request, "cases_list.html", seo("cases", cases=qs))


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


def _make_contact_form_token(request):
    return signing.dumps(
        {
            "path": request.path,
            "ts": timezone.now().timestamp(),
        },
        salt=CONTACT_FORM_TOKEN_SALT,
    )


def _get_client_ip(request):
    forwarded_for = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _validate_contact_form_token(request):
    token = request.POST.get("contact_form_token", "")
    if not token:
        return False

    try:
        payload = signing.loads(
            token,
            salt=CONTACT_FORM_TOKEN_SALT,
            max_age=CONTACT_FORM_MAX_AGE_SECONDS,
        )
    except signing.BadSignature:
        return False
    except signing.SignatureExpired:
        return False

    if payload.get("path") != request.path:
        return False

    rendered_at = payload.get("ts")
    if rendered_at is None:
        return False

    age_seconds = timezone.now().timestamp() - float(rendered_at)
    return age_seconds >= CONTACT_FORM_MIN_SECONDS


def _validate_turnstile(request):
    if not getattr(settings, "TURNSTILE_ENABLED", False):
        return True

    token = request.POST.get("cf-turnstile-response", "").strip()
    if not token:
        return False

    try:
        encoded_payload = parse.urlencode(
            {
                "secret": settings.TURNSTILE_SECRET_KEY,
                "response": token,
                "remoteip": _get_client_ip(request),
            }
        ).encode("utf-8")
        verify_request = urllib_request.Request(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data=encoded_payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib_request.urlopen(verify_request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (error.URLError, ValueError, json.JSONDecodeError) as exc:
        logger.warning("Turnstile validation failed: %s", exc)
        return False

    return bool(payload.get("success"))


def _contact_context(request, form):
    return seo(
        "contact",
        form=form,
        contact_form_token=_make_contact_form_token(request),
        turnstile_enabled=getattr(settings, "TURNSTILE_ENABLED", False),
        turnstile_site_key=getattr(settings, "TURNSTILE_SITE_KEY", ""),
    )


@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        form_is_valid = form.is_valid()

        if request.POST.get("website"):
            form.add_error(None, _("Spam detection triggered."))
        if not _validate_contact_form_token(request):
            form.add_error(
                None,
                _(
                    "Bitte senden Sie das Formular erneut ab."
                    if request.LANGUAGE_CODE == "de"
                    else "Please submit the form again."
                ),
            )
        if not _validate_turnstile(request):
            form.add_error(
                None,
                _(
                    "Bitte bestätigen Sie, dass Sie ein Mensch sind."
                    if request.LANGUAGE_CODE == "de"
                    else "Please confirm that you are human."
                ),
            )

        if form_is_valid and not form.errors:
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
                msg = form.save(commit=False)
                msg.language = request.LANGUAGE_CODE
                msg.save()

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
        return render(request, "contact.html", _contact_context(request, form), status=400)

    # GET
    form = ContactForm(initial={"language": request.LANGUAGE_CODE})
    return render(request, "contact.html", _contact_context(request, form))

def impressum(request):
    return render(request, "impressum.html")

def privacy(request):
    return render(request, "privacy.html")
