"""Exportiert SHAB-Neugründungen als Excel-Datei (für Weitergabe / FC Oftringen).

    python manage.py export_newcompanies --out ~/Downloads/Neugruendungen.xlsx
    python manage.py export_newcompanies --bezirk-zofingen --active-only \
        --out ~/Downloads/Neugruendungen_Bezirk_Zofingen.xlsx
"""
import os

from django.core.management.base import BaseCommand

from web.models import NewCompany

BEZIRK_ZOFINGEN = [
    "Aarburg", "Bottenwil", "Brittnau", "Kirchleerau", "Kölliken", "Moosleerau",
    "Murgenthal", "Oftringen", "Reitnau", "Rothrist", "Safenwil", "Staffelbach",
    "Strengelbach", "Uerkheim", "Vordemwald", "Wiliberg", "Zofingen",
]

# Generische Firmen-Postfächer (keine natürliche Person erkennbar)
GENERIC_PREFIXES = (
    "info@", "kontakt@", "contact@", "office@", "mail@", "admin@", "hello@",
    "welcome@", "sales@", "support@", "mailbox@", "empfang@", "sekretariat@",
    "buchhaltung@", "praxis@", "team@", "post@", "verkauf@", "anfrage@",
)


def contact_risk(r):
    """Kontakt-Risiko für Massenmail (UWG/revDSG).

    🔴 Person        – Einzelunternehmen ODER persönliche Adresse → kein Massenmail
    🟡 Firma generisch – AG/GmbH mit info@/kontakt@ → Grauzone, nur personalisiert
    ⚪ keine E-Mail   – nur Telefon/Brief möglich
    """
    email = (r.email or "").lower().strip()
    if not email:
        return "⚪ keine E-Mail"
    is_einzel = "einzel" in (r.legal_form or "").lower()
    is_generic = email.startswith(GENERIC_PREFIXES)
    if is_einzel or not is_generic:
        return "🔴 Person"
    return "🟡 Firma generisch"


COLUMNS = [
    ("Kontakt-Risiko", contact_risk),
    ("Firma", "name"),
    ("Rechtsform", "legal_form"),
    ("Strasse", lambda r: " ".join(x for x in [r.street, r.house_number] if x)),
    ("PLZ", "zip_code"),
    ("Ort", "town"),
    ("Kontaktperson", "contact_person"),
    ("Telefon", "phone"),
    ("E-Mail", "email"),
    ("Website", "website"),
    ("Gründungsdatum", lambda r: r.publication_date.strftime("%d.%m.%Y")
     if hasattr(r.publication_date, "strftime") else (r.publication_date or "")),
    ("UID", "uid"),
    ("Register-Status", "zefix_status"),
    ("Zefix", "zefix_url"),
    ("HR-Auszug", "zefix_excerpt_url"),
]


class Command(BaseCommand):
    help = "Exportiert NewCompany-Datensätze als Excel (.xlsx)."

    def add_arguments(self, parser):
        parser.add_argument("--out", required=True, help="Zielpfad der .xlsx-Datei.")
        parser.add_argument("--towns", default="", help="Komma-Liste von Orten.")
        parser.add_argument("--bezirk-zofingen", action="store_true",
                            help="Nur die 17 Gemeinden des Bezirks Zofingen.")
        parser.add_argument("--active-only", action="store_true",
                            help="Nur Register-Status ACTIVE.")
        parser.add_argument("--risk", choices=["person", "firma", "nomail", "mailbar"],
                            default="",
                            help="Filter nach Kontakt-Risiko: person (🔴), "
                                 "firma (🟡 generisch), nomail (⚪), "
                                 "mailbar (nur 🟡 generische Firmenadressen).")

    def handle(self, *args, **opts):
        from openpyxl import Workbook
        from openpyxl.styles import Font

        qs = NewCompany.objects.all()
        towns = []
        if opts["bezirk_zofingen"]:
            towns = BEZIRK_ZOFINGEN
        elif opts["towns"]:
            towns = [t.strip() for t in opts["towns"].split(",") if t.strip()]
        if towns:
            qs = qs.filter(town__in=towns)
        if opts["active_only"]:
            qs = qs.filter(zefix_status="ACTIVE")
        qs = qs.order_by("town", "name")

        # Risiko-Filter (in Python, da zusammengesetzte Logik)
        risk = opts["risk"]
        want = {"person": "🔴 Person", "firma": "🟡 Firma generisch",
                "mailbar": "🟡 Firma generisch", "nomail": "⚪ keine E-Mail"}.get(risk)
        records = [r for r in qs if (not want or contact_risk(r) == want)]

        wb = Workbook()
        ws = wb.active
        ws.title = "Neugründungen"
        ws.append([c[0] for c in COLUMNS])
        for cell in ws[1]:
            cell.font = Font(bold=True)
        ws.freeze_panes = "A2"

        n = 0
        for r in records:
            row = []
            for _, accessor in COLUMNS:
                val = accessor(r) if callable(accessor) else getattr(r, accessor, "")
                row.append(val or "")
            ws.append(row)
            n += 1

        # Spaltenbreiten grob setzen
        for i, (header, _) in enumerate(COLUMNS, start=1):
            width = max(len(header) + 2, 14)
            if header in ("Firma", "E-Mail", "Website", "Zefix", "HR-Auszug", "Strasse"):
                width = 32
            ws.column_dimensions[chr(64 + i) if i <= 26 else "A"].width = width

        out = os.path.expanduser(opts["out"])
        wb.save(out)
        self.stdout.write(self.style.SUCCESS(f"{n} Firmen exportiert → {out}"))
