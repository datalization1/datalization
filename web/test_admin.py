"""Smoke-Test der Django-Admin: Listen + Formulare rendern für eingeloggten Staff."""
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import CaseStudy, ContactMessage, StartRequest

NO_MANIFEST = override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})


@NO_MANIFEST
class AdminSmokeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_superuser("tester", "t@example.com", "pw-123456")
        ContactMessage.objects.create(first_name="Max", last_name="Muster",
                                      email="max@example.com", service="Odoo", message="Hallo")
        StartRequest.objects.create(first_name="Erika", last_name="Beispiel",
                                    email="erika@example.com", branches="odoo", language="de")

    def setUp(self):
        self.client.login(username="tester", password="pw-123456")

    def test_index_and_changelists(self):
        urls = [
            reverse("admin:index"),
            reverse("admin:web_contactmessage_changelist"),
            reverse("admin:web_startrequest_changelist"),
            reverse("admin:web_casestudy_changelist"),
        ]
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_change_forms_render(self):
        cm = ContactMessage.objects.first()
        sr = StartRequest.objects.first()
        self.assertEqual(self.client.get(
            reverse("admin:web_contactmessage_change", args=[cm.pk])).status_code, 200)
        self.assertEqual(self.client.get(
            reverse("admin:web_startrequest_change", args=[sr.pk])).status_code, 200)
        # Case-Study-Formular (mit Bild-Upload-Feld)
        self.assertEqual(self.client.get(
            reverse("admin:web_casestudy_add")).status_code, 200)


@NO_MANIFEST
class AdminBrandingTests(TestCase):
    def test_login_page_uses_datalization_branding(self):
        resp = self.client.get(reverse("admin:login"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Datalization")      # Wortmarke statt „Django administration"
        self.assertContains(resp, "#F48B2D")           # Brand-Orange-Override geladen
