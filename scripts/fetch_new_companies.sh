#!/usr/bin/env bash
# Wöchentlicher Akquise-Lauf (Mittwoch 06:00 via launchd).
# Läuft seit 19.11.2026 im --no-odoo-Modus (Odoo-Tarif auf Standard reduziert →
# External API gesperrt). Kette im Command `weekly_run`:
#   Pull → Anreicherung → Brief-Charge-PDF (lokal markiert) → FC-Report (+Mail)
#   → Digest. KEIN Odoo-Push/Tag/Sync mehr.
# Knöpfe aus der .env: SHAB_DAYS, SHAB_REENRICH_DAYS, FC_REPORT_EMAIL.
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source .venv/bin/activate

python manage.py weekly_run --no-odoo
