"""Legt in Odoo die gespeicherten Arbeits-Filter (Favoriten) für die Akquise-Teams
an – damit der Alltag über klare Ansichten läuft statt über tausende Leads.

Zwei Blöcke: 'Datalization – Neu-Akquise' (Neugründungen) und 'Regionale Akquise'
(Bestand Region: Anruf-Liste / Mail-Akquise / Nachfass / nach Ort gruppiert).
Alle Filter sind persönlich (Favoriten-Menü der Leads-Ansicht), idempotent
(über Namen gesucht/aktualisiert).

    python manage.py odoo_sales_views

Ströme/Tags: Datalization=2, Erstkontakt E-Mail=6, Brief versendet=7,
Brief-Kandidat=8, Region Zofingen=10. Teams: Datalization=1, Regionale Akquise=5.
Stage 'Neu'=1.
"""
from django.core.management.base import BaseCommand, CommandError

from leadgen import odoo_crm

LEADS_ACTION_ID = 249           # CRM → Leads (Listenansicht)
DATA_TEAM = 1
REGION_TEAM = 5                 # Regionale Akquise (Bestand Region)
STAGE_NEU = 1
TAG_DATALIZATION = 2
TAG_MAIL = 6                    # Erstkontakt E-Mail
TAG_BRIEF_SENT = 7             # Brief versendet
TAG_BRIEF_CAND = 8            # Brief-Kandidat

# (Name, Domain-String[, Context-String]) – Reihenfolge = Anzeige-Logik.
FILTERS = [
    # --- Datalization – Neu-Akquise (Neugründungen) ---
    ("🎯 Diese Woche dran",
     f"[['team_id','=',{DATA_TEAM}],['tag_ids','in',[{TAG_BRIEF_CAND},{TAG_MAIL}]],"
     f"['tag_ids','not in',{TAG_BRIEF_SENT}]]"),

    ("📬 Brief-Kandidaten",
     f"[['team_id','=',{DATA_TEAM}],['email_from','=',False],['street','!=',False],"
     f"['tag_ids','not in',{TAG_BRIEF_SENT}]]"),

    ("✉️ Mail-Kandidaten offen",
     f"[['team_id','=',{DATA_TEAM}],['email_from','!=',False],"
     f"['tag_ids','not in',{TAG_MAIL}],['stage_id','=',{STAGE_NEU}]]"),

    ("⏰ Nachfass fällig",
     f"[['team_id','=',{DATA_TEAM}],['activity_state','in',['today','overdue']]]"),

    ("🆕 Neu & unberührt",
     f"[['team_id','=',{DATA_TEAM}],['stage_id','=',{STAGE_NEU}],"
     f"['tag_ids','not in',[{TAG_MAIL},{TAG_BRIEF_CAND},{TAG_BRIEF_SENT}]],"
     f"['activity_ids','=',False]]"),

    # --- Regionale Akquise (Bestand Region) ---
    ("🌍 Region: Anruf-Liste",
     f"[['team_id','=',{REGION_TEAM}],['phone','!=',False],['stage_id','=',{STAGE_NEU}]]"),

    ("🌍 Region: Mail-Akquise",
     f"[['team_id','=',{REGION_TEAM}],['email_from','!=',False],['stage_id','=',{STAGE_NEU}]]"),

    ("🌍 Region: Nachfass fällig",
     f"[['team_id','=',{REGION_TEAM}],['activity_state','in',['today','overdue']]]"),

    ("🌍 Region: nach Ort",
     f"[['team_id','=',{REGION_TEAM}]]",
     "{'group_by': ['city']}"),
]


class Command(BaseCommand):
    help = "Legt die gespeicherten Arbeits-Filter für das Datalization-Team an."

    def handle(self, *args, **opts):
        if not odoo_crm.enabled():
            raise CommandError("Odoo nicht konfiguriert.")
        c = odoo_crm.OdooClient()

        for entry in FILTERS:
            name, domain = entry[0], entry[1]
            context = entry[2] if len(entry) > 2 else "{}"
            vals = {"name": name, "model_id": "crm.lead", "domain": domain,
                    "context": context,
                    "user_ids": [(6, 0, [c.uid])], "action_id": LEADS_ACTION_ID,
                    "is_default": False}
            existing = c._execute("ir.filters", "search",
                                  [["name", "=", name], ["model_id", "=", "crm.lead"]], limit=1)
            if existing:
                c._execute("ir.filters", "write", existing, vals)
                fid, verb = existing[0], "aktualisiert"
            else:
                fid, verb = c._execute("ir.filters", "create", vals), "angelegt"

            # Treffer zählen zur Kontrolle
            try:
                n = c._execute("crm.lead", "search_count", eval(domain))
                cnt = f"{n:>4} Treffer"
            except Exception as e:  # noqa: BLE001
                cnt = f"(Zählung fehlgeschlagen: {e})"
            self.stdout.write(self.style.SUCCESS(f"{name:26} {verb} (id {fid}) – {cnt}"))

        self.stdout.write("\nFertig. In CRM → Leads unter ★ Favoriten sichtbar.")
