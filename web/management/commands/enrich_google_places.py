"""Telefon/Website von Neugründungs-Leads via Google Places anreichern.

Sucht je Firma „Name, Adresse" und übernimmt Telefon + Website, wenn der Ort
in der gefundenen Adresse übereinstimmt (Schutz vor Falschtreffern).

    python manage.py enrich_google_places --active-only
    python manage.py enrich_google_places --towns "Zofingen,Oftringen" --update-odoo
    python manage.py enrich_google_places --limit 20 --dry-run
"""
import time

from django.core.management.base import BaseCommand, CommandError

from web import google_places, odoo_crm
from web.models import NewCompany


class Command(BaseCommand):
    help = "Reichert NewCompany-Leads via Google Places mit Telefon/Website an."

    def add_arguments(self, parser):
        parser.add_argument("--towns", default="", help="Komma-Liste von Orten (sonst alle).")
        parser.add_argument("--active-only", action="store_true",
                            help="Nur Firmen mit Register-Status ACTIVE.")
        parser.add_argument("--all", action="store_true",
                            help="Auch Firmen anreichern, die schon ein Telefon haben.")
        parser.add_argument("--update-odoo", action="store_true",
                            help="Gefundene Telefone/Websites auch in Odoo aktualisieren.")
        parser.add_argument("--limit", type=int, default=0)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        if not google_places.enabled():
            raise CommandError("GOOGLE_PLACES_API_KEY fehlt in der .env.")

        qs = NewCompany.objects.all()
        if opts["towns"]:
            qs = qs.filter(town__in=[t.strip() for t in opts["towns"].split(",") if t.strip()])
        if opts["active_only"]:
            qs = qs.filter(zefix_status="ACTIVE")
        if not opts["all"]:
            qs = qs.filter(phone="")
        qs = qs.order_by("town", "name")
        if opts["limit"]:
            qs = qs[:opts["limit"]]
        recs = list(qs)
        self.stdout.write(f"{len(recs)} Leads zu prüfen …")

        client = None
        if opts["update_odoo"] and not opts["dry_run"] and odoo_crm.enabled():
            client = odoo_crm.OdooClient()

        found = miss = err = 0
        for r in recs:
            query = ", ".join(x for x in [
                r.name,
                " ".join(y for y in [r.street, r.house_number] if y),
                f"{r.zip_code} {r.town}".strip()] if x)
            res = google_places.lookup(query)
            if res and res.get("error"):
                err += 1
                self.stderr.write("  ! " + res["error"])
                if "429" in res["error"] or "RESOURCE_EXHAUSTED" in res["error"]:
                    time.sleep(3)
                continue
            addr = (res or {}).get("address", "").lower()
            phone = (res or {}).get("phone", "")
            # Ort-Match als Schutz vor Falschtreffern
            if not phone or (r.town and r.town.lower() not in addr):
                miss += 1
                continue
            r.phone = phone[:40]
            if res.get("website") and not r.website:
                r.website = res["website"][:200]
            found += 1
            if not opts["dry_run"]:
                r.save(update_fields=["phone", "website"])
                if client and r.odoo_lead_id:
                    try:
                        client._execute("crm.lead", "write", [r.odoo_lead_id],
                                        {"phone": r.phone, "website": r.website or False})
                    except Exception as e:
                        self.stderr.write(f"  ~ Odoo {r.name}: {str(e)[:60]}")
            self.stdout.write(f"  + {r.name[:30]:31} ☎ {r.phone}")
            time.sleep(0.1)

        self.stdout.write(self.style.SUCCESS(
            f"Telefon gefunden: {found}, kein Treffer: {miss}, Fehler: {err}"))
