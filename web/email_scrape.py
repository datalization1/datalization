"""Gemeinsame E-Mail-Scrape-Logik (Impressum/Kontakt einer Firmen-Website)."""
import re
import requests

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
MAILTO_RE = re.compile(r'mailto:([^"\'?>\s]+)', re.I)
HEADERS = {"User-Agent": "Mozilla/5.0 (Datalization Lead-Tool; +info@datalization.ch)"}
SUBPAGES = ["", "/impressum", "/kontakt", "/de/impressum", "/de/kontakt",
            "/contact", "/datenschutz", "/ueber-uns"]
BAD = ("example.com", "sentry", "wix.com", "@2x", ".png", ".jpg", ".gif",
       "@sentry.io", "domain.com", "email@", "name@", "mail@mail")


def domain(url):
    u = re.sub(r"^https?://", "", (url or "").lower()).lstrip("www.")
    return u.split("/")[0]


def clean_url(url):
    url = (url or "").strip()
    if url and not url.startswith("http"):
        url = "http://" + url
    return url.rstrip("/")


def _emails_from(html):
    found = set()
    for m in MAILTO_RE.findall(html):
        found.add(m.split("?")[0].strip().lower())
    for m in EMAIL_RE.findall(html):
        found.add(m.strip().lower())
    return {e for e in found if e and not any(b in e for b in BAD)
            and not e.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"))}


def _best_email(emails, site_domain):
    if not emails:
        return ""
    same = [e for e in emails if e.split("@")[-1] == site_domain]
    pool = same or list(emails)
    for pref in ("info@", "kontakt@", "office@", "mail@", "contact@"):
        for e in pool:
            if e.startswith(pref):
                return e
    return sorted(pool, key=len)[0]


def scrape_site(site, timeout=8):
    """Durchsucht Startseite + Impressum/Kontakt und gibt die beste E-Mail zurück."""
    base = clean_url(site)
    if not base:
        return ""
    dom = domain(base)
    for sub in SUBPAGES:
        try:
            r = requests.get(base + sub, headers=HEADERS, timeout=timeout, allow_redirects=True)
            if r.status_code != 200 or "text/html" not in r.headers.get("content-type", ""):
                continue
            email = _best_email(_emails_from(r.text), dom)
            if email:
                return email
        except Exception:
            continue
    return ""
