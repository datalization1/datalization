# Logo-Dateien für Dokumente

Für Offerten, Rechnungen, Briefe, Präsentationen und E-Mail-Signaturen.
Nicht für die Website — die nutzt das Inline-SVG in
`web/templates/partials/logo_mark.html`, das sich automatisch an Hell und
Dunkel anpasst.

## Schreibweise

- **Firmenname im Text:** Datalization (gross)
- **Im Logo-Schriftzug:** datalization (klein)

Das ist Absicht und muss nicht angeglichen werden: die Wortmarke ist ein
gestaltetes Zeichen, der Firmenname ist Text. So halten es viele Marken.
In Fliesstext, Impressum, Rechnungskopf und Vertrag also immer «Datalization».

## Die drei Aufbauten

| | Verhältnis | Standardmass | Wofür |
|---|---|---|---|
| **marke** | 1,03 : 1 | 18,6 × 18 mm | Wenn der Firmenname daneben ohnehin getippt steht — z. B. Rechnungskopf mit Adressblock. |
| **horizontal** | 3,89 : 1 | 46,7 × 12 mm | Der Allrounder. Briefkopf, E-Mail-Signatur, Folienfuss. |
| **vertikal** | 1,41 : 1 | 28,2 × 20 mm | Wenn wenig Breite da ist — Offerten-Deckblatt, Etikett, Social-Profilbild. |

## Alle Dateien

Jeder Aufbau liegt als SVG (Vektor, verlustfrei) und PNG (2000 px lange Seite) vor.

| Datei | Marke | Hintergrund | Einsatz |
|---|---|---|---|
| `datalization-marke.svg` / `.png` | schwarz | transparent | **Standard.** Auf weissem oder hellem Grund. |
| `datalization-marke-aufweiss.svg` / `.png` | schwarz | weiss | Wenn das Programm keine Transparenz kann, oder auf leicht farbigem Grund. |
| `datalization-marke-weiss.svg` / `.png` | weiss | transparent | Auf dunklen Flächen. |
| `datalization-horizontal.svg` / `.png` | schwarz | transparent | **Standard.** |
| `datalization-horizontal-aufweiss.svg` / `.png` | schwarz | weiss | |
| `datalization-horizontal-weiss.svg` / `.png` | weiss | transparent | |
| `datalization-vertikal.svg` / `.png` | schwarz | transparent | **Standard.** |
| `datalization-vertikal-aufweiss.svg` / `.png` | schwarz | weiss | |
| `datalization-vertikal-weiss.svg` / `.png` | weiss | transparent | |

Der Punkt ist in **allen** Varianten orange — auch in der weissen.

## Masse

Alle Dateien haben **12 % Freiraum rundum eingebaut**. Die angegebene Höhe ist
die Höhe der ganzen Datei; die Zeichnung darin ist entsprechend kleiner. So
entsteht der Abstand zum Seitenrand automatisch.

Die SVG-Dateien tragen das Standardmass bereits in sich — viele Programme
übernehmen es beim Einfügen.

**marke**

| Einsatz | Höhe | Breite |
|---|---|---|
| Rechnung / Offerte, Kopfbereich | 18 mm | 18,6 mm |
| Deckblatt | 24 mm | 24,7 mm |
| Folgeseiten, Fusszeile | 12 mm | 12,4 mm |
| Kleinstmass | 10 mm | 10,3 mm |

**horizontal**

| Einsatz | Höhe | Breite |
|---|---|---|
| Briefkopf, Rechnung | 12 mm | 46,7 mm |
| E-Mail-Signatur | 9 mm | 35 mm |
| Deckblatt, Folientitel | 16 mm | 62,2 mm |
| Kleinstmass — darunter wird der Schriftzug eng | 7 mm | 27,2 mm |

**vertikal**

| Einsatz | Höhe | Breite |
|---|---|---|
| Offerten-Deckblatt | 20 mm | 28,2 mm |
| Etikett, Profilbild | 30 mm | 42,3 mm |
| Kleinstmass | 14 mm | 19,7 mm |

In Pixeln, falls die Vorlage in px rechnet:

| mm | 96 dpi (Bildschirm) | 300 dpi (Druck) |
|---|---|---|
| 9 mm | 34 px | 106 px |
| 12 mm | 45 px | 142 px |
| 18 mm | 68 px | 213 px |
| 20 mm | 76 px | 236 px |
| 24 mm | 91 px | 283 px |

## Regeln

- **Nicht verzerren** — Seitenverhältnis immer beibehalten.
- **Der Punkt bleibt orange** (`#F48B2D`), auf jedem Untergrund.
- **Schriftzug nicht neu setzen.** Er ist in Pfade umgewandelt, damit er ohne
  installierte Schrift überall identisch aussieht. Wer ihn abtippt, bekommt eine
  andere Laufweite.
- **Keinen Rahmen und keinen Schatten** hinzufügen.
- Auf Fotos oder farbigen Flächen die Variante `-aufweiss` verwenden, nicht die
  transparente auf unruhigem Grund.

## Farben

| | Hex | RGB | CMYK (Richtwert) |
|---|---|---|---|
| Marke schwarz | `#101010` | 16 / 16 / 16 | 0 / 0 / 0 / 95 |
| Punkt orange | `#F48B2D` | 244 / 139 / 45 | 0 / 52 / 88 / 0 |
| Marke weiss | `#FFFFFF` | 255 / 255 / 255 | 0 / 0 / 0 / 0 |

## Herkunft des Schriftzugs

Inter SemiBold, Laufweite 0,14 em — dieselbe Schrift und Laufweite wie auf der
Website. Inter steht unter der SIL Open Font License, das Umwandeln in Pfade und
die Verwendung im Logo sind damit zulässig.
