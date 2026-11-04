"""Setzt das unternehmensweite Odoo-Dokumenten-Layout (Kopf/Fuss) auf das
Datalization-Briefdesign: Wortmarke links, Slogan rechts, zentrierte Fusszeile.

Gilt danach für ALLE Reports, die web.external_layout nutzen – Rechnungen,
Offerten, Lieferscheine, CRM-Briefe usw.

Idempotent. Reversibel: der vorherige external_report_layout_id wird ausgegeben.

    python manage.py odoo_document_layout
"""
import base64
import os

from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

LAYOUT_XMLID = "x_datalization.external_layout_custom"
MODULE, NAME = LAYOUT_XMLID.split(".")
LOGO_FILE = "brand/datalization-horizontal.png"      # schwarz auf transparent
FOOTER_LINE = ("<span style=\"color:#333333;font-weight:bold;\">Datalization</span> · "
               "Bärengasse 3 · 4800 Zofingen · 076 563 06 08 · "
               "info@datalization.ch · www.datalization.ch")

LAYOUT_ARCH = f"""<t t-name="{LAYOUT_XMLID}">
<t t-if="not o" t-set="o" t-value="doc"/>
<t t-if="not company" t-set="company" t-value="(o and o.company_id) or res_company"/>
<div class="header">
  <table style="width:100%;border:0;border-collapse:collapse;">
    <tr>
      <td style="text-align:left;vertical-align:middle;">
        <img t-if="company.logo" t-att-src="image_data_uri(company.logo)" style="height:12mm;width:auto;" alt="Datalization"/>
      </td>
      <td style="text-align:right;vertical-align:middle;white-space:nowrap;">
        <span style="font-family:'Inter',Arial,sans-serif;font-weight:600;font-size:9.5pt;color:#0A0A0A;letter-spacing:-0.01em;">Einfache Lösungen schaffen</span><span style="display:inline-block;width:4pt;height:4pt;background:#F48B2D;border-radius:50%;margin-left:1.14pt;vertical-align:baseline;"></span>
      </td>
    </tr>
  </table>
</div>
<t t-call="web.external_layout_body"><t t-out="0"/></t>
<div class="footer">
  <div style="border-top:1px solid #dddddd;padding-top:4px;text-align:center;font-size:8pt;color:#666666;">
    {FOOTER_LINE}
  </div>
</div>
</t>"""


class Command(BaseCommand):
    help = "Setzt das unternehmensweite Datalization-Dokumentenlayout in Odoo."

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        # 1) Custom-Layout-View anlegen/aktualisieren
        view = c._execute("ir.ui.view", "search", [["key", "=", LAYOUT_XMLID]], limit=1)
        v_vals = {"name": "Datalization Dokumenten-Layout", "type": "qweb",
                  "key": LAYOUT_XMLID, "arch_db": LAYOUT_ARCH}
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

        # 2) Firmenlogo = horizontale Wortmarke
        logo_path = os.path.join(os.getcwd(), LOGO_FILE)
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()

        # 3) Firma: Logo, Layout, Kopf/Fuss-Felder setzen (vorher merken)
        comp = c._execute("res.company", "search_read", [],
                          fields=["id", "external_report_layout_id"], limit=1)[0]
        prev = comp["external_report_layout_id"]
        c._execute("res.company", "write", [comp["id"]], {
            "logo": logo_b64,
            "external_report_layout_id": view_id,
            "report_header": "<div>Einfache Lösungen schaffen</div>",
            "report_footer": f"<p>{FOOTER_LINE}</p>",
            "primary_color": "#F48B2D",
            "secondary_color": "#0A0A0A",
        })

        self.stdout.write(self.style.SUCCESS(
            f"Dokumentenlayout gesetzt (view {view_id}). Gilt für alle external_layout-Reports."))
        self.stdout.write(f"  Vorheriges Layout (zum Zurücksetzen): {prev}")
