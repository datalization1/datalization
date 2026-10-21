#!/usr/bin/env bash
# Wöchentlicher Neugründungs-Lauf (Mittwoch), voll angereichert.
# 1) SHAB holen + Zefix (Status/Links) + Google Places (Telefon/Website)
# 2) Nach-Anreicherung: kürzlich gegründete Firmen mit Lücke erneut versuchen
#    (gehen oft erst Wochen nach Gründung online) – Telefon via Google, E-Mail
#    von der Website.
# 3) Neue Leads voll angereichert nach Odoo pushen (ohne gelöschte)
# 4) Nachgereichte Telefon/E-Mail/Website bereits gepushter Leads nach Odoo syncen
# Keys/Passwörter aus der .env.
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source .venv/bin/activate
DAYS="${SHAB_DAYS:-8}"
# Fenster für die Nach-Anreicherung: so lange eine Firma als „neu" nachverfolgt
# wird, wird ihre Lücke jede Woche erneut versucht (Default ~4 Monate).
REENRICH_DAYS="${SHAB_REENRICH_DAYS:-120}"

# 1) Neue Publikationen holen (inkl. Zefix + Google inline)
python manage.py fetch_new_companies --days "$DAYS" --no-odoo --no-email

# 2) Nach-Anreicherung bestehender Lücken (letzte REENRICH_DAYS Tage)
python manage.py enrich_google_places --active-only --days "$REENRICH_DAYS"
python manage.py scrape_newcompany_emails --active-only --days "$REENRICH_DAYS"

# 3) Neue Treffer als Leads nach Odoo (Bestand/zefix: wird ausgeschlossen)
python manage.py push_leads_odoo --model shab

# 4) Bezirk-Zofingen-Neugründungen zusätzlich für FC Oftringen taggen
python manage.py tag_fc_oftringen

# 5) Nachgereichte Kontaktdaten in bestehende Odoo-Leads schreiben
python manage.py sync_odoo_contacts --active-only --days "$REENRICH_DAYS"
