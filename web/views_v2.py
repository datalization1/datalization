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


def v2_digitalisierung(request):
    return render(request, "v2/digitalisierung.html", {"active": "digitalisierung"})


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

            try:
                context = {"msg": msg}
                subject_admin = f"[Datalization] Neue Kontaktanfrage von {msg.first_name} {msg.last_name}"
                text_admin = render_to_string("emails/contact_admin.txt", context)
                html_admin = render_to_string("emails/contact_admin.html", context)
                email_admin = EmailMultiAlternatives(
                    subject=subject_admin, body=text_admin,
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                    to=[getattr(settings, "CONTACT_RECEIVER_EMAIL", "info@datalization.ch")],
                )
                email_admin.attach_alternative(html_admin, "text/html")
                email_admin.send(fail_silently=True)
            except Exception:
                pass

            try:
                context_u = {"msg": msg}
                subject_user = ("Vielen Dank für Ihre Anfrage bei datalization"
                                if msg.language == "de" else "Thank you for contacting datalization")
                text_user = render_to_string("emails/contact_user.txt", context_u)
                html_user = render_to_string("emails/contact_user.html", context_u)
                email_user = EmailMultiAlternatives(
                    subject=subject_user, body=text_user,
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                    to=[msg.email],
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
def v2_booking(request):
    return render(request, "v2/booking.html", {"form": StartForm(initial={"language": request.LANGUAGE_CODE})})


@require_http_methods(["POST"])
@ensure_csrf_cookie
def v2_booking_submit(request):
    form = StartForm(request.POST)
    if form.is_valid():
        req = form.save()

        try:
            ctx = {"req": req}
            subject_admin = f"[Datalization] Neue Erstgespräch-Anfrage von {req.first_name} {req.last_name}"
            text_admin = render_to_string("emails/start_admin.txt", ctx)
            email_admin = EmailMessage(
                subject=subject_admin, body=text_admin,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                to=[getattr(settings, "CONTACT_RECEIVER_EMAIL", "info@datalization.ch")],
            )
            email_admin.send(fail_silently=True)
        except Exception:
            pass

        try:
            ctx_u = {"req": req}
            subject_user = "Danke für Ihre Anfrage" if req.language == "de" else "Thank you for your request"
            text_user = render_to_string("emails/start_user.txt", ctx_u)
            email_user = EmailMessage(
                subject=subject_user, body=text_user,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                to=[req.email],
            )
            email_user.send(fail_silently=True)
        except Exception:
            pass

        messages.success(request, "Danke! Wir melden uns in Kürze." if request.LANGUAGE_CODE == "de"
                         else "Thank you! We’ll get back to you shortly.")
        return redirect("v2:booking")

    messages.error(request, "Bitte prüfen Sie Ihre Eingaben." if request.LANGUAGE_CODE == "de"
                   else "Please check your input.")
    return render(request, "v2/booking.html", {"form": form})
