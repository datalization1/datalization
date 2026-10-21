"""Tagt neue Bezirk-Zofingen-Gründungen in Odoo mit 'Sponsoring FC Oftringen'.

Läuft im wöchentlichen Mittwoch-Lauf nach dem Odoo-Push. Betrifft NUR echte
SHAB-Neugründungen (nicht den Zefix-Ist-Bestand) im Bezirk Zofingen, die bereits
einen Odoo-Lead haben. Idempotent (Tag wird per (4,id) nur ergänzt).

    python manage.py tag_fc_oftringen
    python manage.py tag_fc_oftringen --dry-run
"""
import time

from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm
from web.models import NewCompany

BEZIRK_ZOFINGEN = [
    "Aarburg", "Bottenwil", "Brittnau", "Kirchleerau", "Kölliken", "Moosleerau",
    "Murgenthal", "Oftringen", "Reitnau", "Rothrist", "Safenwil", "Staffelbach",
    "Strengelbach", "Uerkheim", "Vordemwald", "Wiliberg", "Zofingen",
]
TAG = "Sponsoring FC Oftringen"


class Command(BaseCommand):
    help = "Tagt neue Bezirk-Zofingen-Gründungen in Odoo mit 'Sponsoring FC Oftringen'."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--sleep", type=float, default=0.3)

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        qs = (NewCompany.objects
              .exclude(shab_id__startswith="zefix:")      # nur echte Neugründungen
              .filter(town__in=BEZIRK_ZOFINGEN, odoo_lead_id__isnull=False))
        recs = list(qs)
        self.stdout.write(f"{len(recs)} Bezirk-Zofingen-Neugründungen mit Odoo-Lead.")
        if opts["dry_run"]:
            for r in recs:
                self.stdout.write(f"  ~ würde taggen: {r.name} ({r.town})")
            return

        tag = c.tag_id(TAG)
        done = failed = 0
        for r in recs:
            for attempt in range(4):
                try:
                    c._execute("crm.lead", "write", [r.odoo_lead_id], {"tag_ids": [(4, tag)]})
                    done += 1
                    break
                except Exception as e:
                    if ("429" in str(e) or "Too Many" in str(e)) and attempt < 3:
                        time.sleep(2 ** attempt)
                        continue
                    self.stderr.write(f"  ! {r.name[:30]}: {str(e)[:60]}")
                    failed += 1
                    break
            time.sleep(opts["sleep"])
        self.stdout.write(self.style.SUCCESS(f"Getaggt: {done}, Fehler: {failed}"))
