from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import CaseStudy


class StaticViewSitemap(Sitemap):
    """Feste Seiten. i18n=True erzeugt je Sprache einen Eintrag (/de/… und /en/…),
    alternates=True ergaenzt die hreflang-Verweise zwischen den Sprachfassungen."""

    changefreq = "monthly"
    protocol = "https"
    i18n = True
    alternates = True
    x_default = True

    # Startseite wichtiger als der Rest
    PRIORITIES = {
        "web:home": 1.0,
        "web:services": 0.9,
        "web:service_it_support": 0.9,
        "web:monekey": 0.9,
    }

    def items(self):
        return [
            "web:home",
            "web:services",
            "web:service_it_support",
            "web:service_data_analytics",
            "web:service_software",
            "web:service_digitalisierung",
            "web:service_beratung",
            "web:monekey",
            "web:cases",
            "web:about",
            "web:contact",
            "web:booking",
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PRIORITIES.get(item, 0.7)


class CaseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"
    i18n = True
    alternates = True
    x_default = True

    def items(self):
        return CaseStudy.objects.filter(published=True)

    def location(self, obj):
        return reverse("web:case_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj):
        return obj.date
