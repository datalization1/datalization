"""SEO: der Sprachpräfix-Redirect muss 301 (permanent) sein, nicht 302.

Siehe datalization_site/middleware.PermanentLocaleMiddleware. Ein 302 hielt
nicht-präfixierte URLs in der Search Console im „Seite mit Weiterleitung"-Limbo.
"""
from django.test import TestCase


class LocaleRedirectIsPermanentTests(TestCase):
    def test_nonprefixed_urls_redirect_301_to_de(self):
        for path, target in [
            ("/kontakt/", "/de/kontakt/"),
            ("/odoo/vergleich/", "/de/odoo/vergleich/"),
            ("/data-analytics/", "/de/data-analytics/"),
        ]:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 301, f"{path} sollte 301 sein")
            self.assertEqual(resp.headers.get("Location"), target)
