"""
URL configuration for datalization_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import get_language

from web.sitemaps import StaticViewSitemap, CaseSitemap

sitemaps = {"static": StaticViewSitemap, "cases": CaseSitemap}

def robots_txt(_):
    return HttpResponse("User-agent: *\nAllow: /\nSitemap: /sitemap.xml", content_type="text/plain")

# Root ohne Sprachpräfix -> auf aktuelle Sprache umleiten
def redirect_to_lang_root(request):
    lang = get_language() or "de"
    return redirect(f"/{lang}/", permanent=False)

urlpatterns = [
    path("", redirect_to_lang_root, name="root"),                 # <— Fix für 404 auf /
    path("robots.txt", robots_txt),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("i18n/", include("django.conf.urls.i18n")),             # set_language etc.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("", include(("web.urls", "web"), namespace="web")),     # <— Namespace sauber
    path("admin/", admin.site.urls),
)