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

from web.sitemaps import StaticViewSitemap, CaseSitemap

sitemaps = {"static": StaticViewSitemap, "cases": CaseSitemap}
ICON_DIR = Path(__file__).resolve().parent.parent / "web" / "static" / "img"

def robots_txt(_):
    return HttpResponse("User-agent: *\nAllow: /\nSitemap: /sitemap.xml", content_type="text/plain")


def serve_icon(filename, content_type):
    path = ICON_DIR / filename
    if not path.exists():
        raise Http404(f"{filename} not found")
    return FileResponse(path.open("rb"), content_type=content_type)


def favicon_ico(_):
    return serve_icon("favicon-48.png", "image/png")


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
        "background_color": "#0a0a0a",
        "theme_color": "#0a0a0a",
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

# Root ohne Sprachpräfix -> auf aktuelle Sprache umleiten
def redirect_to_lang_root(request):
    lang = get_language() or "de"
    return redirect(f"/{lang}/", permanent=False)

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
    path("", include(("web.urls", "web"), namespace="web")),     # <— Namespace sauber
    path("admin/", admin.site.urls),
)
