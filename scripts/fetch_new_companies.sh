#!/usr/bin/env bash
# Täglicher SHAB-Neugründungs-Abruf. Von launchd/cron aufrufen.
# Keys/Passwörter kommen aus der .env (SEARCH_CH_API_KEY, HOSTPOINT_MAIL_PASSWORD).
set -euo pipefail
cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
source .venv/bin/activate
exec python manage.py fetch_new_companies --days "${SHAB_DAYS:-2}"
