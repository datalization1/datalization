"""Pusht importierte Leads gebündelt (Batch) nach Odoo CRM.

    python manage.py push_leads_odoo --model acquisition
    python manage.py push_leads_odoo --model realestate
    python manage.py push_leads_odoo --model all
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from web import odoo_crm
from web.models import AcquisitionLead, NewCompany, RealEstateLead


class Command(BaseCommand):
    help = "Pusht AcquisitionLead/RealEstateLead gebündelt nach Odoo CRM."

    def add_arguments(self, parser):
        parser.add_argument("--model", choices=["acquisition", "realestate", "shab", "all"],
                            default="all")
        parser.add_argument("--chunk", type=int, default=80,
                            help="Datensätze pro API-Call (Default 80).")
        parser.add_argument("--limit", type=int, default=0,
                            help="Max. Datensätze (0 = alle).")

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert (ODOO_URL/DB/USERNAME/API_KEY).")
        client = odoo_crm.OdooClient()
        self.stdout.write(self.style.SUCCESS(f"Odoo verbunden (uid={client.uid})."))

        targets = []
        if opts["model"] in ("shab", "all"):
            targets.append(("Neugründungen", NewCompany, client.shab_vals))
        if opts["model"] in ("acquisition", "all"):
            targets.append(("Akquise", AcquisitionLead, client.acq_vals))
        if opts["model"] in ("realestate", "all"):
            targets.append(("Immobilien", RealEstateLead, client.broker_vals))

        for label, Model, builder in targets:
            qs = Model.objects.filter(odoo_lead_id__isnull=True).order_by("pk")
            if opts["limit"]:
                qs = qs[:opts["limit"]]
            records = list(qs)
            total = len(records)
            self.stdout.write(f"{label}: {total} zu pushen …")
            done = failed = 0
            for i in range(0, total, opts["chunk"]):
                chunk = records[i:i + opts["chunk"]]
                try:
                    vals = [builder(r) for r in chunk]
                    ids = client.create_many(vals)
                    now = timezone.now()
                    for r, lid in zip(chunk, ids):
                        r.odoo_lead_id = lid
                        r.odoo_synced_at = now
                    Model.objects.bulk_update(chunk, ["odoo_lead_id", "odoo_synced_at"])
                    done += len(ids)
                except Exception as e:
                    failed += len(chunk)
                    self.stderr.write(f"  ! Batch {i}-{i+len(chunk)}: {e}")
                self.stdout.write(f"  … {done}/{total}", ending="\r")
                self.stdout.flush()
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS(
                f"{label}: {done} gepusht, {failed} fehlgeschlagen."))
