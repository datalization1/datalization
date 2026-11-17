"""Eigenständige Admin: Login-Schutz, Seiten rendern, Referenz/Block anlegen."""
import datetime

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import CaseStudy, ContentBlock

SETTINGS = override_settings(
    ADMIN_PASSWORD="test-pw",
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)


@SETTINGS
class CustomAdminTests(TestCase):
    def _login(self):
        return self.client.post(reverse("web:admin_login"), {"password": "test-pw"})

    def test_requires_login(self):
        resp = self.client.get(reverse("web:custom_admin"))
        self.assertRedirects(resp, reverse("web:admin_login"))

    def test_wrong_password(self):
        self.client.post(reverse("web:admin_login"), {"password": "falsch"})
        self.assertRedirects(self.client.get(reverse("web:custom_admin")),
                             reverse("web:admin_login"))

    def test_all_pages_render_after_login(self):
        self._login()
        for name in ["custom_admin", "admin_contacts", "admin_bookings",
                     "admin_cases", "admin_case_new", "admin_content", "admin_content_new"]:
            self.assertEqual(self.client.get(reverse(f"web:{name}")).status_code, 200, name)

    def test_create_case(self):
        self._login()
        resp = self.client.post(reverse("web:admin_case_new"), {
            "title": "Testprojekt AG", "category": "Odoo", "slug": "",
            "date": "2026-11-17", "published": "on",
            "problem_brief": "Altsystem", "summary": "Odoo eingeführt",
            "result_points": "Zeit gespart", "client_brief": "Treuhand",
        })
        self.assertRedirects(resp, reverse("web:admin_cases"))
        c = CaseStudy.objects.get(title="Testprojekt AG")
        self.assertEqual(c.slug, "testprojekt-ag")  # auto-slug

    def test_create_content_block(self):
        self._login()
        resp = self.client.post(reverse("web:admin_content_new"), {
            "key": "home_hero_title", "label": "Hero Titel",
            "text_de": "Einfache Lösungen", "text_en": "Simple solutions",
        })
        self.assertRedirects(resp, reverse("web:admin_content"))
        self.assertTrue(ContentBlock.objects.filter(key="home_hero_title").exists())

    def test_django_admin_disabled(self):
        self.assertEqual(self.client.get("/admin/").status_code, 404)
