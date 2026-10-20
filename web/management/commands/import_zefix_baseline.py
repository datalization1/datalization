"""Ist-Bestand ('Stand null'): alle aktiven Firmen der 17 Gemeinden des Bezirks
Zofingen aus dem Zefix-Index importieren – in dieselbe NewCompany-Tabelle wie die
Neugründungen, damit die Liste danach inkrementell mit SHAB-Neugründungen wächst.

Zefix liefert KEIN Telefon/E-Mail/Adresse – die werden danach wie bei den
Neugründungen via Google Places (Telefon/Website) + Website-Scrape (E-Mail)
angereichert:

    python manage.py import_zefix_baseline
    python manage.py enrich_google_places --towns "<17 Gemeinden>"   # Telefon/Website
    python manage.py scrape_newcompany_emails                         # E-Mail
    python manage.py push_leads_odoo --model shab                     # nach Odoo

Dedupe über UID: bereits vorhandene Firmen (auch aus SHAB) werden übersprungen.
"""
import requests
from django.core.management.base import BaseCommand, CommandError

from web import zefix
from web.models import NewCompany

BEZIRK_ZOFINGEN = [
    "Aarburg", "Bottenwil", "Brittnau", "Kirchleerau", "Kölliken", "Moosleerau",
    "Murgenthal", "Oftringen", "Reitnau", "Rothrist", "Safenwil", "Staffelbach",
    "Strengelbach", "Uerkheim", "Vordemwald", "Wiliberg", "Zofingen",
]


def _fmt_uid(uid):
    """CHE413249551 -> ('CHE413249551', 'CHE-413.249.551')."""
    u = (uid or "").upper().replace("-", "").replace(".", "").replace(" ", "")
    digits = u[3:]
    if len(digits) == 9:
        pretty = f"CHE-{digits[0:3]}.{digits[3:6]}.{digits[6:9]}"
    else:
        pretty = uid
    return u, pretty


class Command(BaseCommand):
    help = "Importiert den aktiven Firmenbestand des Bezirks Zofingen aus Zefix."

    def add_arguments(self, parser):
        parser.add_argument("--towns", default="",
                            help="Teilmenge der Gemeinden (sonst alle 17).")
        parser.add_argument("--limit", type=int, default=0,
                            help="Max. Firmen pro Gemeinde (0 = alle).")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        if not zefix.enabled():
            raise CommandError("Zefix nicht konfiguriert (ZEFIX_USERNAME/ZEFIX_PASSWORD).")
        auth = zefix._auth()
        base = zefix.BASE

        towns = ([t.strip() for t in opts["towns"].split(",") if t.strip()]
                 or BEZIRK_ZOFINGEN)

        # BFS-Nummern der Zielgemeinden aus dem Community-Index holen (Kanton AG).
        self.stdout.write("Hole Gemeinde-Index (BFS-Nummern) …")
        comms = requests.get(base + "/community", auth=auth, timeout=40).json()
        ag = {c["name"]: c["bfsId"] for c in comms if c.get("canton") == "AG"}
        bfs = {t: ag.get(t) for t in towns}
        missing = [t for t, v in bfs.items() if v is None]
        if missing:
            raise CommandError(f"Keine BFS-Nummer gefunden für: {', '.join(missing)}")

        total_seen = created = skipped = 0
        for town, seat_id in bfs.items():
            r = requests.post(base + "/company/search", auth=auth,
                              json={"legalSeatId": seat_id, "activeOnly": True,
                                    "maxEntries": 3000}, timeout=60)
            r.raise_for_status()
            rows = [c for c in r.json() if c.get("status") == "ACTIVE"]
            if opts["limit"]:
                rows = rows[:opts["limit"]]
            t_created = t_skipped = 0
            for c in rows:
                total_seen += 1
                uid_raw = c.get("uid") or ""
                uid_norm, uid_pretty = _fmt_uid(uid_raw)
                # Dedupe über UID (SHAB-Neugründung oder früherer Baseline-Lauf).
                if uid_norm and NewCompany.objects.filter(uid__in=[uid_norm, uid_pretty]).exists():
                    skipped += 1
                    t_skipped += 1
                    continue
                lf = c.get("legalForm") or {}
                legal_form = (lf.get("shortName") or {}).get("de") or \
                             (lf.get("name") or {}).get("de", "")
                data = {
                    "shab_id": f"zefix:{uid_norm or c.get('ehraid')}",
                    "name": c.get("name", "")[:255],
                    "uid": uid_norm,
                    "legal_form": legal_form[:120],
                    "seat": c.get("legalSeat", "")[:120],
                    "town": c.get("legalSeat", "")[:120],
                    "canton": "AG",
                    "zefix_status": "ACTIVE",
                    "zefix_url": f"https://www.zefix.admin.ch/de/search/entity/list?name={uid_norm}&directLink=true",
                    "zefix_excerpt_url": f"https://ag.chregister.ch/cr-portal/auszug/auszug.xhtml?uid={uid_pretty}",
                    "notes": "Bestand Bezirk Zofingen (Zefix-Index)",
                    "status": "new",
                }
                if not opts["dry_run"]:
                    NewCompany.objects.create(**data)
                created += 1
                t_created += 1
            self.stdout.write(f"  {town:14} aktiv {len(rows):4}  neu {t_created:4}  "
                              f"übersprungen {t_skipped:4}")

        verb = "würde importieren" if opts["dry_run"] else "importiert"
        self.stdout.write(self.style.SUCCESS(
            f"\nAktiv gesehen: {total_seen} | {verb}: {created} | übersprungen (schon vorhanden): {skipped}"))
        if opts["dry_run"]:
            self.stdout.write("(dry-run – nichts gespeichert)")
