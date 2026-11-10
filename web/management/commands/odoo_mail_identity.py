"""Setzt die einheitliche Datalization-E-Mail-CI in Odoo (Korrespondenz).

Deckt vier Flächen ab – idempotent, über einen Aufruf:

  1. E-Mail-Signatur am Benutzer (res.users): CI-Block mit „d"-Logo, Name/Rolle,
     Kontakt und Slogan. Das Benachrichtigungs-Layout UND die Sales-Vorlagen
     hängen diese Signatur automatisch an jede Mail an → trägt die CI überall.
  2. E-Mail-Button-Farben der Firma (email_primary/secondary_color): Button
     dunkel (#0A0A0A) mit weisser Schrift statt Odoo-Lila.
  3. Allgemeine Korrespondenz-Vorlage (mail.template auf res.partner): leere,
     CI-gerahmte Mail für freie Briefe – Anrede + Platz für den Text; die
     Signatur kommt automatisch dazu.
  4. Modell-Mails eindeutschen: Offerte (36), Pro-forma (37), Auftrags-
     bestätigung (38), Gutschrift (16). Rechnung (14) ist bereits Deutsch.
     Nur sichtbarer Text wird ersetzt – QWeb-Felder/Buttons bleiben unberührt.

Reversibel: vorherige Farben/Signatur werden ausgegeben.

    python manage.py odoo_mail_identity
"""
from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

LOGO_URL = "https://datalization.ch/static/email/datalization-email-logo.png"

# --- 1) CI-Signatur (Tabelle = maximale Mailclient-Kompatibilität) ---------
SIGNATURE_HTML = f"""<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:Arial,Helvetica,sans-serif;margin-top:6px;">
<tr>
<td style="padding:0 14px 0 0;vertical-align:top;"><img src="{LOGO_URL}" width="48" height="46" alt="Datalization" style="display:block;border:0;width:48px;height:auto;"></td>
<td style="padding:0 0 0 14px;border-left:1px solid #DDDDDD;vertical-align:top;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:18px;color:#0A0A0A;">
<strong style="font-size:14px;color:#0A0A0A;">Datalization</strong><br>
<span>076 563 06 08</span><br>
<a href="https://datalization.ch" style="color:#0A0A0A;text-decoration:none;">www.datalization.ch</a><br>
<span style="color:#555555;">B&auml;rengasse 3, 4800 Zofingen</span>
</td>
</tr>
<tr><td colspan="2" style="padding:10px 0 0 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#F48B2D;font-weight:bold;">Einfache L&ouml;sungen schaffen<span style="color:#F48B2D;">&#9679;</span></td></tr>
</table>""".strip()

# --- 2) E-Mail-Button-Farben ------------------------------------------------
EMAIL_PRIMARY = "#FFFFFF"   # Button-Textfarbe
EMAIL_SECONDARY = "#0A0A0A"  # Button-Hintergrund (CI-Dunkel)

# --- 3) Allgemeine Korrespondenz-Vorlage ------------------------------------
CORRESPONDENCE_NAME = "Datalization – Korrespondenz"
CORRESPONDENCE_SUBJECT = "Nachricht von Datalization"
# Signatur wird von Odoo automatisch angehängt → hier nur Anrede + Platzhalter.
CORRESPONDENCE_BODY = """
<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.6;color:#1a1a1a;">
  <p>Guten Tag<t t-if="object.name"> <t t-out="object.name or ''"/></t></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
  <p>Freundliche Gr&uuml;sse</p>
</div>
""".strip()

# --- 4) Eindeutschung der Modell-Mails (nur sichtbarer Text) ----------------
REPLACEMENTS = {
    # Betreff-Token
    "'Quotation'": "'Offerte'",
    "'Pro Forma'": "'Proforma'",
    "'Order'": "'Auftrag'",
    " Order {{": " Auftrag {{",
    "Credit Note (Ref": "Gutschrift (Ref",
    "Credit Note": "Gutschrift",
    # Anrede
    "Hello <t": "Guten Tag <t",
    "Hello,": "Guten Tag,",
    # Offerte/Auftrag
    "Your quotation": "Ihre Offerte",
    "Your Pro forma invoice for quotation": "Ihre Proforma-Rechnung zur Offerte",
    "Your Pro forma invoice for order": "Ihre Proforma-Rechnung zum Auftrag",
    "Your order": "Ihr Auftrag",
    "is ready for review.": "liegt zur Ansicht für Sie bereit.",
    "is available.": "liegt für Sie bereit.",
    "amounting in": "über",
    "(with reference:": "(Referenz:",
    "with reference:": "Referenz:",
    # Auftragsbestätigung
    "has been confirmed and will be ready on": "wurde bestätigt und ist bereit am",
    "has been confirmed and will be ready soon.": "wurde bestätigt und ist in Kürze bereit.",
    "has been confirmed.": "wurde bestätigt.",
    "Thank you for your trust.": "Herzlichen Dank für Ihr Vertrauen.",
    "is pending. It will be confirmed when the payment is received.":
        "ist in Bearbeitung und wird nach Zahlungseingang bestätigt.",
    "Your payment reference is": "Ihre Zahlungsreferenz lautet",
    # Dokumente / Schluss
    "Here are some additional documents that may interest you:":
        "Weitere Dokumente, die Sie interessieren könnten:",
    "Here is an additional document that may interest you:":
        "Ein weiteres Dokument, das Sie interessieren könnte:",
    "Do not hesitate to contact us if you have any questions.":
        "Bei Fragen stehen wir Ihnen gerne zur Verfügung.",
}
SALES_TEMPLATE_IDS = [36, 37, 38, 16]  # Offerte, Pro-forma, Auftragsbest., Gutschrift


def _germanize(text):
    if not text:
        return text, 0
    n = 0
    for en, de in REPLACEMENTS.items():
        if en in text:
            n += text.count(en)
            text = text.replace(en, de)
    return text, n


class Command(BaseCommand):
    help = "Setzt die einheitliche Datalization-E-Mail-CI (Signatur, Farben, Korrespondenz, Modell-Mails)."

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        # 1) Signatur am Benutzer ------------------------------------------
        u = c._execute("res.users", "read", [c.uid], fields=["name", "signature"])[0]
        prev_sig = (u.get("signature") or "")[:60]
        c._execute("res.users", "write", [c.uid], {"signature": SIGNATURE_HTML})
        self.stdout.write(self.style.SUCCESS(
            f"1) Signatur gesetzt für {u['name']} (uid {c.uid})."))
        self.stdout.write(f"   Vorher: {prev_sig!r}")

        # 2) E-Mail-Button-Farben ------------------------------------------
        comp = c._execute("res.company", "read", [1],
                          fields=["email_primary_color", "email_secondary_color"])[0]
        c._execute("res.company", "write", [1], {
            "email_primary_color": EMAIL_PRIMARY,
            "email_secondary_color": EMAIL_SECONDARY,
        })
        self.stdout.write(self.style.SUCCESS(
            f"2) E-Mail-Farben: Button {EMAIL_SECONDARY} / Text {EMAIL_PRIMARY}."))
        self.stdout.write(f"   Vorher: primary={comp['email_primary_color']}, "
                          f"secondary={comp['email_secondary_color']}")

        # 3) Korrespondenz-Vorlage -----------------------------------------
        partner_model = c._execute("ir.model", "search",
                                   [["model", "=", "res.partner"]], limit=1)
        if not partner_model:
            raise CommandError("Modell res.partner nicht gefunden.")
        vals = {
            "name": CORRESPONDENCE_NAME,
            "model_id": partner_model[0],
            "subject": CORRESPONDENCE_SUBJECT,
            "body_html": CORRESPONDENCE_BODY,
            "email_from": "{{ (user.email_formatted or object.company_id.email_formatted) }}",
            "use_default_to": True,
        }
        existing = c._execute("mail.template", "search",
                              [["name", "=", CORRESPONDENCE_NAME]], limit=1)
        if existing:
            c._execute("mail.template", "write", existing, vals)
            self.stdout.write(self.style.SUCCESS(
                f"3) Korrespondenz-Vorlage aktualisiert (id {existing[0]})."))
        else:
            tid = c._execute("mail.template", "create", vals)
            self.stdout.write(self.style.SUCCESS(
                f"3) Korrespondenz-Vorlage angelegt (id {tid})."))

        # 4) Modell-Mails eindeutschen -------------------------------------
        self.stdout.write(self.style.SUCCESS("4) Modell-Mails eindeutschen:"))
        for tid in SALES_TEMPLATE_IDS:
            rec = c._execute("mail.template", "read", [tid],
                             fields=["name", "subject", "body_html"])
            if not rec:
                self.stdout.write(f"   [{tid}] fehlt – übersprungen.")
                continue
            t = rec[0]
            new_subj, ns = _germanize(t.get("subject"))
            new_body, nb = _germanize(t.get("body_html"))
            if ns or nb:
                c._execute("mail.template", "write", [tid],
                           {"subject": new_subj, "body_html": new_body})
                self.stdout.write(
                    f"   [{tid}] {t['name']}: {ns} im Betreff, {nb} im Text ersetzt.")
            else:
                self.stdout.write(f"   [{tid}] {t['name']}: bereits Deutsch.")

        self.stdout.write(self.style.SUCCESS("\nFertig. CI-E-Mail-Identität gesetzt."))
