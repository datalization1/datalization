from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

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
            "v2:monekey",
            "v2:odoo_partner",
            "v2:ueber_datalization",
            "v2:kontakt",
            "v2:seo_erp_kmu",
            "v2:seo_buchhaltung",
            "v2:seo_treuhand",
            "v2:seo_handwerk",
            "v2:seo_olten",
        ]

    def location(self, item):
        return reverse(item)
