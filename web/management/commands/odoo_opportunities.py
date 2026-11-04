"""Konvertiert Datalization-Leads in Odoo zu Chancen (Opportunities) und legt
für anschreibbare Firmen eine E-Mail-Aktivität an.

Umfang (Datalization-Universum):
  * echte SHAB-Neugründungen (ohne Zefix-Ist-Bestand) mit Odoo-Lead
  * kuratierte Akquise-Leads mit Priorität A/B/C (nicht Monekey/Partner)

E-Mail-Aktivität NUR für 🟡 "Firma generisch" (AG/GmbH mit info@/kontakt@) –
rechtlich (UWG/revDSG) der einzige sauber kalt-anschreibbare Teil. Einzel-
unternehmen/persönliche Adressen (🔴) bekommen KEINE Massenmail-Aktivität.

Idempotent: bereits konvertierte Chancen und bereits vorhandene E-Mail-
Aktivitäten werden übersprungen.

    python manage.py odoo_opportunities --dry-run
    python manage.py odoo_opportunities
"""
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from web import odoo_crm
from web.management.commands.export_newcompanies import contact_risk
from web.models import AcquisitionLead, NewCompany

EMAIL_ACTIVITY_TYPE_ID = 1          # mail.activity.type "Email"
CRM_LEAD_MODEL_ID = 2655            # ir.model crm.lead
MAILBAR = "🟡 Firma generisch"


def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


class Command(BaseCommand):
    help = "Datalization-Leads → Chancen + E-Mail-Aktivität (🟡 Firma generisch)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--no-activity", action="store_true",
                            help="Nur konvertieren, keine E-Mail-Aktivitäten.")
        parser.add_argument("--activity-days", type=int, default=3,
                            help="Fälligkeit der E-Mail-Aktivität in Tagen (Default 3).")

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()
        dry = opts["dry_run"]

        # --- Zielmenge zusammenstellen ---------------------------------------
        shab = list(NewCompany.objects
                    .exclude(shab_id__startswith="zefix:")
                    .filter(odoo_lead_id__isnull=False))
        acq = list(AcquisitionLead.objects
                   .filter(odoo_lead_id__isnull=False,
                           priority__in=["A", "B", "C", "a", "b", "c"]))
        target_ids = [r.odoo_lead_id for r in shab] + [r.odoo_lead_id for r in acq]
        self.stdout.write(f"Zielmenge: {len(shab)} SHAB-Neugründungen + "
                          f"{len(acq)} Akquise-Leads (A/B/C) = {len(target_ids)} Chancen.")

        # --- Welche sind noch 'lead' (nicht schon Chance)? -------------------
        still_lead = []
        for chunk in _chunks(target_ids, 200):
            rows = c._execute("crm.lead", "read", chunk, fields=["id", "type"])
            still_lead += [r["id"] for r in rows if r.get("type") == "lead"]
        self.stdout.write(f"  davon noch Lead (werden konvertiert): {len(still_lead)}, "
                          f"bereits Chance: {len(target_ids) - len(still_lead)}")

        # --- Konvertieren ----------------------------------------------------
        if still_lead and not dry:
            for chunk in _chunks(still_lead, 100):
                c._execute("crm.lead", "write", chunk, {"type": "opportunity"})
            self.stdout.write(self.style.SUCCESS(f"  → {len(still_lead)} Leads zu Chancen konvertiert."))
        elif still_lead:
            self.stdout.write(f"  [dry-run] würde {len(still_lead)} Leads konvertieren.")

        # --- E-Mail-Aktivitäten (nur 🟡 Firma generisch) ---------------------
        if opts["no_activity"]:
            self.stdout.write("E-Mail-Aktivitäten übersprungen (--no-activity).")
            return

        mailbar = [r for r in shab
                   if r.email and contact_risk(r) == MAILBAR and r.odoo_lead_id]
        mailbar_ids = [r.odoo_lead_id for r in mailbar]
        self.stdout.write(f"Anschreibbar (🟡 Firma generisch, mit E-Mail): {len(mailbar)}")

        # bereits vorhandene E-Mail-Aktivitäten (idempotent)
        existing = set()
        for chunk in _chunks(mailbar_ids, 200):
            rows = c._execute("mail.activity", "search_read",
                              [["res_model", "=", "crm.lead"],
                               ["activity_type_id", "=", EMAIL_ACTIVITY_TYPE_ID],
                               ["res_id", "in", chunk]],
                              fields=["res_id"])
            existing.update(r["res_id"] for r in rows)
        todo = [r for r in mailbar if r.odoo_lead_id not in existing]
        self.stdout.write(f"  bereits mit E-Mail-Aktivität: {len(existing)}, "
                          f"neu anzulegen: {len(todo)}")

        deadline = (timezone.localdate() + timedelta(days=opts["activity_days"])).isoformat()
        if dry:
            for r in todo[:10]:
                self.stdout.write(f"  [dry-run] Aktivität für {r.name} ({r.email})")
            if len(todo) > 10:
                self.stdout.write(f"  … und {len(todo) - 10} weitere")
            return

        created = 0
        for r in todo:
            vals = {
                "activity_type_id": EMAIL_ACTIVITY_TYPE_ID,
                "res_model_id": CRM_LEAD_MODEL_ID,
                "res_id": r.odoo_lead_id,
                "user_id": c.uid,
                "date_deadline": deadline,
                "summary": f"Erstkontakt-E-Mail an {r.name}",
                "note": f"Neugründung {r.town}. E-Mail: {r.email}. "
                        f"Personalisiert anschreiben (keine generische Massenmail).",
            }
            c._execute("mail.activity", "create", vals)
            created += 1
        self.stdout.write(self.style.SUCCESS(f"  → {created} E-Mail-Aktivitäten angelegt "
                                             f"(fällig {deadline})."))
