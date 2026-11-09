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
import json
from pathlib import Path

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import get_language
from django.views.generic import RedirectView

from web.sitemaps import StaticViewSitemap

sitemaps = {"static": StaticViewSitemap}
ICON_DIR = Path(__file__).resolve().parent.parent / "web" / "static" / "img"

def robots_txt(request):
    # Die Sitemap-Zeile muss laut Spezifikation eine absolute URL sein.
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    return HttpResponse(
        "User-agent: *\n"
        "Allow: /\n"
        # Interne v1-Admin-Oberfläche nicht indexieren lassen.
        "Disallow: /custom-admin/\n"
        "Disallow: /*/custom-admin/\n"
        f"Sitemap: {sitemap_url}\n",
        content_type="text/plain",
    )


def serve_icon(filename, content_type):
    path = ICON_DIR / filename
    if not path.exists():
        raise Http404(f"{filename} not found")
    return FileResponse(path.open("rb"), content_type=content_type)


def favicon_ico(_):
    return serve_icon("favicon.ico", "image/x-icon")


def favicon_png(_):
    return serve_icon("favicon-48.png", "image/png")


def site_icon_svg(_):
    return serve_icon("site-icon.svg", "image/svg+xml")


def apple_touch_icon(_):
    return serve_icon("apple-touch-icon.png", "image/png")


def icon_192(_):
    return serve_icon("icon-192.png", "image/png")


def icon_512(_):
    return serve_icon("icon-512.png", "image/png")


def site_webmanifest(_):
    manifest = {
        "name": "datalization",
        "short_name": "datalization",
        "lang": "de-CH",
        "start_url": "/de/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#ffffff",
        "icons": [
            {
                "src": "/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
            },
            {
                "src": "/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
            },
        ],
    }
    return HttpResponse(
        json.dumps(manifest),
        content_type="application/manifest+json",
    )

# Root ohne Sprachpräfix -> dauerhaft (301) auf die Standardsprache umleiten,
# damit Google die /de/-Startseite eindeutig als kanonisch konsolidiert.
# Ein 301 muss stabil sein -> feste Standardsprache statt der je Request
# wechselnden get_language()-Fassung verwenden.
def redirect_to_lang_root(request):
    return redirect(f"/{settings.LANGUAGE_CODE}/", permanent=True)


# Alte /v2/-Vorschaulinks und /cases/<slug>/ dauerhaft auf den neuen Root
# (v2:home) umleiten. Eigene Funktion statt RedirectView, damit der gefangene
# Rest-Pfad bzw. slug NICHT an reverse('v2:home') weitergereicht wird – das
# würde NoReverseMatch (HTTP 500) auslösen.
def redirect_v2_legacy(request, **kwargs):
    return redirect("v2:home", permanent=True)

urlpatterns = [
    path("", redirect_to_lang_root, name="root"),                 # <— Fix für 404 auf /
    path("robots.txt", robots_txt),
    path("favicon.ico", favicon_ico, name="favicon_ico"),
    path("favicon-48.png", favicon_png, name="favicon_png"),
    path("site-icon.svg", site_icon_svg, name="site_icon_svg"),
    path("apple-touch-icon.png", apple_touch_icon, name="apple_touch_icon"),
    path("icon-192.png", icon_192, name="icon_192"),
    path("icon-512.png", icon_512, name="icon_512"),
    path("site.webmanifest", site_webmanifest, name="site_webmanifest"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("i18n/", include("django.conf.urls.i18n")),             # set_language etc.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    # Website v2.0 ist seit dem Go-live die produktive Seite am Root.
    path("", include(("web.urls_v2", "v2"), namespace="v2")),

    # 301-Weiterleitungen der abgelösten v1-Seiten auf das passende v2-Pendant.
    path("about/", RedirectView.as_view(pattern_name="v2:ueber_datalization", permanent=True)),
    path("contact/", RedirectView.as_view(pattern_name="v2:kontakt", permanent=True)),
    path("services/", RedirectView.as_view(pattern_name="v2:home", permanent=True)),
    path("services/it-support/", RedirectView.as_view(pattern_name="v2:digitalisierung", permanent=True)),
    path("services/data-analytics/", RedirectView.as_view(pattern_name="v2:data_analytics", permanent=True)),
    path("services/softwareentwicklung/", RedirectView.as_view(pattern_name="v2:digitalisierung", permanent=True)),
    path("services/digitalisierung/", RedirectView.as_view(pattern_name="v2:digitalisierung", permanent=True)),
    path("services/beratung-strategie/", RedirectView.as_view(pattern_name="v2:home", permanent=True)),
    path("start/", RedirectView.as_view(pattern_name="v2:kontakt", permanent=True)),
    path("match/", RedirectView.as_view(pattern_name="v2:home", permanent=True)),
    path("cases/", RedirectView.as_view(pattern_name="v2:home", permanent=True)),
    # <slug> bewusst an redirect_v2_legacy (verwirft den slug) statt RedirectView:
    path("cases/<slug:slug>/", redirect_v2_legacy),

    # Alte /v2/-Vorschaulinks dauerhaft auf den neuen Root umleiten.
    path("v2/", redirect_v2_legacy),
    path("v2/<path:rest>", redirect_v2_legacy),

    # v1 bleibt eingehängt für das interne custom_admin + web:-Namespace-Reverses;
    # die öffentlichen Alt-Seiten sind oben bereits per 301 abgefangen.
    path("", include(("web.urls", "web"), namespace="web")),

    path("admin/", admin.site.urls),
)
