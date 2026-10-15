"""Zefix REST API (Handelsregister-Index) – Lookup/Anreicherung.

Aktiv, sobald ZEFIX_USERNAME/ZEFIX_PASSWORD gesetzt sind. Liefert offizielle
Firmendaten (Status, Rechtsform, Kanton, Zefix-Link, HR-Auszug-Link).
Kein Telefon/keine E-Mail (nicht im Handelsregister enthalten).
"""
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

BASE = "https://www.zefix.admin.ch/ZefixPublicREST/api/v1"


def _auth():
    u = getattr(settings, "ZEFIX_USERNAME", "")
    p = getattr(settings, "ZEFIX_PASSWORD", "")
    return HTTPBasicAuth(u, p) if u and p else None


def enabled():
    return _auth() is not None


def _norm_uid(uid):
    return (uid or "").upper().replace("CHE-", "CHE").replace(".", "").replace("-", "").replace(" ", "")


def by_uid(uid, timeout=20):
    """Firmendetails per UID. Gibt ein dict zurück oder None."""
    auth = _auth()
    if not auth or not uid:
        return None
    try:
        r = requests.get(f"{BASE}/company/uid/{_norm_uid(uid)}", auth=auth, timeout=timeout)
        if r.status_code != 200:
            return None
        d = r.json()
        rec = d[0] if isinstance(d, list) and d else (d if isinstance(d, dict) else None)
        if not rec:
            return None
        lf = rec.get("legalForm") or {}
        return {
            "name": rec.get("name", ""),
            "status": rec.get("status", ""),
            "canton": rec.get("canton", ""),
            "legal_form_short": (lf.get("shortName") or {}).get("de", ""),
            "zefix_url": (rec.get("zefixDetailWeb") or {}).get("de", ""),
            "excerpt_url": rec.get("cantonalExcerptWeb", ""),
        }
    except Exception:
        return None
