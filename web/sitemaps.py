from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CaseStudy

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    def items(self):
        return ["web:home","web:about","web:services","web:cases","web:contact"]
    def location(self, item):
        return reverse(item)

class CaseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    def items(self):
        return CaseStudy.objects.filter(published=True)
    def lastmod(self, obj):
        return obj.date
