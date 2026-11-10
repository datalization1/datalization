"""Wöchentliche Akquise-Maschine – EIN Lauf erledigt die ganze Kette.

Gedacht für den Mittwoch-Cron (ersetzt die Schrittliste in
scripts/fetch_new_companies.sh). Orchestriert bestehende Commands und deckelt
die Chargen auf die Nachfass-Kapazität.

Ablauf:
  1) SHAB-Pull (inkrementell) + Zefix/Google inline
  2) Nach-Anreicherung bestehender Lücken (Telefon/E-Mail)
  3) Neue Treffer als Leads nach Odoo (Bestand/zefix: ausgeschlossen)
  4) Bezirk-Zofingen-Neugründungen für FC Oftringen taggen
  5) Nachgereichte Kontaktdaten in bestehende Leads syncen
  6) Leads→Chancen + E-Mail-Aktivitäten, gedeckelt auf --mail-limit (nur vorbereiten)
  7) Brief-Charge: PDF für --brief-limit Firmen OHNE E-Mail (taggt + Nachfass-Aktivität)
  8) FC-Oftringen-Report erzeugen und (wenn konfiguriert) an den Verein mailen
  9) Digest an dich: was raus ging, was nachzufassen ist

    python manage.py weekly_run --dry-run    # zeigt nur den Plan, ändert nichts
    python manage.py weekly_run              # scharfer Lauf

Knöpfe (auch via Env): --days (SHAB_DAYS=8), --reenrich-days (SHAB_REENRICH_DAYS=120),
--mail-limit (10), --brief-limit (10), --fc-email (FC_REPORT_EMAIL),
--digest-email (default info@datalization.ch).
"""
import os
import traceback
from datetime import date

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from leadgen import odoo_crm
from leadgen.management.commands.odoo_mail_identity import SIGNATURE_HTML

DEFAULT_DIGEST = "info@datalization.ch"

# Gespeicherte Arbeits-Filter (siehe odoo_sales_views) für die Digest-Zahlen.
DATA_TEAM = 1
SNAPSHOT = {
    "📬 Brief-Kandidaten offen": [["team_id", "=", DATA_TEAM], ["email_from", "=", False],
                                  ["street", "!=", False], ["tag_ids", "not in", 7]],
    "✉️ Mail-Kandidaten offen": [["team_id", "=", DATA_TEAM], ["email_from", "!=", False],
                                 ["tag_ids", "not in", 6], ["stage_id", "=", 1]],
    "⏰ Nachfass fällig": [["team_id", "=", DATA_TEAM],
                          ["activity_state", "in", ["today", "overdue"]]],
    "🆕 Neu & unberührt": [["team_id", "=", DATA_TEAM], ["stage_id", "=", 1],
                          ["tag_ids", "not in", [6, 8, 7]], ["activity_ids", "=", False]],
}


class Command(BaseCommand):
    help = "Wöchentliche Akquise-Maschine (Pull → Chargen → FC-Report → Digest)."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true",
                            help="Nur den Plan zeigen, nichts ausführen/ändern.")
        parser.add_argument("--days", type=int,
                            default=int(os.getenv("SHAB_DAYS", "8")))
        parser.add_argument("--reenrich-days", type=int,
                            default=int(os.getenv("SHAB_REENRICH_DAYS", "120")))
        parser.add_argument("--mail-limit", type=int, default=10)
        parser.add_argument("--brief-limit", type=int, default=10)
        parser.add_argument("--fc-days", type=int, default=7,
                            help="Zeitfenster des FC-Reports in Tagen (Default 7 = Wochen-Delta).")
        parser.add_argument("--fc-email", default=os.getenv("FC_REPORT_EMAIL", ""))
        parser.add_argument("--digest-email", default=DEFAULT_DIGEST)
        parser.add_argument("--no-fc-mail", action="store_true")
        parser.add_argument("--no-digest", action="store_true")
        parser.add_argument("--skip-fetch", action="store_true",
                            help="Pull/Anreicherung überspringen (nur Chargen/Report).")
        parser.add_argument("--no-backup", action="store_true",
                            help="Kein DB-Backup zu Beginn des Laufs.")
        parser.add_argument("--backup-keep", type=int, default=8,
                            help="Anzahl behaltener Wochen-Backups pro Ziel (Default 8).")

    # ---------------------------------------------------------------- helpers
    def _step(self, n, label):
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n[{n}] {label}"))

    def _call(self, dry, cmd, *args, **kw):
        """Sub-Command ausführen (oder im Dry-Run nur anzeigen)."""
        shown = " ".join([cmd, *args] + [f"--{k.replace('_', '-')} {v}"
                                         for k, v in kw.items()])
        if dry:
            self.stdout.write(f"    [dry-run] manage.py {shown}")
            return
        self.stdout.write(f"    → manage.py {shown}")
        call_command(cmd, *args, **kw, stdout=self.stdout)

    def _reports_dir(self):
        d = os.path.join(settings.BASE_DIR, "reports")
        os.makedirs(d, exist_ok=True)
        return d

    def _backup_db(self, dry, today, keep):
        """Konsistente SQLite-Sicherung (lokal + Google Drive), mit Rotation.

        Nutzt die sqlite3-Backup-API statt cp → sauberer Snapshot auch bei
        offener DB. Zielordner: backups/ (lokal) und – wenn vorhanden – ein
        Cloud-Ordner (DB_BACKUP_CLOUD_DIR, Default Google Drive).
        """
        import glob
        import sqlite3

        src = settings.DATABASES["default"]["NAME"]
        if not os.path.exists(src):
            self.stdout.write(self.style.WARNING(f"    DB nicht gefunden ({src}) – kein Backup."))
            return
        fname = f"db_{today.isoformat()}.sqlite3"

        # Cloud-Ziel = OneDrive (per Glob gefunden → robust gegen Umlaut/Varianten).
        # DB_BACKUP_CLOUD_DIR überschreibt. Google Drive bewusst NICHT (Streaming-
        # Mount verschwindet zeitweise ganz, untauglich für einen 06:00-Cron).
        cloud = os.environ.get("DB_BACKUP_CLOUD_DIR")
        if not cloud:
            od = sorted(glob.glob(os.path.expanduser("~/Library/CloudStorage/OneDrive*")))
            cloud = os.path.join(od[0], "Datalization-Backups") if od else ""
        # Cloud nur nutzen, wenn der übergeordnete Sync-Ordner GERADE existiert
        # (sonst – z. B. Mount nicht bereit – nur lokal sichern, kein Fehler).
        targets = [os.path.join(settings.BASE_DIR, "backups")]
        if cloud and os.path.isdir(os.path.dirname(cloud.rstrip("/"))):
            targets.append(cloud)

        if dry:
            self.stdout.write(f"    [dry-run] DB-Backup → {', '.join(targets)} (behalte {keep})")
            return

        for d in targets:
            try:
                os.makedirs(d, exist_ok=True)
                dst = os.path.join(d, fname)
                with sqlite3.connect(src) as s, sqlite3.connect(dst) as bak:
                    s.backup(bak)                       # konsistenter Snapshot
                # Rotation: nur die letzten `keep` behalten
                old = sorted(glob.glob(os.path.join(d, "db_*.sqlite3")))[:-keep]
                for f in old:
                    os.remove(f)
                is_local = os.path.abspath(d) == os.path.abspath(
                    os.path.join(settings.BASE_DIR, "backups"))
                where = "lokal" if is_local else ("OneDrive" if "OneDrive" in d else "Cloud")
                size = os.path.getsize(dst) / 1_000_000
                self.stdout.write(self.style.SUCCESS(
                    f"    ✓ {where}: {fname} ({size:.1f} MB), {keep} Kopien behalten."))
            except Exception as e:  # noqa: BLE001
                self.stdout.write(self.style.ERROR(f"    Backup nach {d} fehlgeschlagen: {e}"))

    def _snapshot(self):
        """Aktuelle Zahlen der Arbeits-Filter (für den Digest)."""
        if not odoo_crm.enabled():
            return {}
        c = odoo_crm.OdooClient()
        return {name: c._execute("crm.lead", "search_count", dom)
                for name, dom in SNAPSHOT.items()}

    # ------------------------------------------------------------------- main
    def handle(self, *args, **o):
        dry = o["dry_run"]
        today = timezone.localdate()
        rd = o["reenrich_days"]
        self.stdout.write(self.style.SUCCESS(
            f"=== Wochenlauf {today.isoformat()} "
            f"{'(DRY-RUN)' if dry else ''} ==="))
        self.stdout.write(f"Pull {o['days']} Tage · Nach-Anreicherung {rd} Tage · "
                          f"Mail-Charge {o['mail_limit']} · Brief-Charge {o['brief_limit']}")

        if not o["no_backup"]:
            self._step(0, "DB-Backup (lokal + OneDrive)")
            self._backup_db(dry, today, o["backup_keep"])

        if not o["skip_fetch"]:
            self._step(1, "SHAB-Pull + Zefix/Google")
            self._call(dry, "fetch_new_companies", "--no-odoo", "--no-email",
                       days=o["days"])
            self._step(2, "Nach-Anreicherung bestehender Lücken")
            self._call(dry, "enrich_google_places", "--active-only", days=rd)
            self._call(dry, "scrape_newcompany_emails", "--active-only", days=rd)
            self._step(3, "Neue Treffer → Odoo-Leads")
            self._call(dry, "push_leads_odoo", model="shab")
            self._step(4, "FC-Oftringen-Tag (Bezirk Zofingen)")
            self._call(dry, "tag_fc_oftringen")
            self._step(5, "Nachgereichte Kontaktdaten syncen")
            self._call(dry, "sync_odoo_contacts", "--active-only", days=rd)
        else:
            self.stdout.write("  (Pull/Anreicherung übersprungen – --skip-fetch)")

        if o["mail_limit"] > 0:
            self._step(6, f"Leads→Chancen + E-Mail-Charge (max {o['mail_limit']})")
            self._call(dry, "odoo_opportunities", limit=o["mail_limit"])
        else:
            self._step(6, "E-Mail-Charge übersprungen (--mail-limit ≤ 0)")

        brief_out = os.path.join(self._reports_dir(),
                                 f"Neugruender-Briefe_{today.isoformat()}.html")
        if o["brief_limit"] > 0:
            self._step(7, f"Brief-Charge PDF (max {o['brief_limit']})")
            self._call(dry, "generate_letters", limit=o["brief_limit"], out=brief_out)
        else:
            self._step(7, "Brief-Charge übersprungen (--brief-limit ≤ 0)")
            brief_out = "(keine Brief-Charge)"

        self._step(8, "FC-Oftringen-Report erzeugen + mailen")
        self._fc_report(dry, today, o)

        self._step(9, "Digest an dich")
        self._digest(dry, today, o, brief_out)

        self.stdout.write(self.style.SUCCESS(f"\n=== Wochenlauf fertig ({today}) ==="))

    # ------------------------------------------------------------- FC report
    def _fc_report(self, dry, today, o):
        out = os.path.join(self._reports_dir(),
                           f"FC-Oftringen_Neugruendungen_{today.isoformat()}.xlsx")
        self._call(dry, "export_newcompanies", "--bezirk-zofingen", "--active-only",
                   "--new-only", out=out, days=o["fc_days"])
        if dry:
            self.stdout.write(f"    [dry-run] Report-Mail an {o['fc_email'] or '(keine FC-Adresse)'}")
            return
        if o["no_fc_mail"] or not o["fc_email"]:
            self.stdout.write(self.style.WARNING(
                f"    Report erzeugt ({out}), aber NICHT gemailt "
                f"({'--no-fc-mail' if o['no_fc_mail'] else 'keine FC_REPORT_EMAIL/--fc-email'})."))
            return
        try:
            kw = today.isocalendar().week
            intro = ("im Anhang die diese Woche neu gegründeten Firmen im Bezirk "
                     "Zofingen – mögliche Sponsoren für den FC Oftringen.")
            text_body = (f"Hoi Marco\n\n{intro}\n\nFreundliche Grüsse\n\n"
                         "Tihomir Danesic\n\n"
                         "Datalization\n"
                         "076 563 06 08 · www.datalization.ch\n"
                         "Bärengasse 3, 4800 Zofingen\nEinfache Lösungen schaffen")
            html_body = (
                "<div style=\"font-family:Arial,Helvetica,sans-serif;font-size:14px;"
                "line-height:1.6;color:#1a1a1a;\">"
                f"<p>Hoi Marco</p><p>{intro}</p>"
                "<p style=\"margin-bottom:2px;\">Freundliche Grüsse</p>"
                "<p style=\"margin-top:0;\">Tihomir Danesic</p></div>"
                + SIGNATURE_HTML)
            msg = EmailMultiAlternatives(
                subject=f"Neugründungen Bezirk Zofingen – KW {kw}",
                body=text_body, to=[o["fc_email"]], reply_to=[DEFAULT_DIGEST])
            msg.attach_alternative(html_body, "text/html")
            if os.path.exists(out):
                msg.attach_file(out)
            msg.send(fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f"    Report an {o['fc_email']} gemailt."))
        except Exception as e:  # noqa: BLE001
            self.stdout.write(self.style.ERROR(
                f"    FC-Mail fehlgeschlagen: {e}. Report liegt unter {out}."))

    # ---------------------------------------------------------------- digest
    def _digest(self, dry, today, o, brief_out):
        snap = {} if dry else self._snapshot()
        lines = [f"Wochenlauf {today.isoformat()} abgeschlossen.", ""]
        if snap:
            lines.append("Stand Datalization-Pipeline:")
            lines += [f"  {name}: {n}" for name, n in snap.items()]
            lines.append("")
        lines += [
            f"Brief-Charge erzeugt: {brief_out}",
            "→ Öffnen, drucken, unterschreiben, Visitenkarte beilegen, versenden.",
            "→ Danach in Odoo Filter '📬 Brief-Kandidaten' die Charge als 'Brief versendet' markieren.",
            "",
            "Deine Tagesliste: Odoo → Aktivitäten (Filter '⏰ Nachfass fällig').",
        ]
        body = "\n".join(lines)
        if dry:
            self.stdout.write("    [dry-run] Digest-Mail an "
                              f"{o['digest_email']}:\n" + body)
            return
        if o["no_digest"]:
            self.stdout.write("    Digest übersprungen (--no-digest). Zusammenfassung:\n" + body)
            return
        try:
            EmailMessage(subject=f"Akquise-Wochenlauf {today.isoformat()}",
                         body=body, to=[o["digest_email"]]).send(fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f"    Digest an {o['digest_email']} gemailt."))
        except Exception as e:  # noqa: BLE001
            self.stdout.write(self.style.ERROR(
                f"    Digest-Mail fehlgeschlagen: {e}. Zusammenfassung:\n" + body))
