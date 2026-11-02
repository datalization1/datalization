#!/bin/bash
# Setzt eine HTML-Signatur direkt in die Apple-Mail-Signaturdatei ein.
#
#   ./signatur_einsetzen.sh PLATZHALTER_TIHOMIR tihomir.html
#   ./signatur_einsetzen.sh PLATZHALTER_INFO    info.html
#
# Ablauf:
#   1. Sucht die .mailsignature-Datei, die den Platzhalter-Text enthaelt.
#   2. Legt eine Sicherung (.bak) an.
#   3. Behaelt die Kopfzeilen (Content-Type etc.), ersetzt nur den HTML-Inhalt.
#   4. Sperrt die Datei (chflags uschg), damit Mail sie nicht mehr umbaut.
#
# Voraussetzung: Mail wurde mit Cmd+Q beendet und Terminal hat
# Festplattenvollzugriff (Systemeinstellungen -> Datenschutz & Sicherheit).

set -euo pipefail

PLATZHALTER="${1:-}"
HTML_DATEI="${2:-}"

if [[ -z "$PLATZHALTER" || -z "$HTML_DATEI" ]]; then
  echo "Aufruf: $0 PLATZHALTER signatur.html" >&2
  exit 1
fi

if [[ ! -f "$HTML_DATEI" ]]; then
  echo "Fehler: HTML-Datei '$HTML_DATEI' nicht gefunden." >&2
  exit 1
fi

# Signaturen-Ordner finden (Mail-Version variiert: V10, V9, ...).
SIG_DIR=""
for d in "$HOME/Library/Mail"/V*/MailData/Signatures; do
  [[ -d "$d" ]] && SIG_DIR="$d"
done

if [[ -z "$SIG_DIR" ]]; then
  echo "Fehler: Kein Mail-Signaturen-Ordner gefunden." >&2
  echo "Haben Sie in Mail eine Signatur mit dem Text '$PLATZHALTER' angelegt?" >&2
  exit 1
fi

# Die .mailsignature-Datei finden, die den Platzhalter enthaelt.
ZIEL=""
while IFS= read -r -d '' f; do
  if grep -qF "$PLATZHALTER" "$f"; then
    ZIEL="$f"
    break
  fi
done < <(find "$SIG_DIR" -name '*.mailsignature' -print0)

if [[ -z "$ZIEL" ]]; then
  echo "Fehler: Keine Signatur mit dem Text '$PLATZHALTER' gefunden." >&2
  echo "In Mail eine neue Signatur anlegen, die nur '$PLATZHALTER' enthaelt," >&2
  echo "Mail mit Cmd+Q beenden und das Script erneut ausfuehren." >&2
  exit 1
fi

echo "Gefunden: $ZIEL"

# Entsperren (falls schon frueher gesperrt), Sicherung anlegen.
chflags nouchg "$ZIEL" 2>/dev/null || true
cp -p "$ZIEL" "$ZIEL.bak"
echo "Sicherung: $ZIEL.bak"

# Kopfzeilen behalten (alles bis zur ersten Leerzeile), Inhalt ersetzen.
TMP="$(mktemp)"
awk 'BEGIN{h=1} h==1{print} /^$/{h=0}' "$ZIEL" > "$TMP"
cat "$HTML_DATEI" >> "$TMP"
mv "$TMP" "$ZIEL"

# Sperren, damit Mail die Datei nicht mehr veraendert.
chflags uschg "$ZIEL"
echo "Eingesetzt und gesperrt."
echo "Mail starten und unter 'Signatur auswaehlen' die neue Signatur waehlen."
