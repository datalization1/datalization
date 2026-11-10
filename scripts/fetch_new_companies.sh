#!/usr/bin/env bash
# Wöchentlicher Akquise-Lauf (Mittwoch 06:00 via launchd).
# Die ganze Kette steckt jetzt im Management-Command `weekly_run`:
#   Pull → Anreicherung → Push → FC-Tag → Sync → Mail-Charge (max 10) →
#   Brief-Charge-PDF (max 10) → FC-Report (+Mail) → Digest.
# Knöpfe kommen aus der .env:
#   SHAB_DAYS (Pull-Fenster), SHAB_REENRICH_DAYS (Nach-Anreicherung),
#   FC_REPORT_EMAIL (Empfänger FC-Report), HOSTPOINT_MAIL_PASSWORD (Mailversand).
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source .venv/bin/activate

python manage.py weekly_run
