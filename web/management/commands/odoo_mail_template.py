"""Legt/aktualisiert die Odoo-E-Mail-Vorlage für den Neugründungs-Erstkontakt an.

Vorlage hängt an crm.lead; der Firmenname wird dynamisch eingesetzt
({{ object.partner_name }}). Beim Senden in Odoo: Chance öffnen → E-Mail →
Vorlage 'Datalization – Neugründung Erstkontakt' laden → prüfen → senden.

Idempotent: wird über den Namen gesucht und aktualisiert.

    python manage.py odoo_mail_template
"""
from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

CRM_LEAD_MODEL_ID = 2655
TEMPLATE_NAME = "Datalization – Neugründung Erstkontakt"
SUBJECT = "Herzlichen Glückwunsch zur Gründung von {{ object.partner_name or object.name }}"

BODY_HTML = """
<div style="max-width:560px;margin:0 auto;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#1a1a1a;">
  <p>Guten Tag</p>
  <p>herzlichen Gl&uuml;ckwunsch zur Gr&uuml;ndung von <strong>{{ object.partner_name or object.name }}</strong> &ndash;
     wir haben Ihren Eintrag im Handelsregister (SHAB) gesehen und w&uuml;nschen Ihnen einen guten Start.</p>
  <p>Wir sind <strong>Datalization</strong> aus der Region Zofingen und helfen kleinen Betrieben, von Anfang an
     eine einfache, saubere digitale Basis aufzubauen:</p>
  <ul style="padding-left:20px;margin:12px 0;">
    <li>Offerten, Rechnungen und Buchhaltung ohne Zettelwirtschaft</li>
    <li>Kundenverwaltung (CRM) &ndash; h&auml;ufig mit <strong>Odoo</strong></li>
    <li>wiederkehrende Abl&auml;ufe automatisieren &ndash; mehr Zeit f&uuml;rs Kerngesch&auml;ft</li>
  </ul>
  <p>Gerade am Anfang spart ein durchdachtes Setup sp&auml;ter viel Zeit und &Auml;rger.
     Unser Leitsatz: <em>einfache L&ouml;sungen schaffen.</em></p>
  <p>Wenn Sie m&ouml;gen, zeigen wir Ihnen in einem <strong>kostenlosen 30-min&uuml;tigen Erstgespr&auml;ch</strong>
     unverbindlich, was f&uuml;r Ihren Betrieb sinnvoll ist.</p>
  <p style="margin-top:20px;">Freundliche Gr&uuml;sse<br><strong>Datalization</strong></p>
  <p style="font-size:13px;color:#555;margin-top:4px;">
    <a href="mailto:info@datalization.ch" style="color:#0a7d8c;text-decoration:none;">info@datalization.ch</a> &middot;
    <a href="https://datalization.ch" style="color:#0a7d8c;text-decoration:none;">datalization.ch</a>
  </p>
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
