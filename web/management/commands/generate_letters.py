"""Erzeugt druckfertige Serienbriefe (A4, Schweizer Fensterkuvert) für
Neugründungen OHNE E-Mail – zum Ausdrucken, von Hand unterschreiben und mit
beigelegter Visitenkarte versenden.

Ausgabe ist EINE HTML-Datei, ein Brief pro A4-Seite. Im Browser öffnen →
⌘P → 'Als PDF sichern' oder direkt drucken (Ränder: 'Keine'/Standard).

    python manage.py generate_letters
    python manage.py generate_letters --bezirk-zofingen
    python manage.py generate_letters --limit 3   # Testlauf
"""
import os

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from web import odoo_crm
from web.models import NewCompany

SENT_TAG = "Brief versendet"
LEGAL_RANK = [("aktien", 3), ("gmbh", 2), ("kollektiv", 2)]  # Rest = 1

BEZIRK_ZOFINGEN = [
    "Aarburg", "Bottenwil", "Brittnau", "Kirchleerau", "Kölliken", "Moosleerau",
    "Murgenthal", "Oftringen", "Reitnau", "Rothrist", "Safenwil", "Staffelbach",
    "Strengelbach", "Uerkheim", "Vordemwald", "Wiliberg", "Zofingen",
]
MONTHS = ["", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
          "August", "September", "Oktober", "November", "Dezember"]
LOGO_URL = "https://datalization.ch/static/email/datalization-email-logo.png"


def esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


PAGE_CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Arial, Helvetica, sans-serif; color: #000; }
.letter {
  position: relative; width: 210mm; min-height: 297mm;
  padding: 18mm 20mm 16mm 25mm; page-break-after: always;
  font-size: 11pt; line-height: 1.5;
}
.letter:last-child { page-break-after: auto; }
.head { display: flex; justify-content: flex-end; align-items: center; gap: 10px; }
.head img { width: 40px; height: auto; display: block; }
.head .wm { text-align: right; font-size: 10pt; line-height: 1.3; }
.head .wm b { font-size: 13pt; }
.head .wm .slogan { color: #F48B2D; font-weight: bold; font-size: 9pt;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.sender-line { position: absolute; top: 42mm; left: 25mm;
  font-size: 7pt; color: #555; }
.address { position: absolute; top: 46mm; left: 25mm; font-size: 11pt; line-height: 1.4; }
.content { margin-top: 62mm; }
.date { text-align: right; margin-bottom: 10mm; }
.subject { font-weight: bold; margin-bottom: 6mm; }
.content p { margin: 0 0 3mm 0; }
.content ul { margin: 3mm 0; padding-left: 6mm; }
.content li { margin-bottom: 1mm; }
.sign-space { height: 18mm; }
.enclosure { margin-top: 8mm; font-size: 10pt; }
.footer { position: absolute; bottom: 10mm; left: 25mm; right: 20mm;
  border-top: 1px solid #ccc; padding-top: 2mm;
  font-size: 8pt; color: #666; text-align: center; }
"""


def render_letter(r, datum):
    street = " ".join(x for x in [r.street, r.house_number] if x).strip()
    firma = esc(r.name)
    return f"""
<div class="letter">
  <div class="head">
    <img src="{LOGO_URL}" alt="Datalization">
    <div class="wm"><b>Datalization</b><br>
      <span class="slogan">Einfache Lösungen schaffen.</span></div>
  </div>

  <div class="sender-line">Datalization · Bärengasse 3 · 4800 Zofingen</div>
  <div class="address">
    {firma}<br>
    {esc(street)}<br>
    {esc(r.zip_code)} {esc(r.town)}
  </div>

  <div class="content">
    <div class="date">Zofingen, {datum}</div>
    <div class="subject">Herzlichen Glückwunsch zur Gründung – und ein Angebot für Ihren Start</div>

    <p>Sehr geehrte Damen und Herren</p>
    <p>herzlichen Glückwunsch zur Gründung von <b>{firma}</b>. Wir haben Ihren Eintrag im
       Handelsregister (SHAB) gesehen und wünschen Ihnen einen erfolgreichen Start.</p>
    <p>Wir sind <b>Datalization</b> aus Zofingen und bauen für kleine Betriebe die ganze
       digitale Basis auf – von der IT bis zu den Abläufen:</p>
    <ul>
      <li>Komplette <b>IT aus einer Hand</b>: Hardware, Software-Lizenzen, Einrichtung und
          laufender Betrieb (<b>Managed IT</b>)</li>
      <li>Offerten, Rechnungen und Buchhaltung ohne Zettelwirtschaft</li>
      <li>Kundenverwaltung (CRM) – häufig mit <b>Odoo</b></li>
      <li>wiederkehrende Abläufe automatisieren – mehr Zeit fürs Kerngeschäft</li>
    </ul>
    <p>Gerade am Anfang spart ein durchdachtes Setup später viel Zeit und Ärger. Gerne zeigen
       wir Ihnen in einem <b>kostenlosen 30-minütigen Erstgespräch</b> unverbindlich, was für
       Ihren Betrieb sinnvoll ist – rufen Sie uns an (076 563 06 08) oder schreiben Sie an
       info@datalization.ch.</p>
    <p>Meine Visitenkarte habe ich beigelegt.</p>

    <p style="margin-top:6mm;">Freundliche Grüsse</p>
    <div class="sign-space"></div>
    <p>Tihomir Danesic<br>Datalization</p>

    <div class="enclosure">Beilage: Visitenkarte</div>
  </div>

  <div class="footer">
    Datalization · Bärengasse 3 · 4800 Zofingen · 076 563 06 08 ·
    info@datalization.ch · www.datalization.ch
  </div>
</div>"""


class Command(BaseCommand):
    help = "Serienbriefe (HTML/A4) für Neugründungen ohne E-Mail."

    def add_arguments(self, parser):
        parser.add_argument("--out", default="~/Downloads/Serienbrief_Neugruendungen.html")
        parser.add_argument("--bezirk-zofingen", action="store_true")
        parser.add_argument("--active-only", action="store_true", default=True)
        parser.add_argument("--limit", type=int, default=15, help="Anzahl Briefe (Default 15).")
        parser.add_argument("--mark", action="store_true",
                            help="Die erzeugten Firmen in Odoo mit 'Brief versendet' taggen, "
                                 "damit sie beim nächsten Lauf übersprungen werden.")

    @staticmethod
    def _rank(r):
        """Priorität: Telefon (Nachfass) → AG/GmbH → Bezirk Zofingen → neuste."""
        lf = (r.legal_form or "").lower()
        legal = next((v for k, v in LEGAL_RANK if k in lf), 1)
        has_phone = 1 if (r.phone or "").strip() else 0
        bezirk = 1 if r.town in BEZIRK_ZOFINGEN else 0
        pub = r.publication_date.toordinal() if hasattr(r.publication_date, "toordinal") else 0
        return (has_phone, legal, bezirk, pub)

    def handle(self, *args, **opts):
        qs = (NewCompany.objects
              .exclude(shab_id__startswith="zefix:")
              .filter(Q(email="") | Q(email__isnull=True))
              .exclude(Q(street="") | Q(street__isnull=True))
              .exclude(Q(zip_code="") | Q(zip_code__isnull=True))
              .exclude(Q(town="") | Q(town__isnull=True)))
        if opts["active_only"]:
            qs = qs.filter(zefix_status="ACTIVE")
        if opts["bezirk_zofingen"]:
            qs = qs.filter(town__in=BEZIRK_ZOFINGEN)

        # Bereits versendete (Odoo-Tag 'Brief versendet') überspringen
        client = None
        sent_tag = None
        if odoo_crm.enabled():
            client = odoo_crm.OdooClient()
            sent_tag = client.tag_id(SENT_TAG)
            sent_ids = client._execute("crm.lead", "search_read",
                                       [["tag_ids", "in", sent_tag]], fields=["id"])
            sent = {x["id"] for x in sent_ids}
            if sent:
                qs = qs.exclude(odoo_lead_id__in=sent)
                self.stdout.write(f"{len(sent)} bereits mit '{SENT_TAG}' getaggt → übersprungen.")

        records = sorted(qs, key=self._rank, reverse=True)[:opts["limit"]]
        if not records:
            self.stdout.write("Keine offenen Briefkandidaten.")
            return

        today = timezone.localdate()
        datum = f"{today.day}. {MONTHS[today.month]} {today.year}"
        letters = [render_letter(r, datum) for r in records]

        self.stdout.write(f"Ausgewählt ({len(records)}):")
        for r in records:
            tel = f"☎ {r.phone}" if r.phone else "(kein Tel.)"
            self.stdout.write(f"  • {r.name[:40]:40} {r.town:14} {r.legal_form[:18]:18} {tel}")

        if opts["mark"] and client:
            ids = [r.odoo_lead_id for r in records if r.odoo_lead_id]
            if ids:
                client._execute("crm.lead", "write", ids, {"tag_ids": [(4, sent_tag)]})
                self.stdout.write(self.style.SUCCESS(
                    f"{len(ids)} Firmen in Odoo mit '{SENT_TAG}' getaggt."))

        html = (f"<!DOCTYPE html><html lang='de'><head><meta charset='utf-8'>"
                f"<title>Serienbrief Neugründungen</title><style>{PAGE_CSS}</style></head>"
                f"<body>{''.join(letters)}</body></html>")

        out = os.path.expanduser(opts["out"])
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        self.stdout.write(self.style.SUCCESS(f"{len(letters)} Briefe erzeugt → {out}"))
