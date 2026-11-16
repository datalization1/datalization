"""Projekt-Middleware.

PermanentLocaleMiddleware: wie Djangos LocaleMiddleware, aber der Sprachpräfix-
Redirect (z. B. /kontakt/ -> /de/kontakt/) ist 301 (permanent) statt 302
(temporär). SEO: 301 signalisiert Google den dauerhaften Umzug, die nicht-
präfixierte URL wird konsolidiert statt im „Seite mit Weiterleitung"-Limbo zu
hängen. Die übrigen Redirects (non-www->www, Root, alte v1-Pfade) sind bereits 301.
"""
from django.http import HttpResponsePermanentRedirect
from django.middleware.locale import LocaleMiddleware


class PermanentLocaleMiddleware(LocaleMiddleware):
    response_redirect_class = HttpResponsePermanentRedirect
