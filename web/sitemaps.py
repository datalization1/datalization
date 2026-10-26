from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Feste Seiten. i18n=True erzeugt je Sprache einen Eintrag (/de/… und /en/…),
    alternates=True ergaenzt die hreflang-Verweise zwischen den Sprachfassungen."""

    changefreq = "monthly"
    protocol = "https"
    i18n = True
    alternates = True
    x_default = True

    # Startseite wichtiger als der Rest; Rechtstexte gehoeren in den Index
    # (belegen eine reale Firma), brauchen aber kein Gewicht.
    PRIORITIES = {
        "v2:home": 1.0,
        "v2:odoo": 0.9,
        "v2:data_analytics": 0.9,
        "v2:digitalisierung": 0.9,
        "v2:softwareentwicklung": 0.9,
        "v2:monekey": 0.9,
        "v2:odoo_partner": 0.9,
        "v2:impressum": 0.3,
        "v2:datenschutz": 0.3,
    }

    def items(self):
        # Website v2.0 ist die produktive Seite – nur die öffentlichen v2-Seiten.
        return [
            "v2:home",
            "v2:odoo",
            "v2:odoo_wieso",
            "v2:odoo_einfuehrung",
            "v2:odoo_vergleich",
            "v2:data_analytics",
            "v2:digitalisierung",
            "v2:softwareentwicklung",
            "v2:monekey",
            "v2:odoo_partner",
            "v2:ueber_datalization",
            "v2:kontakt",
            "v2:seo_erp_kmu",
            "v2:seo_buchhaltung",
            "v2:seo_treuhand",
            "v2:seo_handwerk",
            "v2:seo_olten",
            "v2:impressum",
            "v2:datenschutz",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PRIORITIES.get(item, 0.7)
