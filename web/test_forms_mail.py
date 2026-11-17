"""Tests für Kontakt- und Booking-Formular-Mails (v2).

Deckt ab: korrekte Empfänger, reply_to, Betreff (mit Anliegen), alle Felder
inkl. Anliegen in der internen Mail, sowie Bestätigungsmail in DE und EN.
Nutzt das locmem-Backend (ändert settings.py nicht).
"""
from unittest.mock import patch

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation

from .models import ContactMessage, StartRequest

LOCMEM = "django.core.mail.backends.locmem.EmailBackend"


def _by_recipient(outbox, addr):
    return next(m for m in outbox if addr in m.to)


@override_settings(EMAIL_BACKEND=LOCMEM, TURNSTILE_ENABLED=False,
                   CONTACT_RECEIVER_EMAIL="info@datalization.ch")
class ContactFormMailTests(TestCase):
    def _url(self, lang):
        with translation.override(lang):
            return reverse("v2:kontakt")

    def _post(self, lang="de", **overrides):
        data = {
            "first_name": "Max", "last_name": "Muster", "company": "Muster AG",
            "email": "max@example.com", "phone": "079 123 45 67",
            "service": "Geschäftssoftware (Odoo)", "message": "Ich interessiere mich für Odoo.",
            "website": "", "contact_form_token": "x",
        }
        data.update(overrides)
        with patch("web.views._validate_contact_form_token", return_value=True), \
             patch("web.views._validate_turnstile", return_value=True):
            return self.client.post(self._url(lang), data)

    def test_anliegen_wird_gespeichert(self):
        """Regressions-Test für «Anliegen: -»: service landet im Modell + Mail."""
        resp = self._post()
        self.assertEqual(resp.status_code, 302)
        msg = ContactMessage.objects.get()
        self.assertEqual(msg.service, "Geschäftssoftware (Odoo)")

    def test_interne_mail_empfaenger_replyto_betreff_felder(self):
        self._post()
        self.assertEqual(len(mail.outbox), 2)
        admin = _by_recipient(mail.outbox, "info@datalization.ch")
        # Empfänger + reply_to
        self.assertEqual(admin.to, ["info@datalization.ch"])
        self.assertEqual(admin.reply_to, ["max@example.com"])
        # Betreff: «Neue Anfrage: [Anliegen] – [Name]»
        self.assertEqual(admin.subject, "Neue Anfrage: Geschäftssoftware (Odoo) – Max Muster")
        # alle Felder inkl. Anliegen im Body
        body = admin.body
        for needle in ["Max", "Muster", "Muster AG", "max@example.com",
                       "079 123 45 67", "Geschäftssoftware (Odoo)", "Odoo"]:
            self.assertIn(needle, body)
        self.assertNotIn("Anliegen: -", body)

    def test_bestaetigung_de(self):
        self._post(lang="de")
        user = _by_recipient(mail.outbox, "max@example.com")
        self.assertEqual(user.to, ["max@example.com"])
        self.assertIn("bei Datalization", user.body)       # Firmenname gross
        self.assertNotIn("bei datalization", user.body)    # nicht mehr klein
        self.assertIn("Geschäftssoftware (Odoo)", user.body)
        self.assertIn("Arbeitstag", user.body)
        self.assertIn("Tihomir Danesic", user.body)
        self.assertIn("Freundliche Grüsse", user.body)    # Schweizer ss
        # HTML-Alternative vorhanden + CI-Farbe
        html = user.alternatives[0][0]
        self.assertIn("#F48B2D", html)
        self.assertIn("Ihr Anliegen", html)

    def test_bestaetigung_en(self):
        self._post(lang="en")
        user = _by_recipient(mail.outbox, "max@example.com")
        self.assertIn("Thank you", user.body)
        self.assertIn("one business day", user.body)
        self.assertIn("Your topic", user.body)
        self.assertIn("Datalization", user.body)

    def test_fehlendes_anliegen_ist_pflicht(self):
        # Serverseitige Pflicht direkt am Formular geprüft (ohne Template-Render).
        from .forms import ContactForm
        form = ContactForm(data={
            "first_name": "Max", "last_name": "Muster", "email": "max@example.com",
            "message": "Test ohne Anliegen.", "service": "",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("service", form.errors)


@override_settings(EMAIL_BACKEND=LOCMEM, TURNSTILE_ENABLED=False,
                   CONTACT_RECEIVER_EMAIL="info@datalization.ch")
class BookingFormMailTests(TestCase):
    def _post(self, lang="de", **overrides):
        data = {
            "first_name": "Erika", "last_name": "Beispiel", "company": "Beispiel GmbH",
            "email": "erika@example.com", "phone": "062 111 22 33",
            "branches": "odoo", "notes": "Wir wollen Odoo einführen.",
            "pains": "2026-11-20", "start_mode": "morning", "language": lang,
            "website": "",
        }
        data.update(overrides)
        with patch("web.views._validate_turnstile", return_value=True):
            return self.client.post(reverse("v2:booking_submit"), data)

    def test_interne_mail_labels_replyto_betreff(self):
        resp = self._post()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(len(mail.outbox), 2)
        admin = _by_recipient(mail.outbox, "info@datalization.ch")
        self.assertEqual(admin.reply_to, ["erika@example.com"])
        self.assertEqual(admin.subject, "Neue Anfrage: Odoo – Erika Beispiel")
        body = admin.body
        # korrekte Beschriftung (nicht mehr Branchen/Themen/Startwunsch)
        self.assertIn("Anliegen: Odoo", body)
        self.assertIn("Wunschdatum: 2026-11-20", body)
        self.assertIn("Wunschzeit: Vormittags (9–12 Uhr)", body)
        self.assertIn("erika@example.com", body)

    def test_bestaetigung_de(self):
        self._post(lang="de")
        user = _by_recipient(mail.outbox, "erika@example.com")
        self.assertIn("Datalization", user.body)
        self.assertIn("Odoo", user.body)
        self.assertIn("Arbeitstag", user.body)
        self.assertIn("Tihomir Danesic", user.body)
        html = user.alternatives[0][0]
        self.assertIn("#F48B2D", html)

    def test_bestaetigung_en(self):
        self._post(lang="en")
        user = _by_recipient(mail.outbox, "erika@example.com")
        self.assertIn("Thank you", user.body)
        self.assertIn("one business day", user.body)
        self.assertIn("Odoo", user.body)
