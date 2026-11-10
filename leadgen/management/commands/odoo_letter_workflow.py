"""Richtet die wöchentliche Brief-Routine in Odoo ein (Stapeldruck + Tracking).

Zwei Hilfen in der CRM-Leads-Ansicht:

1. Gespeicherter Filter „📬 Brief-Kandidaten" – Leads ohne E-Mail, mit Strasse,
   Tag 'Datalization', noch NICHT 'Brief versendet'. Ein Klick in den Favoriten.
2. Server-Aktion „📬 Als Brief versendet markieren" – setzt bei den markierten
   Leads das Tag 'Brief versendet' (erscheint im Aktionen-Menü ⚙ bei Auswahl).

Wochenroutine: Leads → Favorit „📬 Brief-Kandidaten" → markieren → Drucken →
'Erstkontakt-Brief' (ein PDF mit allen) → drucken/unterschreiben/Visitenkarte →
dieselben markieren → ⚙ „Als Brief versendet markieren".

Idempotent (über Namen gesucht/aktualisiert).

    python manage.py odoo_letter_workflow
"""
from django.core.management.base import BaseCommand, CommandError

from leadgen import odoo_crm

CRM_LEAD_MODEL_ID = 2655
LEADS_ACTION_ID = 249           # CRM → Leads (Listenansicht)
TAG_DATALIZATION = 2
TAG_BRIEF_VERSENDET = 7

FILTER_NAME = "📬 Brief-Kandidaten"
FILTER_DOMAIN = ("[['email_from','=',False],['street','!=',False],"
                 "['tag_ids','in',%d],['tag_ids','not in',%d]]"
                 % (TAG_DATALIZATION, TAG_BRIEF_VERSENDET))

ACTION_NAME = "📬 Als Brief versendet markieren"
ACTION_CODE = f"records.write({{'tag_ids': [(4, {TAG_BRIEF_VERSENDET})]}})"


class Command(BaseCommand):
    help = "Richtet Brief-Filter + 'Brief versendet'-Aktion in Odoo ein."

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        # 1) Gespeicherter Filter (persönlich, erscheint in Favoriten) ------
        f_vals = {"name": FILTER_NAME, "model_id": "crm.lead",
                  "domain": FILTER_DOMAIN, "user_ids": [(6, 0, [c.uid])],
                  "action_id": LEADS_ACTION_ID, "is_default": False}
        existing = c._execute("ir.filters", "search", [["name", "=", FILTER_NAME],
                                                       ["model_id", "=", "crm.lead"]], limit=1)
        if existing:
            c._execute("ir.filters", "write", existing, f_vals)
            fid = existing[0]
            self.stdout.write(self.style.SUCCESS(f"1) Filter aktualisiert (id {fid})."))
        else:
            fid = c._execute("ir.filters", "create", f_vals)
            self.stdout.write(self.style.SUCCESS(f"1) Filter angelegt (id {fid})."))

        # 2) Server-Aktion 'Brief versendet' --------------------------------
        a_vals = {"name": ACTION_NAME, "model_id": CRM_LEAD_MODEL_ID,
                  "state": "code", "code": ACTION_CODE,
                  "binding_model_id": CRM_LEAD_MODEL_ID, "binding_type": "action"}
        a_exist = c._execute("ir.actions.server", "search", [["name", "=", ACTION_NAME]], limit=1)
        if a_exist:
            c._execute("ir.actions.server", "write", a_exist, a_vals)
            aid = a_exist[0]
            self.stdout.write(self.style.SUCCESS(f"2) Server-Aktion aktualisiert (id {aid})."))
        else:
            aid = c._execute("ir.actions.server", "create", a_vals)
            self.stdout.write(self.style.SUCCESS(f"2) Server-Aktion angelegt (id {aid})."))

        # Zählung
        n = c._execute("crm.lead", "search_count", [
            ["email_from", "=", False], ["street", "!=", False],
            ["tag_ids", "in", TAG_DATALIZATION], ["tag_ids", "not in", TAG_BRIEF_VERSENDET]])
        self.stdout.write(f"\nAktuell {n} offene Brief-Kandidaten im Filter.")
