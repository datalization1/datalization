"""Richtet in Odoo den druckbaren QWeb-Report 'Erstkontakt-Brief' auf crm.lead ein.

Nutzt das unternehmensweite Dokumenten-Layout (web.external_layout → siehe
odoo_document_layout) – also identischer Kopf/Fuss wie Rechnungen/Offerten.
Der Report liefert nur den Briefkörper: Empfängeradresse rechts (Fensterkuvert
rechts), Ort/Datum links, Betreff, Text, Unterschrift.

Idempotent. In Odoo: Chance(n) markieren → Drucken → 'Erstkontakt-Brief'.

    python manage.py odoo_letter_report
"""
from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

CRM_LEAD_MODEL_ID = 2655
XMLID = "x_datalization.erstkontakt_brief"
MODULE, NAME = XMLID.split(".")

# Deutsches Datum ohne Locale-Abhängigkeit (Babel/Server-Locale unzuverlässig)
DATUM = ("'%d. %s %d' % (datetime.date.today().day, "
         "['','Januar','Februar','März','April','Mai','Juni','Juli','August',"
         "'September','Oktober','November','Dezember'][datetime.date.today().month], "
         "datetime.date.today().year)")

ARCH = f"""<t t-name="{XMLID}">
<t t-call="web.html_container">
<t t-foreach="docs" t-as="o">
<t t-call="web.external_layout">
<div class="page">
  <div class="row">
    <div class="col-6 offset-6">
      <div style="font-size:7pt;color:#666;">Datalization · Bärengasse 3 · 4800 Zofingen</div>
      <div style="margin-top:1mm;">
        <span t-out="o.partner_name or o.name"/><br/>
        <span t-out="o.street"/><br/>
        <span t-out="o.zip"/> <span t-out="o.city"/>
      </div>
    </div>
  </div>
  <p style="margin-top:16mm;">Zofingen, <span t-out="{DATUM}"/></p>
  <h4 style="margin-top:14mm;margin-bottom:6mm;"><strong>Herzlichen Glückwunsch zur Gründung – und ein Angebot für Ihren Start</strong></h4>
  <p>Sehr geehrte Damen und Herren</p>
  <p>herzlichen Glückwunsch zur Gründung von <strong><span t-out="o.partner_name or o.name"/></strong>.
     Wir haben Ihren Eintrag im Handelsregister (SHAB) gesehen und wünschen Ihnen einen erfolgreichen Start.</p>
  <p>Wir sind <strong>Datalization</strong> aus Zofingen und bauen für kleine Betriebe die ganze digitale
     Basis auf – von der IT bis zu den Abläufen:</p>
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
  <p style="margin-top:6mm;">Freundliche Grüsse</p>
  <div style="height:22mm;"/>
  <p style="margin-bottom:0;"><strong>Tihomir Danesic</strong></p>
  <p style="margin-top:0;">Inhaber</p>
  <p style="margin-top:6mm;"><small>Beilage: Visitenkarte</small></p>
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
                  "paperformat_id": False,
                  "binding_model_id": CRM_LEAD_MODEL_ID, "binding_type": "report"}
        if rep:
            c._execute("ir.actions.report", "write", rep, r_vals)
            rep_id = rep[0]
        else:
            rep_id = c._execute("ir.actions.report", "create", r_vals)

        self.stdout.write(self.style.SUCCESS(
            f"Report 'Erstkontakt-Brief' bereit (action {rep_id}, view {view_id}). "
            f"Nutzt das unternehmensweite Layout."))
