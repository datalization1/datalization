"""Booking leitet nach Erfolg auf die eigene Danke-Seite (Google-Ads-Conversion)."""
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation

NO_MANIFEST = override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
                   TURNSTILE_ENABLED=False)
class BookingRedirectTests(TestCase):
    def test_success_redirects_to_thanks(self):
        data = {"first_name": "Erika", "last_name": "Beispiel", "email": "erika@example.com",
                "branches": "odoo", "start_mode": "morning", "language": "de", "website": ""}
        with patch("web.views._validate_turnstile", return_value=True):
            resp = self.client.post(reverse("v2:booking_submit"), data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], reverse("v2:booking_thanks"))


@NO_MANIFEST
class BookingThanksRenderTests(TestCase):
    def test_renders_de_en_with_noindex(self):
        for lang, needle in (("de", "Vielen Dank"), ("en", "Thank you")):
            with translation.override(lang):
                url = reverse("v2:booking_thanks")
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200, f"[{lang}]")
            self.assertContains(resp, needle)
            self.assertContains(resp, "noindex")
