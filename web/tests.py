from django.test import TestCase
from datetime import date

from .models import CaseStudy


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
