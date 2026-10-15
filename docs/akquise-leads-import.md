# Datalization-Akquise-Leads – Import der Kleinbetrieb-Liste

Importiert kuratierte regionale Kleinbetrieb-Leads aus einer Excel-Liste
(Blatt **„Leads"**) in eine eigene Admin-Liste. Gehört zum **Datalization**-Strom.

## Quelldatei

Excel (`.xlsx`) mit dem Blatt „Leads" und den Spalten: Nr, Firma, Segment, Ort,
Adresse, Telefon, Prio, Grösse, Mitarbeitende (Schätzung), Quelle Grösse,
Ansatz (Gesprächseinstieg), Status, Kontaktiert am, Nächster Schritt, Notizen.

Die **Prio**-Spalte ist meist A/B/C, kann aber auch **„Monekey"** oder
**„Partner"** sein – danach richtet sich der Odoo-Tag beim Push.

## Import

```bash
python manage.py import_acquisition_leads "/pfad/Akquise_Zofingen_Kleinbetriebe.xlsx" --dry-run
python manage.py import_acquisition_leads "/pfad/Akquise_Zofingen_Kleinbetriebe.xlsx"
```

Dedupe/Update über Firma+Ort. Benötigt `openpyxl` (in requirements.txt).

## Im Admin & Odoo

Unter **Akquise-Leads (Datalization)**: filterbar nach Prio/Status/Ort/Segment.
Aktion **„Ausgewählte als Leads nach Odoo pushen"** legt crm.leads an:
- **Tag**: A/B/C → „Datalization", „Monekey" → „Monekey", „Partner" → „Partner".
- **Odoo-Priorität**: A → Sehr hoch, B → Hoch, C → Mittel.
- **Beschreibung**: Segment, Grösse, Mitarbeitende, Priorität, Gesprächseinstieg, Notizen.
