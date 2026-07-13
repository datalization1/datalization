from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.core import signing
from django.test.utils import override_settings
from datetime import date
import json
from unittest.mock import Mock, patch

from .models import CaseStudy
from .models import ContactMessage
from . import views


class SiteIconRoutesTests(TestCase):
    def test_favicon_route_serves_correct_png_icon(self):
        response = self.client.get("/favicon.ico")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")

    def test_apple_touch_icon_route_serves_png_file(self):
        response = self.client.get("/apple-touch-icon.png")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")

    def test_manifest_route_returns_json_payload(self):
        response = self.client.get("/site.webmanifest")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/manifest+json")

        payload = response.json()
        self.assertEqual(payload["name"], "datalization")
        self.assertEqual(payload["icons"][0]["sizes"], "192x192")
        self.assertEqual(payload["icons"][0]["src"], "/icon-192.png")

    def test_homepage_includes_favicon_links(self):
        response = self.client.get("/de/")
        html = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn('rel="icon" type="image/svg+xml"', html)
        self.assertIn('/static/img/favicon.', html)
        self.assertIn('href="/favicon-48.png"', html)
        self.assertIn('href="/favicon.ico"', html)
        self.assertIn('href="/site.webmanifest"', html)


class CaseImageRenderingTests(TestCase):
    def test_missing_case_image_does_not_render_broken_img_tag(self):
        case = CaseStudy.objects.create(
            title="Broken Media Case",
            slug="broken-media-case",
            summary="Test summary",
            date=date(2026, 1, 1),
            published=True,
        )
        case.image.name = "cases/does-not-exist.jpg"
        case.save(update_fields=["image"])

        response = self.client.get("/de/cases/")
        html = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('src="/media/cases/does-not-exist.jpg"', html)


class ContactFormProtectionTests(TestCase):
    def _contact_url(self):
        return reverse("web:contact")

    def _base_payload(self):
        response = self.client.get(self._contact_url())
        return {
            "first_name": "Max",
            "last_name": "Tester",
            "company": "Datalization",
            "email": "max@example.com",
            "phone": "+41 79 123 45 67",
            "message": "Ich brauche Hilfe beim Automatisieren unseres Workflows.",
            "contact_form_token": response.context["contact_form_token"],
            "website": "",
        }

    def test_contact_form_rejects_honeypot_submission(self):
        payload = self._base_payload()
        payload["website"] = "https://spam.invalid"

        with patch.object(views, "CONTACT_FORM_MIN_SECONDS", 0):
            response = self.client.post(
                self._contact_url(),
                payload,
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_form_rejects_too_fast_submission(self):
        payload = self._base_payload()
        payload["contact_form_token"] = signing.dumps(
            {
                "path": self._contact_url(),
                "ts": timezone.now().timestamp(),
            },
            salt=views.CONTACT_FORM_TOKEN_SALT,
        )

        response = self.client.post(
            self._contact_url(),
            payload,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactMessage.objects.count(), 0)

    @override_settings(TURNSTILE_ENABLED=True, TURNSTILE_SITE_KEY="site-key", TURNSTILE_SECRET_KEY="secret-key")
    def test_contact_form_rejects_invalid_turnstile_token(self):
        payload = self._base_payload()
        payload["cf-turnstile-response"] = "invalid-token"

        mocked_response = Mock()
        mocked_response.read.return_value = json.dumps(
            {"success": False, "error-codes": ["invalid-input-response"]}
        ).encode("utf-8")
        mocked_urlopen = Mock()
        mocked_urlopen.__enter__ = Mock(return_value=mocked_response)
        mocked_urlopen.__exit__ = Mock(return_value=False)

        with patch.object(views, "CONTACT_FORM_MIN_SECONDS", 0), patch("web.views.urllib_request.urlopen", return_value=mocked_urlopen):
            response = self.client.post(
                self._contact_url(),
                payload,
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ContactMessage.objects.count(), 0)

    @override_settings(TURNSTILE_ENABLED=True, TURNSTILE_SITE_KEY="site-key", TURNSTILE_SECRET_KEY="secret-key")
    def test_contact_form_accepts_valid_turnstile_token(self):
        payload = self._base_payload()
        payload["cf-turnstile-response"] = "valid-token"

        mocked_response = Mock()
        mocked_response.read.return_value = json.dumps({"success": True}).encode("utf-8")
        mocked_urlopen = Mock()
        mocked_urlopen.__enter__ = Mock(return_value=mocked_response)
        mocked_urlopen.__exit__ = Mock(return_value=False)

        with patch.object(views, "CONTACT_FORM_MIN_SECONDS", 0), patch("web.views.urllib_request.urlopen", return_value=mocked_urlopen):
            response = self.client.post(
                self._contact_url(),
                payload,
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)

    @override_settings(TURNSTILE_ENABLED=True, TURNSTILE_SITE_KEY="site-key", TURNSTILE_SECRET_KEY="secret-key")
    def test_contact_page_renders_turnstile_widget_when_enabled(self):
        response = self.client.get(self._contact_url())
        html = response.content.decode("utf-8")

        self.assertEqual(response.status_code, 200)
        self.assertIn("cf-turnstile", html)
        self.assertIn("site-key", html)
