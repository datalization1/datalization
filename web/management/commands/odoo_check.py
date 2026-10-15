"""Testet die Odoo-Verbindung: Authentifizierung + crm.lead-Zugriff.

    python manage.py odoo_check                 # nur prüfen
    python manage.py odoo_check --create-test   # zusätzlich einen Test-Lead anlegen
"""
from django.core.management.base import BaseCommand

from web import odoo_crm


class Command(BaseCommand):
    help = "Testet die Odoo-Verbindung (Auth + crm.lead-Zugriff)."

    def add_arguments(self, parser):
        parser.add_argument("--create-test", action="store_true",
                            help="Legt einen Test-Lead an (danach in Odoo löschen).")

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            self.stderr.write(self.style.ERROR(
                "Odoo nicht konfiguriert – ODOO_URL/ODOO_DB/ODOO_USERNAME/"
                "ODOO_API_KEY in der .env setzen."))
            return
        try:
            c = odoo_crm.OdooClient()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Verbindung/Auth fehlgeschlagen: {e}"))
            return
        self.stdout.write(self.style.SUCCESS(f"Auth OK – uid={c.uid}  ({c.url}, db={c.db})"))
        try:
            can = c._execute("crm.lead", "check_access_rights", "create",
                             raise_exception=False)
            self.stdout.write(f"crm.lead anlegen erlaubt: {can}")
        except Exception as e:
            self.stderr.write(self.style.WARNING(f"crm.lead-Zugriff unklar: {e}"))
        self.stdout.write(f"Land CH (country_id): {c.country_ch_id()}")

        if opts["create_test"]:
            try:
                lead_id = c._execute("crm.lead", "create", {
                    "name": "Datalization – Testlead (bitte löschen)",
                    "type": "lead",
                })
                self.stdout.write(self.style.SUCCESS(
                    f"Test-Lead angelegt: id={lead_id} → in Odoo unter CRM prüfen "
                    f"und wieder löschen."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Test-Lead fehlgeschlagen: {e}"))
