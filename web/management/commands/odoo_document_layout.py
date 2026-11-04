"""Setzt das unternehmensweite Odoo-Dokumenten-Layout (Kopf/Fuss) auf das
Datalization-Design (Vorlage datalization_layout_odoo.xml):
Wortmarke links, Slogan rechts (Text + oranger CSS-Kreis), zentrierte Fusszeile
mit orangen Trennpunkten und Seitenzahl.

Gilt danach für ALLE Reports, die web.external_layout nutzen – Rechnungen,
Offerten, Lieferscheine, CRM-Briefe usw.

Logo (brand/datalization-horizontal.png) → company.logo.

Idempotent. Reversibel: der vorherige external_report_layout_id wird ausgegeben.

    python manage.py odoo_document_layout
"""
import base64
import os

from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

LAYOUT_XMLID = "x_datalization.external_layout_custom"
MODULE, NAME = LAYOUT_XMLID.split(".")
LOGO_FILE = "brand/datalization-horizontal.png"     # schwarz auf transparent → company.logo

# Kopf-/Fuss-Markup aus der Vorlage datalization_layout_odoo.xml (1:1),
# eingebettet in ein eigenständiges external-Layout.
LAYOUT_ARCH = """<t t-name="x_datalization.external_layout_custom">
<t t-if="not o" t-set="o" t-value="doc"/>
<t t-if="not company" t-set="company" t-value="(o and o.company_id) or res_company"/>
<div t-attf-class="header o_company_#{company.id}_layout">
    <div style="display: table; width: 100%; padding-top: 2mm;">
        <div style="display: table-cell; vertical-align: middle;">
            <img t-if="company.logo" t-att-src="image_data_uri(company.logo)" style="height: 9mm;" alt="Logo"/>
        </div>
        <div style="display: table-cell; vertical-align: middle; text-align: right; font-size: 9.5pt; font-weight: 600; color: #0A0A0A; letter-spacing: -0.01em;">
            Einfache Lösungen schaffen<span style="display: inline-block; width: 0.42em; height: 0.42em; border-radius: 50%; background-color: #F48B2D; margin-left: 0.12em;"></span>
        </div>
    </div>
</div>
<t t-call="web.external_layout_body"><t t-out="0"/></t>
<div t-attf-class="footer o_company_#{company.id}_layout">
    <div style="border-top: 0.25mm solid #E4E4E0; padding-top: 3mm; text-align: center; font-size: 7.5pt; color: #4F4F4F;">
        <strong style="color: #0A0A0A; font-weight: 600;">Datalization</strong>
        <span style="color: #F48B2D; padding: 0 1.4mm;">·</span>Bärengasse 3
        <span style="color: #F48B2D; padding: 0 1.4mm;">·</span>4800 Zofingen
        <span style="color: #F48B2D; padding: 0 1.4mm;">·</span>076 563 06 08
        <span style="color: #F48B2D; padding: 0 1.4mm;">·</span>info@datalization.ch
        <span style="color: #F48B2D; padding: 0 1.4mm;">·</span>www.datalization.ch
    </div>
    <div t-if="report_type == 'pdf'" style="text-align: center; font-size: 7pt; color: #8F8F8F; margin-top: 1mm;">
        Seite <span class="page"/> / <span class="topage"/>
    </div>
</div>
</t>"""


class Command(BaseCommand):
    help = "Setzt das unternehmensweite Datalization-Dokumentenlayout in Odoo."

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        with open(os.path.join(os.getcwd(), LOGO_FILE), "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()

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

        comp = c._execute("res.company", "search_read", [],
                          fields=["id", "external_report_layout_id"], limit=1)[0]
        prev = comp["external_report_layout_id"]
        c._execute("res.company", "write", [comp["id"]], {
            "logo": logo_b64,
            "external_report_layout_id": view_id,
            "primary_color": "#F48B2D",
            "secondary_color": "#0A0A0A",
        })

        self.stdout.write(self.style.SUCCESS(
            f"Dokumentenlayout gesetzt (view {view_id}). Gilt für alle external_layout-Reports."))
        self.stdout.write(f"  Vorheriges Layout (zum Zurücksetzen): {prev}")
