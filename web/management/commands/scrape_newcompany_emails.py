"""E-Mail der SHAB-Neugründungen von deren (via Google gefundenen) Website scrapen."""
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.core.management.base import BaseCommand

from web.email_scrape import scrape_site
from web.models import NewCompany


class Command(BaseCommand):
    help = "Scrapt E-Mails der Neugründungen von ihren Websites (Impressum/Kontakt)."

    def add_arguments(self, parser):
        parser.add_argument("--towns", default="")
        parser.add_argument("--active-only", action="store_true")
        parser.add_argument("--days", type=int, default=0,
                            help="Nur Firmen mit Gründungsdatum der letzten N Tage (0 = alle).")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--workers", type=int, default=12)

    def handle(self, *args, **opts):
        qs = NewCompany.objects.exclude(website="").filter(email="")
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
        records = list(qs)
        total = len(records)
        self.stdout.write(f"{total} Neugründungen mit Website, ohne E-Mail – scrape …")

        done = found = 0
        batch = []
        with ThreadPoolExecutor(max_workers=opts["workers"]) as ex:
            futures = {ex.submit(scrape_site, r.website): r for r in records}
            for fut in as_completed(futures):
                r = futures[fut]
                done += 1
                try:
                    email = fut.result()
                except Exception:
                    email = ""
                if email:
                    r.email = email[:200]
                    batch.append(r)
                    found += 1
                if len(batch) >= 50:
                    NewCompany.objects.bulk_update(batch, ["email"]); batch = []
                if done % 50 == 0:
                    self.stdout.write(f"  … {done}/{total}, gefunden {found}", ending="\r")
                    self.stdout.flush()
            if batch:
                NewCompany.objects.bulk_update(batch, ["email"])
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Fertig: {found} E-Mails gefunden (von {total})."))
