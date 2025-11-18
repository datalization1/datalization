from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # Deine benannten URLs
        return [
            "web:home",
            "web:services",
            "web:cases",
            "web:about",
            "web:contact",
        ]

    def location(self, item):
        return reverse(item)