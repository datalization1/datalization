"""Richtet in Odoo den druckbaren QWeb-Report 'Erstkontakt-Brief' auf crm.lead ein.

Danach in Odoo: Chance (oder mehrere in der Liste) markieren → Drucken →
'Erstkontakt-Brief' → PDF (A4, Schweizer Fensterkuvert, Adresse im Sichtfenster).

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


def _arch():
    return f"""<t t-name="{XMLID}">
<t t-call="web.html_container">
<t t-foreach="docs" t-as="o">
<div class="page" style="position:relative;font-family:Arial,Helvetica,sans-serif;font-size:11pt;line-height:1.5;color:#000;padding:18mm 20mm 16mm 25mm;">
  <div style="text-align:right;">
    <img src="{LOGO}" style="width:40px;height:auto;display:inline-block;vertical-align:middle;"/>
    <span style="font-size:13pt;font-weight:bold;vertical-align:middle;margin-left:8px;">Datalization</span>
    <div style="color:#F48B2D;font-weight:bold;font-size:9pt;">Einfache L&#246;sungen schaffen.</div>
  </div>
  <div style="position:absolute;top:42mm;left:25mm;font-size:7pt;color:#555;">Datalization &#183; B&#228;rengasse 3 &#183; 4800 Zofingen</div>
  <div style="position:absolute;top:46mm;left:25mm;font-size:11pt;line-height:1.4;">
    <span t-out="o.partner_name or o.name"/><br/>
    <span t-out="o.street"/><br/>
    <span t-out="o.zip"/> <span t-out="o.city"/>
  </div>
  <div style="margin-top:62mm;">
    <div style="text-align:right;margin-bottom:10mm;">Zofingen, <span t-esc="datetime.date.today().strftime('%d.%m.%Y')"/></div>
    <div style="font-weight:bold;margin-bottom:6mm;">Herzlichen Gl&#252;ckwunsch zur Gr&#252;ndung &#8211; und ein Angebot f&#252;r Ihren Start</div>
    <p>Sehr geehrte Damen und Herren</p>
    <p>herzlichen Gl&#252;ckwunsch zur Gr&#252;ndung von <b><span t-out="o.partner_name or o.name"/></b>. Wir haben Ihren Eintrag im Handelsregister (SHAB) gesehen und w&#252;nschen Ihnen einen erfolgreichen Start.</p>
    <p>Wir sind <b>Datalization</b> aus Zofingen und bauen f&#252;r kleine Betriebe die ganze digitale Basis auf &#8211; von der IT bis zu den Abl&#228;ufen:</p>
    <ul style="margin:3mm 0;padding-left:6mm;">
      <li>Komplette <b>IT aus einer Hand</b>: Hardware, Software-Lizenzen, Einrichtung und laufender Betrieb (<b>Managed IT</b>)</li>
      <li>Offerten, Rechnungen und Buchhaltung ohne Zettelwirtschaft</li>
      <li>Kundenverwaltung (CRM) &#8211; h&#228;ufig mit <b>Odoo</b></li>
      <li>wiederkehrende Abl&#228;ufe automatisieren &#8211; mehr Zeit f&#252;rs Kerngesch&#228;ft</li>
    </ul>
    <p>Gerade am Anfang spart ein durchdachtes Setup sp&#228;ter viel Zeit und &#196;rger. Gerne zeigen wir Ihnen in einem <b>kostenlosen 30-min&#252;tigen Erstgespr&#228;ch</b> unverbindlich, was f&#252;r Ihren Betrieb sinnvoll ist &#8211; rufen Sie uns an (076 563 06 08) oder schreiben Sie an info@datalization.ch.</p>
    <p>Meine Visitenkarte habe ich beigelegt.</p>
    <p style="margin-top:6mm;">Freundliche Gr&#252;sse</p>
    <div style="height:18mm;"></div>
    <p>Tihomir Danesic<br/>Datalization</p>
    <div style="margin-top:8mm;font-size:10pt;">Beilage: Visitenkarte</div>
  </div>
  <div style="position:absolute;bottom:10mm;left:25mm;right:20mm;border-top:1px solid #ccc;padding-top:2mm;font-size:8pt;color:#666;text-align:center;">Datalization &#183; B&#228;rengasse 3 &#183; 4800 Zofingen &#183; 076 563 06 08 &#183; info@datalization.ch &#183; www.datalization.ch</div>
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

        # 1) Paperformat (randlos, A4)
        pf = c._execute("report.paperformat", "search",
                        [["name", "=", "Datalization Brief A4"]], limit=1)
        pf_vals = {"name": "Datalization Brief A4", "format": "A4",
                   "orientation": "Portrait", "margin_top": 0, "margin_bottom": 0,
                   "margin_left": 0, "margin_right": 0, "header_line": False,
                   "header_spacing": 0, "dpi": 90}
        pf_id = pf[0] if pf else c._execute("report.paperformat", "create", pf_vals)
        if pf:
            c._execute("report.paperformat", "write", pf, pf_vals)

        # 2) QWeb-View
        view = c._execute("ir.ui.view", "search", [["key", "=", XMLID]], limit=1)
        v_vals = {"name": "Erstkontakt-Brief", "type": "qweb",
                  "key": XMLID, "arch_db": _arch()}
        if view:
            c._execute("ir.ui.view", "write", view, v_vals)
            view_id = view[0]
        else:
            view_id = c._execute("ir.ui.view", "create", v_vals)

        # 3) External ID, damit report_name den View auflöst
        imd = c._execute("ir.model.data", "search",
                         [["module", "=", MODULE], ["name", "=", NAME]], limit=1)
        if not imd:
            c._execute("ir.model.data", "create",
                       {"module": MODULE, "name": NAME,
                        "model": "ir.ui.view", "res_id": view_id})

        # 4) Report-Aktion (im Drucken-Menü von crm.lead)
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
