"""Legt/aktualisiert die Odoo-E-Mail-Vorlage für den Neugründungs-Erstkontakt an.

Vorlage hängt an crm.lead; der Firmenname wird dynamisch eingesetzt
(QWeb <t t-out="object.partner_name or object.name"/>). Beim Senden in Odoo:
Chance öffnen → E-Mail → Vorlage 'Datalization – Neugründung Erstkontakt' laden
→ prüfen → senden.

Idempotent: wird über den Namen gesucht und aktualisiert.

    python manage.py odoo_mail_template
"""
from django.core.management.base import BaseCommand, CommandError

from leadgen import odoo_crm

CRM_LEAD_MODEL_ID = 2655
TEMPLATE_NAME = "Datalization – Neugründung Erstkontakt"
SUBJECT = "Herzlichen Glückwunsch zur Gründung von {{ object.partner_name or object.name }}"
LOGO_URL = "https://datalization.ch/static/email/datalization-email-logo.png"

BODY_HTML = f"""
<div style="background:#ffffff;max-width:560px;margin:0 auto;padding:28px 32px;border-radius:6px;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#1a1a1a;">
  <p>Guten Tag</p>
  <p>herzlichen Gl&uuml;ckwunsch zur Gr&uuml;ndung von
     <strong><t t-out="object.partner_name or object.name">Ihre Firma</t></strong> &ndash;
     wir haben Ihren Eintrag im Handelsregister (SHAB) gesehen und w&uuml;nschen Ihnen einen guten Start.</p>
  <p>Wir sind <strong>Datalization</strong> aus der Region Zofingen und bauen f&uuml;r kleine Betriebe
     die ganze digitale Basis auf &ndash; von der IT-Infrastruktur bis zu den Abl&auml;ufen:</p>
  <ul style="padding-left:20px;margin:12px 0;">
    <li>Komplette <strong>IT aus einer Hand</strong>: Hardware beschaffen, Software-Lizenzen,
        Einrichtung und laufender Betrieb (<strong>Managed IT</strong>)</li>
    <li>Offerten, Rechnungen und Buchhaltung ohne Zettelwirtschaft</li>
    <li>Kundenverwaltung (CRM) &ndash; h&auml;ufig mit <strong>Odoo</strong></li>
    <li>wiederkehrende Abl&auml;ufe automatisieren &ndash; mehr Zeit f&uuml;rs Kerngesch&auml;ft</li>
  </ul>
  <p>Gerade am Anfang spart ein durchdachtes Setup sp&auml;ter viel Zeit und &Auml;rger.</p>
  <p>Wenn Sie m&ouml;gen, zeigen wir Ihnen in einem <strong>kostenlosen 30-min&uuml;tigen Erstgespr&auml;ch</strong>
     unverbindlich, was f&uuml;r Ihren Betrieb sinnvoll ist.</p>
  <p style="margin-top:20px;">Freundliche Gr&uuml;sse<br>Tihomir Danesic</p>
  <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;margin-top:4px;">
  <tr>
  <td style="padding:0 14px 0 0;vertical-align:top;"><img src="{LOGO_URL}" width="50" height="48" alt="Datalization" style="display:block;border:0;width:50px;height:auto;"></td>
  <td style="padding:0 0 0 14px;border-left:1px solid #DDDDDD;vertical-align:top;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#0A0A0A;">
  <strong style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#0A0A0A;">Datalization</strong><br>
  <span style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#0A0A0A;">076 563 06 08</span><br>
  <a href="mailto:info@datalization.ch" style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#0A0A0A;text-decoration:none;">info@datalization.ch</a><br>
  <a href="https://datalization.ch" style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#0A0A0A;text-decoration:none;">www.datalization.ch</a><br>
  <span style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#555555;">B&auml;rengasse 3<br>4800 Zofingen</span>
  </td>
  </tr>
  <tr><td colspan="2" style="padding:12px 0 0 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#F48B2D;font-weight:bold;">Einfache L&ouml;sungen schaffen.</td></tr>
  </table>
  <p style="font-size:12px;color:#999;border-top:1px solid #eee;padding-top:12px;margin-top:20px;">
    Kein Interesse? Eine kurze Antwort gen&uuml;gt und Sie h&ouml;ren nichts mehr von uns.
  </p>
</div>
""".strip()


class Command(BaseCommand):
    help = "Legt/aktualisiert die Odoo-E-Mail-Vorlage für Neugründungs-Erstkontakt."

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()
        vals = {
            "name": TEMPLATE_NAME,
            "model_id": CRM_LEAD_MODEL_ID,
            "subject": SUBJECT,
            "body_html": BODY_HTML,
            "email_from": "info@datalization.ch",
            "use_default_to": True,
        }
        existing = c._execute("mail.template", "search",
                              [["name", "=", TEMPLATE_NAME]], limit=1)
        if existing:
            c._execute("mail.template", "write", existing, vals)
            self.stdout.write(self.style.SUCCESS(f"Vorlage aktualisiert (id {existing[0]})."))
        else:
            tid = c._execute("mail.template", "create", vals)
            self.stdout.write(self.style.SUCCESS(f"Vorlage angelegt (id {tid})."))
