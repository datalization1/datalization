"""
Views für die Website v2.0 (Neugestaltung parallel zur Bestandsseite).

Diese Datei ist komplett neu und verändert nichts an web/views.py.
Alle v2-Seiten laufen unter dem URL-Präfix /de/v2/ bzw. /en/v2/ und
tragen vorerst <meta name="robots" content="noindex"> (siehe base_v2.html).

Die Formular-Views (Kontakt, Booking) verwenden die bestehende Logik aus
web/views.py (Token, Honeypot, Turnstile, E-Mail-Versand) wieder – die
v1-Seiten bleiben dabei unangetastet.
"""
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from . import views as web_views
from .forms import ContactForm, StartForm
from .models import ContactMessage

# Booking-Formular: die <select>-Werte sind Maschinen-Codes. Fürs Mail lesbar
# machen (DE, EN). Reihenfolge/Werte identisch zu booking.html.
BOOKING_TOPICS = {
    "general": ("Allgemeine Beratung", "General consulting"),
    "odoo": ("Odoo", "Odoo"),
    "digitalisierung": ("Digitalisierung & Entwicklung", "Digitalization & Development"),
    "data-analytics": ("Daten & Analyse", "Data & Analytics"),
    "monekey": ("Monekey", "Monekey"),
}
BOOKING_TIMES = {
    "morning": ("Vormittags (9–12 Uhr)", "Morning (9–12)"),
    "afternoon": ("Nachmittags (12–17 Uhr)", "Afternoon (12–17)"),
    "evening": ("Abends (17–20 Uhr)", "Evening (17–20)"),
}


def _booking_labels(req):
    """Lesbare Anzeige-Werte fürs Mail (Thema/Wunschzeit je nach Sprache).

    Achtung historische Feldnamen: branches=Thema/Anliegen, pains=Wunschdatum,
    start_mode=Wunschzeit (so legt es booking.html ab)."""
    i = 1 if req.language == "en" else 0
    topic = BOOKING_TOPICS.get(req.branches, (req.branches or "", req.branches or ""))[i]
    time = BOOKING_TIMES.get(req.start_mode, (req.start_mode or "", req.start_mode or ""))[i]
    return {
        "language": req.language,
        "topic_display": topic,
        "time_display": time,
        "date_display": req.pains or "",
    }


def _flag(request, name):
    """Platzhalter-Schalter. Standard AUS; per Query-Param (?foto=1) zuschaltbar
    für die Vorschau, ohne Code zu ändern."""
    return request.GET.get(name) == "1"


def v2_home(request):
    return render(request, "v2/home.html", {
        # Platzhalter (Foto, Odoo-Badge, Referenz) – Standard aus, siehe HANDOFF.md.
        "show_foto": _flag(request, "foto"),
        "show_badge": _flag(request, "badge"),
        "show_referenz": _flag(request, "referenz"),
    })


def v2_odoo(request):
    return render(request, "v2/odoo.html", {"active": "odoo", "odoo_sub": "overview"})


def v2_odoo_wieso(request):
    return render(request, "v2/odoo_wieso.html", {"active": "odoo", "odoo_sub": "wieso"})


def v2_odoo_einfuehrung(request):
    return render(request, "v2/odoo_einfuehrung.html", {"active": "odoo", "odoo_sub": "einfuehrung"})


def v2_odoo_vergleich(request):
    return render(request, "v2/odoo_vergleich.html", {"active": "odoo", "odoo_sub": "vergleich"})


def v2_data_analytics(request):
    return render(request, "v2/data_analytics.html", {"active": "data_analytics"})


# ---------------------------------------------------------------------------
# SEO-Landingpages (lokal / Keyword / Branche). Aus der Nav heraus, via Footer
# und kontextuell verlinkt. Vorerst noindex wie der Rest von v2.
# ---------------------------------------------------------------------------
def v2_seo_erp_kmu(request):
    return render(request, "v2/seo_erp_kmu.html")


def v2_seo_buchhaltung(request):
    return render(request, "v2/seo_buchhaltung.html")


def v2_seo_treuhand(request):
    return render(request, "v2/seo_treuhand.html")


def v2_seo_handwerk(request):
    return render(request, "v2/seo_handwerk.html")


def v2_seo_olten(request):
    return render(request, "v2/seo_olten.html")


def v2_digitalisierung(request):
    return render(request, "v2/digitalisierung.html", {"active": "digitalisierung"})


def v2_softwareentwicklung(request):
    return render(request, "v2/softwareentwicklung.html", {"active": "softwareentwicklung"})


def v2_it_fuer_kmu(request):
    return render(request, "v2/it_fuer_kmu.html", {"active": "it_fuer_kmu"})


def v2_it_projektleitung(request):
    return render(request, "v2/it_projektleitung.html", {"active": "it_projektleitung"})


def v2_it_support(request):
    return render(request, "v2/it_support_m365.html", {"active": "it_support"})


def v2_monekey(request):
    return render(request, "v2/monekey.html", {"active": "monekey"})


def v2_odoo_partner(request):
    return render(request, "v2/odoo_partner_zofingen.html", {"active": "odoo_partner"})


def v2_ueber_datalization(request):
    return render(request, "v2/ueber_datalization.html", {
        "show_foto": _flag(request, "foto"),
    })


def v2_impressum(request):
    return render(request, "v2/impressum.html")


def v2_datenschutz(request):
    return render(request, "v2/datenschutz.html")


# ---------------------------------------------------------------------------
# Kontaktformular (gleiche Logik wie web.views.contact, eigenes v2-Template)
# ---------------------------------------------------------------------------
@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
def v2_kontakt(request):
    if request.method != "POST":
        return render(request, "v2/kontakt.html", web_views._contact_context(request, ContactForm()))

    form = ContactForm(request.POST)
    form_is_valid = form.is_valid()

    if request.POST.get("website"):
        form.add_error(None, "Spam detection triggered.")
    if not web_views._validate_contact_form_token(request):
        form.add_error(None, "Bitte senden Sie das Formular erneut ab." if request.LANGUAGE_CODE == "de"
                       else "Please submit the form again.")
    if not web_views._validate_turnstile(request):
        form.add_error(None, "Bitte bestätigen Sie, dass Sie ein Mensch sind." if request.LANGUAGE_CODE == "de"
                       else "Please confirm that you are human.")

    if form_is_valid and not form.errors:
        cd = form.cleaned_data

        # De-Dup: gleiche E-Mail + gleicher Text innerhalb von 20 Sekunden
        window_start = timezone.now() - timedelta(seconds=20)
        exists = ContactMessage.objects.filter(
            email=cd["email"], message=cd["message"], created__gte=window_start,
        ).exists()

        if not exists:
            msg = form.save(commit=False)
            msg.language = request.LANGUAGE_CODE
            msg.save()

            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch")

            try:
                context = {"msg": msg}
                anliegen = msg.service or "Allgemeine Anfrage"
                subject_admin = f"Neue Anfrage: {anliegen} – {msg.first_name} {msg.last_name}"
                text_admin = render_to_string("emails/contact_admin.txt", context)
                html_admin = render_to_string("emails/contact_admin.html", context)
                email_admin = EmailMultiAlternatives(
                    subject=subject_admin, body=text_admin, from_email=from_email,
                    to=[getattr(settings, "CONTACT_RECEIVER_EMAIL", "info@datalization.ch")],
                    reply_to=[msg.email],   # Antwort in Outlook geht direkt an den Absender
                )
                email_admin.attach_alternative(html_admin, "text/html")
                email_admin.send(fail_silently=True)
            except Exception:
                pass

            try:
                context_u = {"msg": msg, "language": msg.language}
                subject_user = ("Vielen Dank für Ihre Anfrage bei Datalization"
                                if msg.language != "en" else "Thank you for contacting Datalization")
                text_user = render_to_string("emails/contact_confirmation.txt", context_u)
                html_user = render_to_string("emails/contact_confirmation.html", context_u)
                email_user = EmailMultiAlternatives(
                    subject=subject_user, body=text_user, from_email=from_email, to=[msg.email],
                )
                email_user.attach_alternative(html_user, "text/html")
                email_user.send(fail_silently=True)
            except Exception:
                pass

        messages.success(request, "Ihre Nachricht wurde erfolgreich gesendet." if request.LANGUAGE_CODE == "de"
                         else "Your message was sent successfully.")
        return redirect("v2:kontakt")

    messages.error(request, "Bitte prüfen Sie Ihre Eingaben." if request.LANGUAGE_CODE == "de"
                   else "Please check your input.")
    return render(request, "v2/kontakt.html", web_views._contact_context(request, form))


# ---------------------------------------------------------------------------
# Erstgespräch / Booking (gleiche Logik wie web.views.start_submit)
# ---------------------------------------------------------------------------
def _booking_context(request, form=None):
    return {
        "form": form or StartForm(initial={"language": request.LANGUAGE_CODE}),
        "today": timezone.localdate().isoformat(),
        "turnstile_enabled": getattr(settings, "TURNSTILE_ENABLED", False),
        "turnstile_site_key": getattr(settings, "TURNSTILE_SITE_KEY", ""),
    }


def v2_booking(request):
    return render(request, "v2/booking.html", _booking_context(request))


@require_http_methods(["POST"])
@ensure_csrf_cookie
def v2_booking_submit(request):
    form = StartForm(request.POST)

    # Spam-Schutz wie beim Kontaktformular: Honeypot + Cloudflare Turnstile.
    # Beide bauen graceful ab (Honeypot immer aktiv; Turnstile nur wenn Keys gesetzt).
    spam = bool(request.POST.get("website")) or not web_views._validate_turnstile(request)

    if form.is_valid() and not spam:
        req = form.save()

        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch")
        labels = _booking_labels(req)   # lesbare Thema/Wunschzeit/-datum

        try:
            ctx = {"req": req, **labels}
            anliegen = labels["topic_display"] or "Erstgespräch"
            subject_admin = f"Neue Anfrage: {anliegen} – {req.first_name} {req.last_name}"
            text_admin = render_to_string("emails/start_admin.txt", ctx)
            email_admin = EmailMessage(
                subject=subject_admin, body=text_admin, from_email=from_email,
                to=[getattr(settings, "CONTACT_RECEIVER_EMAIL", "info@datalization.ch")],
                reply_to=[req.email],   # Antwort geht direkt an den Absender
            )
            email_admin.send(fail_silently=True)
        except Exception:
            pass

        try:
            ctx_u = {"req": req, **labels}
            subject_user = ("Vielen Dank für Ihre Anfrage bei Datalization"
                            if req.language != "en" else "Thank you for contacting Datalization")
            text_user = render_to_string("emails/booking_confirmation.txt", ctx_u)
            html_user = render_to_string("emails/booking_confirmation.html", ctx_u)
            email_user = EmailMultiAlternatives(
                subject=subject_user, body=text_user, from_email=from_email, to=[req.email],
            )
            email_user.attach_alternative(html_user, "text/html")
            email_user.send(fail_silently=True)
        except Exception:
            pass

        # Eigene Danke-Seite (eigene URL) – für Google-Ads-Conversion-Tracking.
        return redirect("v2:booking_thanks")

    messages.error(request, "Bitte prüfen Sie Ihre Eingaben." if request.LANGUAGE_CODE == "de"
                   else "Please check your input.")
    return render(request, "v2/booking.html", _booking_context(request, form))


def v2_booking_thanks(request):
    """Bestätigungs-/Danke-Seite nach erfolgreicher Buchung (eigene URL für die
    Google-Ads-Conversion). Erreichbar unter /de/termin/danke/ bzw. /en/…."""
    return render(request, "v2/booking_thanks.html", {"active": "booking"})
