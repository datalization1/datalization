# Monekey-Leads – Import der Immobilien-/Maklerliste

Importiert Immobilien-/Maklerfirmen aus der Maklerliste (immoscout + homegate)
als **Monekey-Leads** in eine eigene Admin-Liste. Getrennt vom SHAB-Monitor
(der Odoo/Digitalisierungs-Leads liefert).

## Besonderheit der Quelldatei

Die Datei (`.ods`, trotz `.csv`-Endung) mischt **zwei Layouts**:
- **immoscout**: 11 Spalten
- **homegate**: 12 Spalten (zusätzliche Kanton-Spalte verschiebt alles um 1)

Dieselbe Firma kommt oft **doppelt** vor – je einmal pro Marktplatz, aber mit
**identischer `id`**. Der Import erkennt das Layout automatisch (an der Link-
Domain), dedupliziert über die `id` und **führt die Datensätze zusammen**
(fehlende Felder aus der anderen Quelle ergänzt). Firmennamen-Quote-Artefakte
(`""x""`) werden bereinigt.

Ergebnis beim ersten Import: **7.725 Zeilen → 4.422 eindeutige Firmen**
(3.901 mit Website, 3.709 mit Telefon).

## Import ausführen

```bash
python manage.py import_broker_leads "/pfad/Maklerliste 2.csv" --dry-run   # testen
python manage.py import_broker_leads "/pfad/Maklerliste 2.csv"             # importieren
```

Re-Import ist idempotent (Dedupe/Update über `external_id`). Benötigt `odfpy`
für `.ods` (`pip install odfpy`, steht in requirements.txt). `.csv` geht ohne.

## Im Admin

Unter **Immobilienfirmen (Monekey)**: such-/filterbar (Ort, Status, Marktplatz),
Status pflegbar (neu/kontaktiert/kein Interesse/Kunde).

## Nach Odoo pushen (selektiv)

Einträge markieren → Aktion **„Ausgewählte als Leads nach Odoo pushen (Monekey)"**.
Die Leads bekommen in Odoo den **Tag „Monekey"** (zur Abgrenzung von
den SHAB-Leads) und `type=lead`. Dedupe über `odoo_lead_id`. Setzt die
Odoo-Konfiguration in der `.env` voraus (siehe `docs/shab-monitor.md`).
