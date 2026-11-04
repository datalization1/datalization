"""Richtet in Odoo den druckbaren QWeb-Report 'Erstkontakt-Brief' auf crm.lead ein.

Nutzt das unternehmensweite Dokumenten-Layout + Paperformat 'Datalization A4'
(siehe odoo_document_layout). Positionen gemäss Spezifikation (Körper startet
bei margin_top = 40 mm):
  Absender/Empfänger rechts (links 118 mm, Breite 72 mm), Empfänger ~52 mm;
  Ort/Datum 100 mm; Betreff 112 mm.

Vertikale Positionierung über feste Spacer-Höhen (margin-top kollabiert in
wkhtmltopdf). Paperformat wird explizit am Report gesetzt.

    python manage.py odoo_letter_report
"""
from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

CRM_LEAD_MODEL_ID = 2655
XMLID = "x_datalization.erstkontakt_brief"
MODULE, NAME = XMLID.split(".")
PAPERFORMAT_NAME = "Datalization A4"

DATUM = ("'%d. %s %d' % (datetime.date.today().day, "
         "['','Januar','Februar','März','April','Mai','Juni','Juli','August',"
         "'September','Oktober','November','Dezember'][datetime.date.today().month], "
         "datetime.date.today().year)")

# Körper beginnt bei 40 mm (margin_top). Spacer relativ dazu:
#   Empfänger 52 mm → 12 mm; Ort/Datum 100 mm → 60 mm; Betreff 112 mm → 72 mm.
ARCH = f"""<t t-name="{XMLID}">
<t t-call="web.html_container">
<t t-foreach="docs" t-as="o">
<t t-call="web.external_layout">
<div class="page" style="font-size:10pt;color:#0A0A0A;line-height:1.5;">
  <div style="float:right;width:72mm;padding-top:7mm;">
    <span style="display:inline-block;font-size:6.5pt;color:#4F4F4F;border-bottom:0.2mm solid #BDBDBD;padding-bottom:0.6mm;">Datalization · Bärengasse 3 · 4800 Zofingen</span>
    <div style="font-size:10pt;line-height:1.45;padding-top:1.5mm;">
      <span t-out="o.partner_name or o.name"/><br/>
      <span t-out="o.street"/><br/>
      <span t-out="o.zip"/> <span t-out="o.city"/>
    </div>
  </div>
  <div style="height:60mm;"></div>
  <div style="clear:both;">Zofingen, <span t-out="{DATUM}"/></div>
  <div style="height:7mm;"></div>
  <div style="font-size:11pt;font-weight:bold;letter-spacing:-0.01em;">Herzlichen Glückwunsch zur Gründung – und ein Angebot für Ihren Start</div>
  <div style="height:7mm;"></div>
  <p style="margin:0 0 4mm 0;">Sehr geehrte Damen und Herren</p>
  <p style="margin:0 0 4mm 0;">herzlichen Glückwunsch zur Gründung von <strong><span t-out="o.partner_name or o.name"/></strong>.
     Wir haben Ihren Eintrag im Handelsregister (SHAB) gesehen und wünschen Ihnen einen erfolgreichen Start.</p>
  <p style="margin:0 0 4mm 0;">Wir sind <strong>Datalization</strong> aus Zofingen und bauen für kleine Betriebe die ganze
     digitale Basis auf – von der IT bis zu den Abläufen:</p>
  <ul style="margin:0 0 4mm 0;">
    <li>Komplette <strong>IT aus einer Hand</strong>: Hardware, Software-Lizenzen, Einrichtung und
        laufender Betrieb (<strong>Managed IT</strong>)</li>
    <li>Offerten, Rechnungen und Buchhaltung ohne Zettelwirtschaft</li>
    <li>Kundenverwaltung (CRM) – häufig mit <strong>Odoo</strong></li>
    <li>wiederkehrende Abläufe automatisieren – mehr Zeit fürs Kerngeschäft</li>
  </ul>
  <p style="margin:0 0 4mm 0;">Gerade am Anfang spart ein durchdachtes Setup später viel Zeit und Ärger. Gerne zeigen
     wir Ihnen in einem <strong>kostenlosen 30-minütigen Erstgespräch</strong> unverbindlich, was für Ihren
     Betrieb sinnvoll ist – rufen Sie uns an (076 563 06 08) oder schreiben Sie an info@datalization.ch.</p>
  <p style="margin:0 0 4mm 0;">Meine Visitenkarte habe ich beigelegt.</p>
  <div style="height:8mm;"></div>
  <p style="margin:0;">Freundliche Grüsse</p>
  <div style="height:14mm;"></div>
  <p style="margin:0;font-weight:600;">Tihomir Danesic</p>
  <p style="margin:0;">Inhaber</p>
  <div style="height:6mm;"></div>
  <p style="margin:0;font-size:9pt;">Beilage: Visitenkarte</p>
</div>
</t>
</t>
</t>
</t>"""


class Command(BaseCommand):
    help = "Richtet den Odoo-Druckreport 'Erstkontakt-Brief' (crm.lead) ein."

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        pf = c._execute("report.paperformat", "search", [["name", "=", PAPERFORMAT_NAME]], limit=1)
        pf_id = pf[0] if pf else False

        view = c._execute("ir.ui.view", "search", [["key", "=", XMLID]], limit=1)
        v_vals = {"name": "Erstkontakt-Brief", "type": "qweb", "key": XMLID, "arch_db": ARCH}
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

        rep = c._execute("ir.actions.report", "search",
                         [["report_name", "=", XMLID]], limit=1)
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
            f"Report 'Erstkontakt-Brief' bereit (action {rep_id}, view {view_id}, paperformat {pf_id})."))
