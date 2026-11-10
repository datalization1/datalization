"""Legt in Odoo Aktivitäten 'Brief senden' auf den Brief-Kandidaten an
(Neugründungen OHNE E-Mail, mit vollständiger Adresse, als Chance in Odoo).

Workflow: Chance öffnen → Drucken → 'Erstkontakt-Brief' (siehe
odoo_letter_report) → ausdrucken, unterschreiben, Visitenkarte beilegen,
versenden → Aktivität auf 'Erledigt' setzen. So ist dokumentiert, wer bereits
einen Brief erhalten hat.

Idempotent: jede so bearbeitete Firma bekommt das Tag 'Brief-Kandidat'; schon
getaggte werden nicht erneut mit einer Aktivität versehen.

    python manage.py odoo_letter_activities --dry-run
    python manage.py odoo_letter_activities
"""
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone

from leadgen import odoo_crm
from leadgen.models import NewCompany

CRM_LEAD_MODEL_ID = 2655
CAND_TAG = "Brief-Kandidat"
BEZIRK_ZOFINGEN = [
    "Aarburg", "Bottenwil", "Brittnau", "Kirchleerau", "Kölliken", "Moosleerau",
    "Murgenthal", "Oftringen", "Reitnau", "Rothrist", "Safenwil", "Staffelbach",
    "Strengelbach", "Uerkheim", "Vordemwald", "Wiliberg", "Zofingen",
]
LEGAL_RANK = [("aktien", 3), ("gmbh", 2), ("kollektiv", 2)]


def _rank(r):
    """Priorität: Telefon (Nachfass) → AG/GmbH → Bezirk Zofingen → neuste."""
    lf = (r.legal_form or "").lower()
    legal = next((v for k, v in LEGAL_RANK if k in lf), 1)
    has_phone = 1 if (r.phone or "").strip() else 0
    bezirk = 1 if r.town in BEZIRK_ZOFINGEN else 0
    pub = r.publication_date.toordinal() if hasattr(r.publication_date, "toordinal") else 0
    return (has_phone, legal, bezirk, pub)


def _chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


class Command(BaseCommand):
    help = "Aktivitäten 'Brief senden' für Neugründungen ohne E-Mail (mit Adresse)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--activity-days", type=int, default=7)
        parser.add_argument("--limit", type=int, default=0,
                            help="Nur N Aktivitäten anlegen (0 = alle offenen).")

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()
        dry = opts["dry_run"]

        # Aktivitätstyp 'Brief' sicherstellen
        at = c._execute("mail.activity.type", "search", [["name", "=", "Brief"]], limit=1)
        act_type = at[0] if at else (None if dry else
                                     c._execute("mail.activity.type", "create", {"name": "Brief"}))

        cand = list(NewCompany.objects
                    .exclude(shab_id__startswith="zefix:")
                    .filter(Q(email="") | Q(email__isnull=True), odoo_lead_id__isnull=False)
                    .exclude(Q(street="") | Q(street__isnull=True))
                    .exclude(Q(zip_code="") | Q(zip_code__isnull=True))
                    .exclude(Q(town="") | Q(town__isnull=True)))
        self.stdout.write(f"Brief-Kandidaten (ohne E-Mail, mit Adresse): {len(cand)}")

        # schon bearbeitete (Tag 'Brief-Kandidat') überspringen
        cand_tag = c.tag_id(CAND_TAG)
        tagged = set()
        ids = [r.odoo_lead_id for r in cand]
        for chunk in _chunks(ids, 200):
            rows = c._execute("crm.lead", "search_read",
                              [["id", "in", chunk], ["tag_ids", "in", cand_tag]],
                              fields=["id"])
            tagged.update(x["id"] for x in rows)
        todo = sorted((r for r in cand if r.odoo_lead_id not in tagged),
                      key=_rank, reverse=True)
        if opts["limit"]:
            todo = todo[:opts["limit"]]
        self.stdout.write(f"  bereits bearbeitet: {len(tagged)}, neu anzulegen: {len(todo)}")

        if dry:
            for r in todo[:15]:
                self.stdout.write(f"  [dry-run] {r.name} ({r.town})")
            if len(todo) > 15:
                self.stdout.write(f"  … und {len(todo) - 15} weitere")
            return

        deadline = (timezone.localdate() + timedelta(days=opts["activity_days"])).isoformat()
        created = 0
        for r in todo:
            c._execute("mail.activity", "create", {
                "activity_type_id": act_type,
                "res_model_id": CRM_LEAD_MODEL_ID,
                "res_id": r.odoo_lead_id,
                "user_id": c.uid,
                "date_deadline": deadline,
                "summary": "Erstkontakt-Brief senden",
                "note": f"Neugründung {r.town}. Drucken via 'Erstkontakt-Brief', "
                        f"unterschreiben, Visitenkarte beilegen, versenden. "
                        f"Danach telefonisch nachfassen"
                        f"{' (' + r.phone + ')' if r.phone else ''}.",
            })
            c._execute("crm.lead", "write", [r.odoo_lead_id], {"tag_ids": [(4, cand_tag)]})
            created += 1
        self.stdout.write(self.style.SUCCESS(
            f"{created} Aktivitäten 'Brief senden' angelegt (fällig {deadline})."))
