"""Aktualisiert Telefon/E-Mail/Website bereits gepushter Neugründungen in Odoo.

Die wöchentliche Nach-Anreicherung (Google Places / Website-Scrape) füllt bei
schon nach Odoo gepushten Leads neue Kontaktdaten nach. Dieser Befehl schreibt
diese Felder in den vorhandenen crm.lead – gedrosselt, mit Backoff gegen die
Rate-Limits der Odoo-SaaS-Trial.

    python manage.py sync_odoo_contacts --days 120
    python manage.py sync_odoo_contacts --towns "Zofingen,Oftringen" --dry-run
"""
import time

from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm
from web.models import NewCompany


class Command(BaseCommand):
    help = "Synchronisiert Telefon/E-Mail/Website gepushter Neugründungen nach Odoo."

    def add_arguments(self, parser):
        parser.add_argument("--towns", default="", help="Komma-Liste von Orten (sonst alle).")
        parser.add_argument("--days", type=int, default=0,
                            help="Nur Firmen mit Gründungsdatum der letzten N Tage (0 = alle).")
        parser.add_argument("--active-only", action="store_true")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--sleep", type=float, default=0.4,
                            help="Pause zwischen Writes in Sekunden (Default 0.4).")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert (ODOO_URL/DB/USERNAME/API_KEY).")

        from django.db.models import Q
        qs = (NewCompany.objects
              .filter(odoo_lead_id__isnull=False)
              .filter(Q(phone__gt="") | Q(email__gt="") | Q(website__gt="")))
        if opts["towns"]:
            qs = qs.filter(town__in=[t.strip() for t in opts["towns"].split(",") if t.strip()])
        if opts["active_only"]:
            qs = qs.filter(zefix_status="ACTIVE")
        if opts["days"]:
            from datetime import timedelta
            from django.utils import timezone
            cutoff = (timezone.now() - timedelta(days=opts["days"])).date()
            qs = qs.filter(publication_date__gte=cutoff)
        qs = qs.order_by("town", "name")
        if opts["limit"]:
            qs = qs[:opts["limit"]]
        recs = list(qs)
        self.stdout.write(f"{len(recs)} gepushte Leads mit Kontaktdaten zu synchronisieren …")

        client = None if opts["dry_run"] else odoo_crm.OdooClient()
        done = skipped = failed = 0
        for r in recs:
            vals = {}
            if r.phone:
                vals["phone"] = r.phone
            if r.email:
                vals["email_from"] = r.email
            if r.website:
                vals["website"] = r.website
            if not vals:
                skipped += 1
                continue
            if opts["dry_run"]:
                self.stdout.write(f"  ~ {r.name[:30]:31} {vals}")
                done += 1
                continue
            ok = False
            for attempt in range(4):
                try:
                    client._execute("crm.lead", "write", [r.odoo_lead_id], vals)
                    ok = True
                    break
                except Exception as e:
                    msg = str(e)
                    if ("429" in msg or "Too Many Requests" in msg) and attempt < 3:
                        time.sleep(2 ** attempt)  # 1, 2, 4 s Backoff
                        continue
                    self.stderr.write(f"  ! {r.name[:30]}: {msg[:70]}")
                    break
            if ok:
                done += 1
            else:
                failed += 1
            time.sleep(opts["sleep"])

        self.stdout.write(self.style.SUCCESS(
            f"Synchronisiert: {done}, übersprungen: {skipped}, fehlgeschlagen: {failed}"))
