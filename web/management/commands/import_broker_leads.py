"""Importiert Immobilien-/Maklerfirmen (Monekey-Leads) aus der Maklerliste.

Die Quelldatei mischt zwei Layouts (immoscout = 11 Spalten, homegate = 12
Spalten mit zusätzlicher Kanton-Spalte) und enthält dieselbe Firma oft doppelt
– einmal je Marktplatz, aber mit identischer `id`. Deduplizierung erfolgt über
diese `id`; die Datensätze werden zusammengeführt (fehlende Felder aus der
jeweils anderen Quelle ergänzt).

Unterstützt .ods (via odfpy) und .csv.

    python manage.py import_broker_leads "/pfad/Maklerliste 2.csv"
    python manage.py import_broker_leads <datei> --dry-run
"""
import csv
import re

from django.core.management.base import BaseCommand, CommandError

from web.models import RealEstateLead


def _clean(v):
    v = (v or "").replace("\n", " ").strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':   # CSV-Quote-Artefakte
        v = v[1:-1]
    return v.replace('""', '"').strip()


def _first_line(v):
    return (v or "").split("\n")[0].strip()


class Command(BaseCommand):
    help = "Importiert Immobilienfirmen (Monekey-Leads) aus einer Maklerliste (.ods/.csv)."

    def add_arguments(self, parser):
        parser.add_argument("path", help="Pfad zur Maklerliste (.ods oder .csv)")
        parser.add_argument("--dry-run", action="store_true",
                            help="Nur zählen, nichts speichern.")

    def handle(self, *args, **opts):
        path = opts["path"]
        rows = self._read(path)
        if not rows:
            raise CommandError("Keine Datenzeilen gelesen.")

        merged = {}
        for r in rows:
            rec = self._parse(r)
            if not rec or not rec["id"]:
                continue
            cur = merged.get(rec["id"])
            if cur is None:
                merged[rec["id"]] = rec
            else:
                # fehlende Felder ergänzen; Quellen sammeln
                for k, v in rec.items():
                    if k == "sources":
                        cur["sources"] |= v
                    elif not cur.get(k) and v:
                        cur[k] = v

        self.stdout.write(f"Zeilen: {len(rows)}, eindeutige Firmen: {len(merged)}")

        created = updated = 0
        if not opts["dry_run"]:
            for ext_id, m in merged.items():
                obj, is_new = RealEstateLead.objects.update_or_create(
                    external_id=ext_id,
                    defaults={
                        "name": m["name"][:255],
                        "zip_code": m["postal"][:10],
                        "city": m["city"][:120],
                        "street": m["street"][:200],
                        "full_address": m["full"][:300],
                        "website": m["website"][:300],
                        "phone": m["tel"][:60],
                        "email": m["email"][:200],
                        "source_url": m["source_url"][:400],
                        "marketplace": ",".join(sorted(m["sources"]))[:40],
                    },
                )
                created += is_new
                updated += (not is_new)
            self.stdout.write(self.style.SUCCESS(
                f"Importiert: {created} neu, {updated} aktualisiert. "
                f"Total in DB: {RealEstateLead.objects.count()}"))
        else:
            with_web = sum(1 for m in merged.values() if m["website"].startswith("http"))
            with_tel = sum(1 for m in merged.values() if m["tel"])
            self.stdout.write(f"DRY-RUN: {len(merged)} Firmen "
                              f"({with_web} mit Website, {with_tel} mit Telefon). "
                              f"Nichts gespeichert.")

    # ---- Parsing ----------------------------------------------------------
    def _parse(self, r):
        link = (r[0] if r else "").strip()
        g = lambda i: _clean(r[i]) if i < len(r) else ""
        if "homegate" in link:          # 12 Spalten: ... city, KANTON, street, ...
            rec = dict(id=g(1), name=g(2), postal=g(3), city=g(4),
                       street=g(6), full=g(7), website=g(8), tel=g(9), email=g(10),
                       source_url=link, sources={"homegate"})
        else:                            # immoscout: 11 Spalten
            rec = dict(id=g(1), name=g(2), postal=g(3), city=g(4),
                       street=g(5), full=g(6), website=g(7), tel=g(8), email=g(9),
                       source_url=link, sources={"immoscout"})
        rec["tel"] = _first_line(rec["tel"])
        rec["email"] = _first_line(rec["email"])
        if not rec["website"].startswith("http"):
            rec["website"] = ""         # verschobene/ungültige Werte verwerfen
        return rec

    def _read(self, path):
        if path.lower().endswith(".csv") and not self._is_zip(path):
            with open(path, newline="", encoding="utf-8-sig") as f:
                return [row for row in csv.reader(f)]
        # sonst als ODS behandeln
        try:
            from odf.opendocument import load
            from odf.table import Table, TableRow, TableCell
            from odf.text import P
        except ImportError:
            raise CommandError("odfpy fehlt – bitte `pip install odfpy` (für .ods).")
        doc = load(path)
        tbl = doc.spreadsheet.getElementsByType(Table)[0]

        def cv(c):
            return "\n".join(str(p) for p in c.getElementsByType(P)).strip()

        out = []
        for tr in tbl.getElementsByType(TableRow):
            cells = []
            for c in tr.getElementsByType(TableCell):
                rep = min(int(c.getAttribute("numbercolumnsrepeated") or 1), 50)
                cells.extend([cv(c)] * rep)
            while cells and cells[-1] == "":
                cells.pop()
            if cells:
                out.append(cells)
        return out[1:]  # Kopfzeile weg

    @staticmethod
    def _is_zip(path):
        try:
            with open(path, "rb") as f:
                return f.read(2) == b"PK"
        except OSError:
            return False
