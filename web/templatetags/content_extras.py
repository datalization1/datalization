"""Template-Tags für editierbare Inhalts-Blöcke (CMS-lite).

Nutzung im Template:
    {% load content_extras %}
    {% content_block "home_hero_title" "Fallback-Text" %}
    {% content_block_image "home_hero" as hero_url %}
"""
from django import template

from web.models import ContentBlock

register = template.Library()


@register.simple_tag
def content_block(key, default=""):
    """Lokalisierten Text eines Inhalts-Blocks (DE/EN); Fallback wenn leer/fehlt."""
    block = ContentBlock.objects.filter(key=key).first()
    if not block:
        return default
    return block.localized() or default


@register.simple_tag
def content_block_image(key, default=""):
    """Bild-URL eines Inhalts-Blocks (leer, wenn keins hinterlegt)."""
    block = ContentBlock.objects.filter(key=key).first()
    if block and block.image:
        try:
            return block.image.url
        except Exception:  # noqa: BLE001
            return default
    return default
