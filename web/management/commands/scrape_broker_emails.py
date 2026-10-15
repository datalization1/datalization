"""E-Mail-Adressen der Immobilienfirmen von deren Websites scrapen.

Für RealEstateLead mit Website, aber ohne E-Mail: lädt Startseite + Impressum/
Kontakt und extrahiert die wahrscheinlichste E-Mail (bevorzugt Domain-gleich).
Best-effort, parallelisiert.

    python manage.py scrape_broker_emails
    python manage.py scrape_broker_emails --limit 50 --workers 12
"""
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from django.core.management.base import BaseCommand

from web.models import RealEstateLead

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
MAILTO_RE = re.compile(r'mailto:([^"\'?>\s]+)', re.I)
HEADERS = {"User-Agent": "Mozilla/5.0 (Datalization Lead-Tool; +info@datalization.ch)"}
SUBPAGES = ["", "/impressum", "/kontakt", "/de/impressum", "/de/kontakt",
            "/contact", "/datenschutz", "/ueber-uns"]
BAD = ("example.com", "sentry", "wix.com", "@2x", ".png", ".jpg", ".gif",
       "@sentry.io", "domain.com", "email@", "name@", "mail@mail")


def _domain(url):
    u = re.sub(r"^https?://", "", url.lower()).lstrip("www.")
    return u.split("/")[0]


def _clean_url(url):
    url = url.strip()
    if not url.startswith("http"):
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
    # info@/kontakt@ bevorzugen
    for pref in ("info@", "kontakt@", "office@", "mail@", "contact@"):
        for e in pool:
            if e.startswith(pref):
                return e
    return sorted(pool, key=len)[0]


def _scrape(site):
    base = _clean_url(site)
    dom = _domain(base)
    for sub in SUBPAGES:
        try:
            r = requests.get(base + sub, headers=HEADERS, timeout=8, allow_redirects=True)
            if r.status_code != 200 or "text/html" not in r.headers.get("content-type", ""):
                continue
            email = _best_email(_emails_from(r.text), dom)
            if email:
                return email
        except Exception:
            continue
    return ""


class Command(BaseCommand):
    help = "Scrapt E-Mails der Immobilienfirmen von ihren Websites."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--workers", type=int, default=12)

    def handle(self, *args, **opts):
        qs = (RealEstateLead.objects
              .exclude(website="").filter(email="")
              .exclude(website__isnull=True).order_by("pk"))
        if opts["limit"]:
            qs = qs[:opts["limit"]]
        records = list(qs)
        total = len(records)
        self.stdout.write(f"{total} Firmen mit Website, ohne E-Mail – scrape …")

        done = found = 0
        with ThreadPoolExecutor(max_workers=opts["workers"]) as ex:
            futures = {ex.submit(_scrape, r.website): r for r in records}
            batch = []
            for fut in as_completed(futures):
                r = futures[fut]
                done += 1
                email = ""
                try:
                    email = fut.result()
                except Exception:
                    email = ""
                if email:
                    r.email = email[:200]
                    batch.append(r)
                    found += 1
                if len(batch) >= 100:
                    RealEstateLead.objects.bulk_update(batch, ["email"])
                    batch = []
                if done % 100 == 0:
                    self.stdout.write(f"  … {done}/{total}, gefunden {found}", ending="\r")
                    self.stdout.flush()
            if batch:
                RealEstateLead.objects.bulk_update(batch, ["email"])
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Fertig: {found} E-Mails gefunden (von {total})."))
