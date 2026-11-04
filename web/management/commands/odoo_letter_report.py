"""Richtet in Odoo den druckbaren QWeb-Report 'Erstkontakt-Brief' auf crm.lead ein.

Eigenes Datalization-Layout (Kopf: Logo + Slogan; Fuss: Adresszeile), A4,
Schweizer Fensterkuvert (Empfängeradresse links im Sichtfenster). Danach in
Odoo: Chance(n) markieren → Drucken → 'Erstkontakt-Brief' → PDF.

Technik-Hinweise (wkhtmltopdf/Odoo 20):
* Umlaute als echte UTF-8-Zeichen (keine &#..;-Entities).
* dynamische Werte mit t-out (t-esc wird ignoriert).
* Positionierung via position:fixed (position:absolute wird nicht sauber umgesetzt).

Idempotent: Paperformat, View, External-ID und Report-Aktion werden gesucht
und aktualisiert.

    python manage.py odoo_letter_report
"""
from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

CRM_LEAD_MODEL_ID = 2655
XMLID = "x_datalization.erstkontakt_brief"
MODULE, NAME = XMLID.split(".")
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

ARCH = f"""<t t-name="x_datalization.erstkontakt_brief">
<t t-call="web.html_container">
<t t-foreach="docs" t-as="o">
<div class="page" style="position:relative;font-family:Arial,Helvetica,sans-serif;font-size:11pt;line-height:1.5;color:#000;">
  <div style="position:fixed;top:12mm;right:20mm;text-align:right;">
    <img src="{LOGO}" style="width:42px;height:auto;display:inline-block;vertical-align:middle;"/>
    <span style="font-size:13pt;font-weight:bold;vertical-align:middle;margin-left:8px;">Datalization</span>
    <div style="color:#F48B2D;font-weight:bold;font-size:9pt;margin-top:2px;">Einfache Lösungen schaffen.</div>
  </div>

  <div style="position:fixed;top:45mm;left:25mm;">
    <div style="font-size:7pt;color:#555;">Datalization · Bärengasse 3 · 4800 Zofingen</div>
    <div style="font-size:11pt;line-height:1.4;margin-top:1mm;">
      <span t-out="o.partner_name or o.name"/><br/>
      <span t-out="o.street"/><br/>
      <span t-out="o.zip"/> <span t-out="o.city"/>
    </div>
  </div>

  <div style="position:fixed;bottom:10mm;left:25mm;right:20mm;border-top:1px solid #ccc;padding-top:2mm;font-size:8pt;color:#666;text-align:center;">
    Datalization · Bärengasse 3 · 4800 Zofingen · 076 563 06 08 · info@datalization.ch · www.datalization.ch
  </div>

  <div style="padding:66mm 20mm 24mm 25mm;">
    <div style="text-align:right;margin-bottom:10mm;">Zofingen, <span t-out="datetime.date.today().strftime('%d.%m.%Y')"/></div>
    <div style="font-weight:bold;font-size:13pt;margin-bottom:6mm;">Herzlichen Glückwunsch zur Gründung – und ein Angebot für Ihren Start</div>
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
    <div style="height:22mm;"></div>
    <p>Tihomir Danesic<br/>Datalization</p>
    <div style="margin-top:8mm;font-size:10pt;">Beilage: Visitenkarte</div>
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

        # Paperformat (randlos A4, damit Kopf/Fuss exakt sitzen)
        pf_vals = {"name": "Datalization Brief A4", "format": "A4", "orientation": "Portrait",
                   "margin_top": 0, "margin_bottom": 0, "margin_left": 0, "margin_right": 0,
                   "header_line": False, "header_spacing": 0, "dpi": 90}
        pf = c._execute("report.paperformat", "search",
                        [["name", "=", "Datalization Brief A4"]], limit=1)
        pf_id = pf[0] if pf else c._execute("report.paperformat", "create", pf_vals)
        if pf:
            c._execute("report.paperformat", "write", pf, pf_vals)

        # QWeb-View
        view = c._execute("ir.ui.view", "search", [["key", "=", XMLID]], limit=1)
        v_vals = {"name": "Erstkontakt-Brief", "type": "qweb", "key": XMLID, "arch_db": ARCH}
        if view:
            c._execute("ir.ui.view", "write", view, v_vals)
            view_id = view[0]
        else:
            view_id = c._execute("ir.ui.view", "create", v_vals)

        # External ID, damit report_name den View auflöst
        imd = c._execute("ir.model.data", "search",
                         [["module", "=", MODULE], ["name", "=", NAME]], limit=1)
        if not imd:
            c._execute("ir.model.data", "create",
                       {"module": MODULE, "name": NAME,
                        "model": "ir.ui.view", "res_id": view_id})

        # Report-Aktion (Drucken-Menü von crm.lead)
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
            f"Report 'Erstkontakt-Brief' bereit (action {rep_id}, view {view_id}, "
            f"paperformat {pf_id}). In Odoo: Chance → Drucken → Erstkontakt-Brief."))
