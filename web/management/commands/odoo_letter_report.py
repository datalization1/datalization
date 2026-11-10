"""Richtet in Odoo den druckbaren QWeb-Report 'Erstkontakt-Brief' auf crm.lead ein.

EIGENSTÄNDIGES Layout (nutzt NICHT web.external_layout): Kopf/Adresse/Body/Fuss
sind absolut in einer 210×297-mm-Seite positioniert, eigenes Paperformat mit
0-Rändern. Das rendert in wkhtmltopdf vorhersehbar (keine Kopfzonen-Überlappung,
genau eine Seite) und entspricht der Briefvorlage 1:1. Die Inter-Schrift wird zur
Laufzeit aus dem Firmenlayout (view x_datalization.external_layout_custom)
übernommen, damit Schrift & Marke konsistent bleiben.

Massvorgaben (Briefvorlage): Empfänger rechts (links 118 mm, Breite 72 mm),
Absenderzeile ~47 mm, Empfänger ~50 mm, Body ab 92 mm, Fuss unten 12 mm.

    python manage.py odoo_letter_report
"""
import re

from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

CRM_LEAD_MODEL_ID = 2655
XMLID = "x_datalization.erstkontakt_brief"
MODULE, NAME = XMLID.split(".")
LAYOUT_KEY = "x_datalization.external_layout_custom"   # Quelle der Inter-Schrift
PAPERFORMAT_NAME = "Datalization Brief"                 # 0-Rand, eigenständig

DATUM = ("'%d. %s %d' % (datetime.date.today().day, "
         "['','Januar','Februar','März','April','Mai','Juni','Juli','August',"
         "'September','Oktober','November','Dezember'][datetime.date.today().month], "
         "datetime.date.today().year)")

# Oranger Punkt als SVG (wkhtmltopdf-sicher, wie im Firmenlayout).
DOT = ('<svg width="1.4mm" height="1.4mm" viewBox="0 0 10 10" '
       'style="margin-left:0.5mm;vertical-align:baseline;">'
       '<circle cx="5" cy="5" r="5" fill="#F48B2D"/></svg>')

LAYOUT_CSS = """
*{box-sizing:border-box;}
.page{position:relative;width:210mm;height:296mm;overflow:hidden;
      padding:0 20mm 0 25mm;font-family:'Datalization Inter',sans-serif;
      color:#0A0A0A;}
.dl-header{position:absolute;top:15mm;left:25mm;right:20mm;}
.dl-header .dl-logo{height:9mm;display:inline-block;vertical-align:middle;}
.dl-header .dl-slogan{float:right;font-size:9.5pt;font-weight:600;
      letter-spacing:-0.01em;color:#0A0A0A;line-height:9mm;}
.dl-addr{position:absolute;top:47mm;left:118mm;width:72mm;}
.dl-addr .dl-sender{font-size:6.5pt;color:#4F4F4F;
      border-bottom:0.2mm solid #BDBDBD;padding-bottom:0.6mm;display:inline-block;}
.dl-addr .dl-recipient{font-size:10.5pt;line-height:1.45;padding-top:1.8mm;}
.dl-body{position:absolute;top:92mm;left:25mm;right:20mm;
      font-size:10.5pt;line-height:1.5;}
.dl-body .dl-date{margin-bottom:7mm;}
.dl-body .dl-subject{font-size:11pt;font-weight:700;letter-spacing:-0.01em;
      margin-bottom:7mm;}
.dl-body p{margin:0 0 3.6mm 0;}
.dl-body ul{margin:0 0 3.6mm 0;padding-left:5mm;}
.dl-body li{margin-bottom:0.8mm;}
.dl-body .dl-gruss{margin-top:5mm;margin-bottom:0;}
.dl-body .dl-signspace{height:12mm;}
.dl-body .dl-signer{margin:0;}
.dl-body .dl-enclosure{margin-top:6mm;font-size:9pt;}
.dl-footer{position:absolute;bottom:12mm;left:25mm;right:20mm;
      border-top:0.25mm solid #E4E4E0;padding-top:3mm;text-align:center;
      font-size:7.5pt;color:#4F4F4F;}
.dl-footer strong{color:#0A0A0A;font-weight:600;}
.dl-footer .dl-sep{color:#F48B2D;padding:0 1.4mm;}
"""


def build_arch(font_css):
    return f"""<t t-name="{XMLID}">
<t t-call="web.html_container">
<t t-foreach="docs" t-as="o">
<style>{font_css}{LAYOUT_CSS}</style>
<div class="page">
  <div class="dl-header">
    <img class="dl-logo" t-if="o.company_id.logo" t-att-src="image_data_uri(o.company_id.logo)" alt="Logo"/>
    <span class="dl-slogan">Einfache Lösungen schaffen{DOT}</span>
  </div>
  <div class="dl-addr">
    <span class="dl-sender">Datalization · Bärengasse 3 · 4800 Zofingen</span>
    <div class="dl-recipient"><span t-out="o.partner_name or o.name"/><br/><span t-out="o.street"/><br/><span t-out="o.zip"/> <span t-out="o.city"/></div>
  </div>
  <div class="dl-body">
    <div class="dl-date">Zofingen, <span t-out="{DATUM}"/></div>
    <div class="dl-subject">Herzlichen Glückwunsch zur Gründung – und ein Angebot für Ihren Start</div>
    <p>Sehr geehrte Damen und Herren</p>
    <p>herzlichen Glückwunsch zur Gründung von <strong><span t-out="o.partner_name or o.name"/></strong>.
       Wir haben Ihren Eintrag im Handelsregister (SHAB) gesehen und wünschen Ihnen einen erfolgreichen Start.</p>
    <p>Wir sind <strong>Datalization</strong> aus Zofingen und bauen für kleine Betriebe die ganze
       digitale Basis auf – von der IT bis zu den Abläufen:</p>
    <ul>
      <li>Komplette <strong>IT aus einer Hand</strong>: Hardware, Software-Lizenzen, Einrichtung und
          laufender Betrieb (<strong>Managed IT</strong>)</li>
      <li>Offerten, Rechnungen und Buchhaltung ohne Zettelwirtschaft</li>
      <li>Kundenverwaltung (CRM) – häufig mit <strong>Odoo</strong></li>
      <li>wiederkehrende Abläufe automatisieren – mehr Zeit fürs Kerngeschäft</li>
    </ul>
    <p>Gerade am Anfang spart ein durchdachtes Setup später viel Zeit und Ärger. Gerne zeigen wir Ihnen
       in einem <strong>kostenlosen 30-minütigen Erstgespräch</strong> unverbindlich, was für Ihren Betrieb
       sinnvoll ist – rufen Sie uns an (076 563 06 08) oder schreiben Sie an info@datalization.ch.</p>
    <p>Meine Visitenkarte habe ich beigelegt.</p>
    <p class="dl-gruss">Freundliche Grüsse</p>
    <div class="dl-signspace"></div>
    <p class="dl-signer"><strong>Tihomir Danesic</strong><br/>Inhaber</p>
    <p class="dl-enclosure">Beilage: Visitenkarte</p>
  </div>
  <div class="dl-footer">
    <strong>Datalization</strong><span class="dl-sep">·</span>Bärengasse 3<span class="dl-sep">·</span>4800 Zofingen<span class="dl-sep">·</span>076 563 06 08<span class="dl-sep">·</span>info@datalization.ch<span class="dl-sep">·</span>www.datalization.ch
  </div>
</div>
</t>
</t>
</t>"""


class Command(BaseCommand):
    help = "Richtet den Odoo-Druckreport 'Erstkontakt-Brief' (crm.lead) ein."

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        # Inter-Schrift aus dem Firmenlayout übernehmen (@font-face-Block).
        font_css = ""
        lay = c._execute("ir.ui.view", "search_read", [["key", "=", LAYOUT_KEY]],
                         fields=["arch_db"], limit=1)
        if lay:
            m = re.search(r'<t t-set="dl_css">(.*?)</t>', lay[0]["arch_db"], re.S)
            if m:
                # nur die @font-face-Regeln (ohne die .header/.footer-Zuweisung)
                font_css = m.group(1).split(".header")[0]
        if not font_css:
            self.stdout.write(self.style.WARNING(
                "Inter-Schrift im Firmenlayout nicht gefunden – Fallback auf Odoo-Standardschrift."))

        arch = build_arch(font_css)

        # --- Paperformat 'Datalization Brief' (0-Rand) ---
        pf_vals = {"name": PAPERFORMAT_NAME, "format": "A4", "orientation": "Portrait",
                   "margin_top": 0, "margin_bottom": 0, "margin_left": 0, "margin_right": 0,
                   "header_line": False, "header_spacing": 0, "dpi": 90}
        pf = c._execute("report.paperformat", "search", [["name", "=", PAPERFORMAT_NAME]], limit=1)
        pf_id = pf[0] if pf else c._execute("report.paperformat", "create", pf_vals)
        if pf:
            c._execute("report.paperformat", "write", pf, pf_vals)

        # --- View ---
        view = c._execute("ir.ui.view", "search", [["key", "=", XMLID]], limit=1)
        v_vals = {"name": "Erstkontakt-Brief", "type": "qweb", "key": XMLID, "arch_db": arch}
        if view:
            c._execute("ir.ui.view", "write", view, v_vals)
            view_id = view[0]
        else:
            view_id = c._execute("ir.ui.view", "create", v_vals)

        imd = c._execute("ir.model.data", "search",
                         [["module", "=", MODULE], ["name", "=", NAME]], limit=1)
        if not imd:
            c._execute("ir.model.data", "create",
                       {"module": MODULE, "name": NAME, "model": "ir.ui.view", "res_id": view_id})

        # --- Report-Action ---
        rep = c._execute("ir.actions.report", "search", [["report_name", "=", XMLID]], limit=1)
        r_vals = {"name": "Erstkontakt-Brief", "model": "crm.lead",
                  "report_type": "qweb-pdf", "report_name": XMLID,
                  "print_report_name": "'Brief - %s' % (object.partner_name or object.name)",
                  "paperformat_id": pf_id,
                  "binding_model_id": CRM_LEAD_MODEL_ID, "binding_type": "report"}
        if rep:
            c._execute("ir.actions.report", "write", rep, r_vals)
            rep_id = rep[0]
        else:
            rep_id = c._execute("ir.actions.report", "create", r_vals)

        self.stdout.write(self.style.SUCCESS(
            f"Report 'Erstkontakt-Brief' bereit (action {rep_id}, view {view_id}, "
            f"paperformat '{PAPERFORMAT_NAME}' id {pf_id}, Schrift: "
            f"{'Inter' if font_css else 'Standard'})."))
