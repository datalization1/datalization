"""
Template-Tags für die Website v2.0.

alt_url: liefert für die aktuelle Seite die sprachabhängige Variante (DE/EN)
inkl. getauschtem URL-Präfix (/de/ <-> /en/) – für hreflang-Tags.
"""
from django import template
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def alt_url(context, lang):
    """Absoluter Pfad der aktuellen Seite in der Zielsprache (nur Pfad, kein Host)."""
    request = context.get("request")
    if request is None:
        return ""
    return translate_url(request.get_full_path(), lang)
