"""Sprachalternativen fuer die hreflang-Angaben im Seitenkopf."""

import re

from django.conf import settings
from django.urls import translate_url

_LANG_PREFIX = re.compile(
    r"^/(?:%s)(/|$)" % "|".join(re.escape(code) for code, _ in settings.LANGUAGES)
)


def hreflang(request):
    """Liefert je Sprache die Adresse derselben Seite plus x-default.

    x-default zeigt auf die Adresse ohne Sprachpraefix. Django leitet die per
    LocaleMiddleware auf die passende Sprachfassung weiter - genau das, was
    Google unter einer sprachneutralen Einstiegsadresse versteht.
    """
    path = getattr(request, "path", "") or ""
    if not path.startswith("/") or _LANG_PREFIX.match(path) is None:
        return {}

    alternates = []
    for code, _name in settings.LANGUAGES:
        try:
            url = translate_url(path, code)
        except Exception:
            continue
        alternates.append({"code": code, "url": request.build_absolute_uri(url)})

    neutral = _LANG_PREFIX.sub(r"\1", path) or "/"
    return {
        "hreflang_alternates": alternates,
        "hreflang_x_default": request.build_absolute_uri(neutral),
    }


def site_verification(request):
    """Bestaetigungscode der Google Search Console fuer den Seitenkopf."""
    token = getattr(settings, "GOOGLE_SITE_VERIFICATION", "")
    return {"google_site_verification": token} if token else {}
