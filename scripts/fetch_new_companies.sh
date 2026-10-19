#!/usr/bin/env bash
# Wöchentlicher Neugründungs-Lauf (Mittwoch), voll angereichert.
# 1) SHAB holen + Zefix (Status/Links) + Google Places (Telefon/Website)
# 2) E-Mail von Website scrapen (Impressum/Kontakt)
# 3) Voll angereichert als Leads nach Odoo pushen (ohne gelöschte)
# Keys/Passwörter aus der .env.
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source .venv/bin/activate
DAYS="${SHAB_DAYS:-8}"
python manage.py fetch_new_companies --days "$DAYS" --no-odoo --no-email
python manage.py scrape_newcompany_emails --active-only
python manage.py push_leads_odoo --model shab
