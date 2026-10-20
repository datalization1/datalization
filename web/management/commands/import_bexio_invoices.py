"""Importiert die 14 historischen Bexio-Kundenrechnungen nach Odoo Accounting.

Legt je Rechnung einen geposteten Kundenbeleg (account.move, out_invoice) mit
Original-Bexio-Nummer, Einnahmenkonto 3400 und steuerbefreiter Position an und
verbucht die Zahlung zum Eingangsdatum im PostFinance-Journal (→ Status 'Bezahlt').

Idempotent: bereits vorhandene Nummern werden übersprungen.

    python manage.py import_bexio_invoices --dry-run
    python manage.py import_bexio_invoices
"""
import time

from django.core.management.base import BaseCommand, CommandError

from web import odoo_crm

SALES_JOURNAL_ID = 1       # "Sales" (RE)
BANK_JOURNAL_ID = 6        # "PostFinance"
INCOME_ACCOUNT_ID = 115    # 3400 "Revenues from services"

# (Nr, Rechnungsdatum, partner_id, Beschreibung, Betrag CHF, Zahlungseingang)
INVOICES = [
    ("RE-00003", "2025-12-03", 43, "Applikation Stüürli – Meilenstein 1 (Projektstart)", 6000.00, "2025-12-10"),
    ("RE-00004", "2025-10-31", 44, "IT-Support / Betreuung IT-Infrastruktur (53 h)", 5300.00, "2025-10-31"),
    ("RE-00005", "2025-11-28", 44, "IT-Support November 2025 (57 h)", 5700.00, "2025-11-28"),
    ("RE-00006", "2025-10-31", 45, "Homepage roberts-lackwerk.ch + IT-Support", 1100.00, "2025-10-31"),
    ("RE-00007", "2025-11-26", 45, "Homepage + IT-Support", 1200.00, "2025-11-26"),
    ("RE-00009", "2025-12-30", 44, "IT-Support Dezember 2025 (43 h)", 4300.00, "2026-01-09"),
    ("RE-00010", "2026-01-27", 44, "IT-Support Januar 2026 (53 h)", 5300.00, "2026-02-02"),
    ("RE-00011", "2026-01-27", 43, "Applikation Stürli – Meilenstein 2 (Mobile & Admin Dev)", 9000.00, "2026-02-10"),
    ("RE-00012", "2026-03-23", 43, "Applikation Stürli – Meilenstein 3 (Test/Prod)", 15000.00, "2026-04-30"),
    ("RE-00013", "2026-07-24", 48, "Webseite + Admin-Bereich (MS1 + MS2)", 750.00, "2026-07-27"),
    ("RE-00014", "2026-07-24", 47, "Phase 1 – Intune/Entra/Security Setup (16.5 h)", 1650.00, "2026-07-27"),
    ("RE-00015", "2026-08-28", 48, "Webseite – MS3 Finale Lieferung/Rollout", 750.00, "2026-08-31"),
    ("RE-00016", "2026-08-28", 49, "Swiss21 Setup – 1. Rate (50 %)", 350.00, "2026-08-28"),
    ("RE-00017", "2026-10-07", 47, "Phase 2 – M365 Security (22.5 h)", 2250.00, "2026-10-08"),
]


class Command(BaseCommand):
    help = "Importiert die historischen Bexio-Kundenrechnungen nach Odoo (gepostet + bezahlt)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--no-payment", action="store_true",
                            help="Nur posten, keine Zahlung verbuchen.")
        parser.add_argument("--sleep", type=float, default=0.5)

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        def ex(model, method, *a, **kw):
            return c._execute(model, method, *a, **kw)

        created = skipped = paid = 0
        for num, inv_date, partner_id, desc, amount, pay_date in INVOICES:
            # Idempotenz: existiert die Nummer bereits?
            if ex("account.move", "search_count", [["name", "=", num]]):
                self.stdout.write(f"  = {num} existiert bereits – übersprungen")
                skipped += 1
                continue
            if opts["dry_run"]:
                self.stdout.write(f"  + würde anlegen: {num}  {inv_date}  "
                                  f"Partner {partner_id}  CHF {amount:,.2f}  bezahlt {pay_date}")
                created += 1
                continue

            vals = {
                "move_type": "out_invoice",
                "partner_id": partner_id,
                "invoice_date": inv_date,
                "date": inv_date,
                "journal_id": SALES_JOURNAL_ID,
                "name": num,                      # Original-Bexio-Nummer behalten
                "ref": f"Bexio {num}",
                "invoice_line_ids": [(0, 0, {
                    "name": desc,
                    "quantity": 1.0,
                    "price_unit": amount,
                    "account_id": INCOME_ACCOUNT_ID,
                    "tax_ids": [(6, 0, [])],      # steuerbefreit
                })],
            }
            move_id = ex("account.move", "create", vals)
            move_id = move_id[0] if isinstance(move_id, (list, tuple)) else move_id
            ex("account.move", "action_post", [move_id])
            created += 1
            self.stdout.write(f"  + {num}  gepostet (id={move_id})  CHF {amount:,.2f}")
            time.sleep(opts["sleep"])

            if opts["no_payment"]:
                continue
            # Zahlung verbuchen (Register-Payment-Wizard)
            ctx = {"active_model": "account.move", "active_ids": [move_id]}
            try:
                wiz_id = ex("account.payment.register", "create",
                            {"payment_date": pay_date, "journal_id": BANK_JOURNAL_ID},
                            context=ctx)
                wiz_id = wiz_id[0] if isinstance(wiz_id, (list, tuple)) else wiz_id
                ex("account.payment.register", "action_create_payments", [wiz_id], context=ctx)
                paid += 1
                self.stdout.write(f"      ↳ Zahlung {pay_date} verbucht")
            except Exception as e:
                self.stderr.write(f"      ! Zahlung {num} fehlgeschlagen: {str(e)[:120]}")
            time.sleep(opts["sleep"])

        verb = "würde anlegen" if opts["dry_run"] else "angelegt"
        self.stdout.write(self.style.SUCCESS(
            f"\nFertig: {verb} {created}, übersprungen {skipped}, Zahlungen verbucht {paid}"))
