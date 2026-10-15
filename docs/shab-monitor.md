# SHAB-Monitor – neue Firmengründungen als Leads

Holt täglich neue Handelsregister-Eintragungen (Neugründungen) aus dem **SHAB /
Amtsblattportal**, filtert sie auf dein Einzugsgebiet, reichert wo möglich
Telefon/E-Mail/Website an und schickt dir einen **E-Mail-Digest**. Alle Treffer
landen zusätzlich im **Django-Admin** unter *Neue Firmen* (filter-/durchsuchbar,
Status pflegbar).

- Quelle: `https://amtsblattportal.ch/api/v1` (öffentlich, **kein Key nötig**)
- Rubrik HR, Unterrubrik **HR01** (Neueintragung)
- Kosten: **CHF 0** (öffentliche Daten, Versand über bestehende Mail-Konfig)

## Was kommt rein, was nicht

Aus dem Handelsregister: **Firmenname, Adresse, Sitz, Kanton, Rechtsform, UID,
Zweck, Datum, SHAB-Link**. **Telefon/E-Mail stehen NICHT im Handelsregister** –
sie werden, wenn verfügbar, über die **search.ch**-Telefonbuch-API angereichert
(frische Firmen sind dort manchmal noch nicht gelistet → dann leer).
Firmen „in Liquidation" werden übersprungen.

## Einzugsgebiet anpassen

Die Orte stehen in `datalization_site/settings.py` → `SHAB_TOWNS` (kleingeschrieben,
wird gegen den Sitz-Ort gematcht). Enthält aktuell u. a. **alle 17 Gemeinden des
Bezirks Zofingen** plus die Regionen Aarau/Lenzburg, Baden, Oberaargau/Langenthal,
Sursee und Olten/Gäu. Kanton-Vorfilter: `SHAB_CANTONS` (AG, BE, LU, SO).

## Einrichtung (einmalig)

1. Migration ist bereits angelegt (`0012_newcompany`). Auf einer frischen DB:
   `python manage.py migrate`
2. **Telefon/E-Mail-Anreicherung aktivieren (optional, empfohlen):**
   Gratis-API-Key bei <https://tel.search.ch/api/> anfordern (1000 Abfragen/Monat),
   dann in die `.env`:
   ```
   SEARCH_CH_API_KEY=dein_key
   ```
3. Digest-Empfänger ist standardmässig `info@datalization.ch`
   (`SHAB_DIGEST_EMAIL` in der `.env` überschreibbar). Mailversand nutzt die
   bestehende Hostpoint-SMTP-Konfig (`HOSTPOINT_MAIL_PASSWORD` in der `.env`).

## Manuell ausführen

```bash
python manage.py fetch_new_companies --days 2          # normal (speichern + mailen)
python manage.py fetch_new_companies --days 7 --dry-run # nur testen, nichts speichern/mailen
python manage.py fetch_new_companies --days 2 --no-email # speichern, ohne Mail
```

Treffer danach im Admin unter **Neue Firmen** ansehen/pflegen.

## Täglich automatisch

Die Daten liegen in der **Datenbank** (für Admin + Dedupe) → der Job muss dort
laufen, wo die DB liegt.

### Jetzt (lokal, vor Go-live): macOS launchd
Lege `~/Library/LaunchAgents/ch.datalization.shab.plist` an:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>ch.datalization.shab</string>
  <key>ProgramArguments</key>
  <array><string>/Users/ticodanes/Projects/datalization/scripts/fetch_new_companies.sh</string></array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>/tmp/shab-monitor.log</string>
  <key>StandardErrorPath</key><string>/tmp/shab-monitor.err</string>
</dict></plist>
```
Aktivieren: `launchctl load ~/Library/LaunchAgents/ch.datalization.shab.plist`
(`--days 2` fängt einen verpassten Tag ab, falls der Mac mal aus war.)

### Später (Server/Produktion mit Postgres)
Entweder ein Cron auf dem Server (`scripts/fetch_new_companies.sh`) oder ein
GitHub-Actions-Workflow **mit** `DATABASE_URL` (Postgres) + `SEARCH_CH_API_KEY` +
`HOSTPOINT_MAIL_PASSWORD` als Secrets. Ohne persistente DB (nur SQLite in der
Action) funktionieren Admin-Liste und Dedupe nicht – dann würde der Digest täglich
alles erneut senden.

## Odoo CRM (optional) – Neugründungen als Leads pushen

Die Anbindung ist eingebaut (via XML-RPC, `crm.lead`). Aktivieren durch Setzen
aller vier Werte in der `.env`:

```
ODOO_URL=https://deinefirma.odoo.com
ODOO_DB=deinedb
ODOO_USERNAME=info@datalization.ch
ODOO_API_KEY=dein_api_key
# optional: ODOO_AUTOPUSH=0  → nicht automatisch pushen, nur via Admin-Aktion
```

Den **API-Key** erzeugst du in Odoo unter *Einstellungen → Benutzer →
(dein Benutzer) → Konto-Sicherheit → Neuer API-Key*. Der Benutzer braucht das
Recht, `crm.lead` anzulegen (CRM-App installiert). Tipp: Odoos **„One App Free"**
deckt CRM gratis ab.

**Verhalten:**
- Ist Odoo konfiguriert und `ODOO_AUTOPUSH` aktiv (Default), werden neue Treffer
  beim Lauf automatisch als Leads angelegt. Dedupe über `odoo_lead_id`.
- **Selektiv pushen:** im Admin unter *Neue Firmen* Einträge markieren →
  Aktion *„Ausgewählte als Leads nach Odoo pushen"*. Die Spalte *Odoo* zeigt,
  was schon gepusht ist.
- Push beim Abruf überspringen: `--no-odoo`.

Feld-Mapping: Firmenname → `partner_name`, Adresse → `street/zip/city/country_id`,
Telefon/E-Mail/Website → `phone/email_from/website`, Zweck + Rechtsform + UID +
Sitz + Datum + SHAB-Link → `description`, `type='lead'`.
