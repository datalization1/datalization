"""Rendert die neuen „IT für KMU"-Seiten in DE und EN (200, Kerninhalt, Nav)."""
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation

# Nicht-Manifest-Static im Test (sonst ValueError: missing staticfiles manifest).
NO_MANIFEST = override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})


@NO_MANIFEST
class ITPagesRenderTests(TestCase):
    CASES = [
        ("it_fuer_kmu", "IT für KMU", "IT for SMEs"),
        ("it_projektleitung", "IT-Projekt", "IT project"),
        ("it_support", "Microsoft 365", "Microsoft 365"),
    ]

    def test_pages_render_de_en(self):
        for name, de_needle, en_needle in self.CASES:
            for lang, needle in (("de", de_needle), ("en", en_needle)):
                with translation.override(lang):
                    url = reverse(f"v2:{name}")
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, 200, f"{name} [{lang}]")
                self.assertContains(resp, needle)

    def test_nav_shows_it_fuer_kmu(self):
        with translation.override("de"):
            resp = self.client.get(reverse("v2:it_fuer_kmu"))
        self.assertContains(resp, "IT für KMU")
        self.assertContains(resp, "IT-Projektleitung")
        self.assertContains(resp, "IT-Support &amp; Microsoft 365")
        self.assertNotContains(resp, "Digitalisierung &amp; Entwicklung")  # alter Menüname weg
