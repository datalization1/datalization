# SEO Go-Live-Checkliste (Website v2.0)

Diese Checkliste beschreibt, was passieren muss, damit die neue Website
(v2) von Google gefunden wird. **Vorher ist das bewusst nicht möglich** –
solange v2 auf `noindex` steht und nicht produktiv live ist, ranken auch
die SEO-Landingpages nicht. Das ist Absicht und kein Fehler.

## Voraussetzung

- [ ] **Odoo-Partner-Status vorhanden.** Erst dann darf v2 produktiv gehen
  (voraussichtlich Anfang November 2026). Bis dahin bleibt alles auf
  `noindex`.

---

## 1. Technische Freigabe (im Code)

- [ ] **`noindex` entfernen.** In `web/templates/v2/base_v2.html` (Zeile ~15)
  steht fix `<meta name="robots" content="noindex">`. Diese Zeile entfernen
  bzw. nur noch für echte Nicht-Index-Seiten (Danke-/Admin-Seiten) setzen.
  Danach pro Seite im Quelltext prüfen, dass kein `noindex` mehr ausgeliefert
  wird.

- [ ] **Sites-Domain korrigieren.** `SITE_ID = 1`
  (`datalization_site/settings.py`). Im Django-Admin unter *Sites* die Domain
  von `example.com` auf `datalization.ch` ändern. Davon hängen die absoluten
  URLs in der `sitemap.xml` ab – sonst zeigt die Sitemap auf `example.com`.

- [ ] **v2-Seiten in die Sitemap aufnehmen.** `web/sitemaps.py` listet aktuell
  nur die v1-Seiten (`web:home`, `web:about`, …) und die Case Studies. Beim
  Go-Live die v2-URLs ergänzen (bzw. auf v2 umstellen, falls v2 die alte Seite
  ersetzt): Startseite, Odoo + Unterseiten, Data & Analytics, Digitalisierung,
  Monekey, Über, Kontakt sowie die SEO-Seiten (`geschaeftssoftware-kmu`,
  `odoo-fuer-treuhaender`, `odoo-partner-olten`, `odoo-partner-zofingen`).
  Die Booking-/Submit- und Rechtstexte müssen **nicht** rein.

- [ ] **Entscheid: ersetzt v2 die alte Seite an der Wurzel (`/de/`) oder bleibt
  sie unter `/de/v2/`?** Fürs Ranking ist die Wurzel klar besser. Wird v2
  befördert, braucht es zusätzlich 301-Redirects von den alten v1-URLs auf die
  neuen v2-URLs, damit keine Rankings verloren gehen.

- [ ] **`robots.txt` prüfen.** Liegt unter `datalization_site/urls.py`
  (`Allow: /`, Verweis auf `/sitemap.xml`). Nach Domain-Umstellung sollte der
  Sitemap-Link absolut auf `https://datalization.ch/sitemap.xml` zeigen.

- [ ] **`sitemap.xml` testet 200** und listet die erwarteten URLs mit der
  richtigen Domain. (Der frühere 500er in der `CaseSitemap` ist behoben.)

---

## 2. Google Search Console

- [ ] **Property anlegen** für `datalization.ch` (Domain-Property via
  DNS-TXT-Eintrag empfohlen, deckt alle Subdomains/Protokolle ab).

- [ ] **Sitemap einreichen:** `https://datalization.ch/sitemap.xml`.

- [ ] **Indexierung anstossen:** wichtigste Seiten (Start, Odoo, SEO-Seiten)
  per „URL-Prüfung → Indexierung beantragen" einreichen.

- [ ] **hreflang kontrollieren.** DE/EN und `x-default` sind in `base_v2.html`
  bereits gesetzt – nach Go-Live in der Search Console auf Fehler prüfen.

---

## 3. Lokale Sichtbarkeit (Google Business Profile)

Für „Odoo Partner Zofingen/Olten" ist das lokale Profil oft wichtiger als die
Website selbst.

- [ ] **Google-Unternehmensprofil** für Datalization anlegen/beanspruchen
  (Adresse Bärengasse 3, 4800 Zofingen).
- [ ] Kategorie (z. B. „Softwareunternehmen" / „Unternehmensberatung"),
  Einzugsgebiet (Zofingen, Olten, Aarau, Langenthal, Sursee), Leistungen und
  Website-Link eintragen.
- [ ] Erste Bewertungen von zufriedenen Kund:innen einholen.

---

## 4. Nach dem Go-Live

- [ ] **In Search Console beobachten:** Indexierungsstatus, Suchanfragen,
  Klicks – gibt nach 1–2 Wochen erste Daten.
- [ ] **Interne Verlinkung prüfen:** Die SEO-Seiten sind aus dem Footer und
  kontextuell verlinkt – nach Bedarf aus passenden Textstellen zusätzlich
  verlinken.
- [ ] **Inhalte pflegen:** Reale Referenzen/Case Studies ergänzen, sobald
  vorhanden – das stärkt sowohl Vertrauen als auch Ranking.
