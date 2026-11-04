"""Richtet in Odoo den druckbaren QWeb-Report 'Erstkontakt-Brief' auf crm.lead ein.

Eigene Layout-Vorlage (x_datalization.letter_layout) mit demselben strukturellen
Aufbau wie das Standard-Odoo-Layout (header / external_layout_body / footer) –
dadurch bleiben die Umlaute im PDF sauber – aber mit Datalization-Kopf
(Logo + Slogan) und -Fusszeile (Adresszeile). Rechnungen bleiben unberührt.

Empfängeradresse rechts (Fensterkuvert rechts), Ort/Datum links. Danach in Odoo:
Chance(n) markieren → Drucken → 'Erstkontakt-Brief'.

Idempotent: Views, External-IDs und Report-Aktion werden gesucht und aktualisiert.

    python manage.py odoo_letter_report
"""
from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

CRM_LEAD_MODEL_ID = 2655
REPORT_XMLID = "x_datalization.erstkontakt_brief"
LAYOUT_XMLID = "x_datalization.letter_layout"
LOGO = ("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAwCAYAAABT9ym6AAAEfklEQVR4nOxa"
        "W2gUVxj+zuw9G02bamia9kVt0VDb1N5LaWlsaYug4gVF0AcR8cUrEby8RMULiuKL4JuvKmgUQUERLyio"
        "+BCJhHhBRUR9UYxuJsludsfvjDuyG3fmzM664wh+MPvP7vnnnPOd/z/n/OefDeEdIRaLjY1Go18ODQ0"
        "949cMKoQGnxGJRCYlEom7oVDothDiMu+f89rKojAqQAg+ghaYEA6HL5HAaOs38Qq/k2BjJpM5Bo8Q8BE"
        "1NTXHKf63K6ebTUyn09fhAX671q9OhZqm/QiP8JWIYRh1CpVP4RG+T/Zq4QORoOEDkaChot20TDTInU"
        "+hY8AjfCPCMGSeCzVbokZ7czRdGxqTzWZHJqL6TbHy3rPC8kqJNDDsGMWNrN6uLu4dNSyfT2PMdVFfSYu"
        "82NHcmoLWIQyMhBZC39AIvNj+9d5aPbdctHengfKJjIrH49PZsRns4GR2Loq3izcskto+cSXFDgyLC9n2"
        "klRS+8bYMn6qWNfzxBURxkiNFO3s/EJWEM5XhGrD2NVc35c1VrO1ksGtgPitLxKZytt9ylUrH2I/5LXYIl"
        "FFFLmWngn9we42Kh6ZIz+dOhajJTrgEK1WAUVmNjT8onzCQIsUdhapoyXOw18SEsWT3cieVT4h0ClFKSIa"
        "SXTQjX6C/yiySDKMK6T2UPHIAfn5BhGS2E0SfyEAEKu6nwoNi2wVDONk7equffK2iAiX1laSWIoAIdnWdQ"
        "JaroUr5jl+zZo/GnhAEiuS+vXXrl9kSlpDJgTGwh06c7mcPH/3UPZQDtroibybyqX7K6cKWc/agYGBbXbl"
        "xrYxdalwvGlEW3f38LJwAYk2NyQ4MjnqbdJ1faNsG+5whivgDcoOhZ7j5iTW3Oml6C1VVrj8LoMavSQys7"
        "+//zTKBIkfIRmVmueg0ZwjTMV8x1H+QqVMEkto+rJJFDyv6qjncMG0CIlMUymyD0dpif0IKCzX+kGlyJzT"
        "BgQYFpHPnJRojRSzgJ0IMCwiTU5KnD9nUcFE9AMWkQaF3luxRjWPutbO/thJia7ldpOEop6qrVoWkUdOSh"
        "zIFgQcFhFFhIkJvBKoECrX4hG6Fh5hEmGMc0WlyF15LSqEC9f6Fh5hjhBfg43jG6RbUHSChP8dHBw8BY9g"
        "PJdzsgqbkIHnOG68D1AmTIuwc7ehWJlkB0j2IDszA94QV7kWi2O89sIDXp9HOBpbXOh/xIYOkYw8ldWjDN"
        "A1/3OpOiVffxJlQAxr7CrF93AJkj9PYheZ/btAqdu14fY8Mqzu+xSH+cwZuvTzgsroef1dvNVtiXCu/EP3"
        "OYmAI38m2syjgYz/zFNjUeKLI3uHkfDnvJ2EACM/1/7kG+KPGcyeMH8rpUgXkyvT33gPwMEfz8XqRsm8Fk"
        "02S/o/3gPQOD9LaZeg6+WEaiWZPQg4GA2YrxeUQRpTRJOpvBMV7LrVBL1H5oYfK5PY8oxOZZlXku83riFA"
        "4LK8APnIveywWf6rh345m5dcDJooP6EcDZ/AAR2guEa5vjAR4ut/UaqJlwAAAP//Xpeq7AAAAAZJREFUAw"
        "BMvW3GCHKTxwAAAABJRU5ErkJggg==")

LAYOUT_ARCH = f"""<t t-name="{LAYOUT_XMLID}">
<t t-if="not o" t-set="o" t-value="doc"/>
<t t-if="not company" t-set="company" t-value="(o and o.company_id) or res_company"/>
<div class="header">
  <div style="text-align:right;">
    <img src="{LOGO}" style="width:44px;height:auto;display:inline-block;vertical-align:middle;"/>
    <span style="font-size:14pt;font-weight:bold;vertical-align:middle;margin-left:8px;">Datalization</span>
    <div style="color:#F48B2D;font-weight:bold;font-size:9pt;margin-top:2px;">Einfache Lösungen schaffen.</div>
  </div>
</div>
<t t-call="web.external_layout_body">
  <t t-out="0"/>
</t>
<div class="footer">
  <div class="text-center" style="border-top:1px solid #ccc;padding-top:6px;font-size:8pt;color:#666;">
    Datalization · Bärengasse 3 · 4800 Zofingen · 076 563 06 08 · info@datalization.ch · www.datalization.ch
  </div>
</div>
</t>"""

REPORT_ARCH = f"""<t t-name="{REPORT_XMLID}">
<t t-call="web.html_container">
<t t-foreach="docs" t-as="o">
<t t-call="{LAYOUT_XMLID}">
<div class="page">
  <div class="row">
    <div class="col-6 offset-6">
      <span t-out="o.partner_name or o.name"/><br/>
      <span t-out="o.street"/><br/>
      <span t-out="o.zip"/> <span t-out="o.city"/>
    </div>
  </div>
  <p style="margin-top:16mm;">Zofingen, <span t-out="datetime.date.today().strftime('%d.%m.%Y')"/></p>
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
  <p>Tihomir Danesic<br/>Datalization</p>
  <p style="margin-top:6mm;"><small>Beilage: Visitenkarte</small></p>
</div>
</t>
</t>
</t>
</t>"""


class Command(BaseCommand):
    help = "Richtet den Odoo-Druckreport 'Erstkontakt-Brief' (crm.lead) ein."

    def _upsert_view(self, c, xmlid, name, arch):
        module, nm = xmlid.split(".")
        view = c._execute("ir.ui.view", "search", [["key", "=", xmlid]], limit=1)
        vals = {"name": name, "type": "qweb", "key": xmlid, "arch_db": arch}
        if view:
            c._execute("ir.ui.view", "write", view, vals)
            vid = view[0]
        else:
            vid = c._execute("ir.ui.view", "create", vals)
        imd = c._execute("ir.model.data", "search",
                         [["module", "=", module], ["name", "=", nm]], limit=1)
        if not imd:
            c._execute("ir.model.data", "create",
                       {"module": module, "name": nm, "model": "ir.ui.view", "res_id": vid})
        return vid

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        self._upsert_view(c, LAYOUT_XMLID, "Datalization Brief-Layout", LAYOUT_ARCH)
        view_id = self._upsert_view(c, REPORT_XMLID, "Erstkontakt-Brief", REPORT_ARCH)

        rep = c._execute("ir.actions.report", "search",
                         [["report_name", "=", REPORT_XMLID]], limit=1)
        r_vals = {"name": "Erstkontakt-Brief", "model": "crm.lead",
                  "report_type": "qweb-pdf", "report_name": REPORT_XMLID,
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
            f"In Odoo: Chance → Drucken → Erstkontakt-Brief."))
