"""Google Places API (New) – Telefon/Website-Anreicherung per Textsuche.

Aktiv, sobald GOOGLE_PLACES_API_KEY gesetzt ist. Liefert kein E-Mail.
"""
import requests
from django.conf import settings

URL = "https://places.googleapis.com/v1/places:searchText"
FIELDS = ("places.displayName,places.nationalPhoneNumber,"
          "places.internationalPhoneNumber,places.websiteUri,places.formattedAddress")


def enabled():
    return bool(getattr(settings, "GOOGLE_PLACES_API_KEY", ""))


def lookup(query, timeout=20):
    """Erste passende Firma zu einer Textsuche. Gibt dict oder None."""
    key = getattr(settings, "GOOGLE_PLACES_API_KEY", "")
    if not key or not query:
        return None
    headers = {"Content-Type": "application/json", "X-Goog-Api-Key": key,
               "X-Goog-FieldMask": FIELDS}
    body = {"textQuery": query, "regionCode": "CH", "languageCode": "de",
            "maxResultCount": 1}
    try:
        r = requests.post(URL, json=body, headers=headers, timeout=timeout)
        if r.status_code != 200:
            return {"error": f"{r.status_code}: {r.text[:200]}"}
        places = r.json().get("places") or []
        if not places:
            return None
        p = places[0]
        return {
            "name": (p.get("displayName") or {}).get("text", ""),
            "phone": p.get("nationalPhoneNumber") or p.get("internationalPhoneNumber") or "",
            "website": p.get("websiteUri") or "",
            "address": p.get("formattedAddress", ""),
        }
    except Exception as e:
        return {"error": str(e)[:200]}
