"""Neue Firmengründungen aus dem SHAB holen, speichern und als Digest mailen.

Quelle: Amtsblattportal / SHAB REST-API (öffentlich, kein Key nötig)
  https://amtsblattportal.ch/api/v1/publications
Rubrik HR / Unterrubrik HR01 = Handelsregister-Neueintragung.

Ablauf:
  1. Neueintragungen der letzten N Tage für die Ziel-Kantone abrufen.
  2. Nach Sitz-Ort auf das Einzugsgebiet filtern (settings.SHAB_TOWNS).
  3. Über search.ch optional Telefon/E-Mail/Website anreichern.
  4. Neue Treffer in der DB speichern (Dedupe über shab_id).
  5. Täglichen E-Mail-Digest an settings.SHAB_DIGEST_EMAIL senden.

Beispiel:
  python manage.py fetch_new_companies --days 2
  python manage.py fetch_new_companies --days 7 --dry-run
"""
import re
import xml.etree.ElementTree as ET
from datetime import timedelta

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.html import escape

from web import odoo_crm, zefix
from web.models import NewCompany

LIST_URL = "https://amtsblattportal.ch/api/v1/publications/xml"
SEARCH_CH_URL = "https://search.ch/tel/api/"
HEADERS = {"User-Agent": "Datalization-SHAB-Monitor/1.0 (info@datalization.ch)"}
DETAIL_URL = "https://www.shab.ch/#!/search/publications/detail/{id}"

LEGAL_FORMS = {
    "0101": "Einzelunternehmen",
    "0103": "Kollektivgesellschaft",
    "0104": "Kommanditgesellschaft",
    "0105": "Kommanditaktiengesellschaft",
    "0106": "Aktiengesellschaft",
    "0107": "GmbH",
    "0108": "Genossenschaft",
    "0109": "Verein",
    "0110": "Stiftung",
    "0111": "Zweigniederlassung (ausländisch)",
    "0112": "Zweigniederlassung (schweizerisch)",
}


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _find(elem, name):
    if elem is None:
        return None
    for e in elem.iter():
        if _local(e.tag) == name:
            return e
    return None


def _text(elem, name):
    e = _find(elem, name)
    return (e.text or "").strip() if e is not None and e.text else ""


class Command(BaseCommand):
    help = "Neue Firmengründungen (SHAB HR01) holen, speichern und als Digest mailen."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=2,
                            help="Wie viele Tage zurück (Publikationsdatum). Default 2.")
        parser.add_argument("--dry-run", action="store_true",
                            help="Nichts speichern/mailen, nur anzeigen.")
        parser.add_argument("--no-email", action="store_true",
                            help="Speichern, aber keinen Digest senden.")
        parser.add_argument("--limit", type=int, default=0,
                            help="Max. Anzahl geprüfter Publikationen (0 = alle).")
        parser.add_argument("--no-odoo", action="store_true",
                            help="Nicht nach Odoo CRM pushen (auch wenn konfiguriert).")
        parser.add_argument("--towns", default="",
                            help="Komma-Liste von Orten (überschreibt SHAB_TOWNS für diesen Lauf).")
        parser.add_argument("--cantons", default="",
                            help="Komma-Liste von Kantonen (überschreibt SHAB_CANTONS).")

    def handle(self, *args, **opts):
        days = opts["days"]
        dry = opts["dry_run"]
        no_email = opts["no_email"]
        limit = opts["limit"]
        date_from = (timezone.localdate() - timedelta(days=days)).isoformat()

        if opts["towns"]:
            towns = {t.strip().lower() for t in opts["towns"].split(",") if t.strip()}
        else:
            towns = {t.lower() for t in getattr(settings, "SHAB_TOWNS", set())}
        if opts["cantons"]:
            cantons = [c.strip().upper() for c in opts["cantons"].split(",") if c.strip()]
        else:
            cantons = getattr(settings, "SHAB_CANTONS", ["AG"])

        push_odoo = (not opts["no_odoo"] and not dry
                     and getattr(settings, "ODOO_AUTOPUSH", False) and odoo_crm.enabled())
        self._odoo = None

        self.stdout.write(f"SHAB-Abruf: Kantone {','.join(cantons)}, ab {date_from}, "
                          f"{len(towns)} Zielorte")

        refs = []
        for canton in cantons:
            refs.extend(self._list_refs(canton, date_from))
        # dedupe refs
        seen = set()
        refs = [r for r in refs if not (r[0] in seen or seen.add(r[0]))]
        self.stdout.write(f"{len(refs)} Neueintragungen im Zeitraum (alle Zielkantone)")

        checked = 0
        added = []
        for shab_id, ref in refs:
            if limit and checked >= limit:
                break
            checked += 1
            if NewCompany.objects.filter(shab_id=shab_id).exists():
                continue
            data = self._fetch_parse(shab_id, ref)
            if not data:
                continue
            place = (data["town"] or data["seat"]).lower()
            if towns and place not in towns:
                continue
            # Firmen in Liquidation sind keine Leads – überspringen.
            if re.search(r"in liquidation|in liq\.", data["name"], re.I):
                continue
            self._enrich(data)
            self._enrich_zefix(data)
            if not dry:
                obj = NewCompany.objects.create(**data)
                if push_odoo:
                    try:
                        if self._odoo is None:
                            self._odoo = odoo_crm.OdooClient()
                        odoo_crm.push_company(obj, client=self._odoo)
                    except Exception as e:
                        self.stderr.write(f"  ~ Odoo-Push {obj.name}: {e}")
            added.append(data)
            self.stdout.write(self.style.SUCCESS(
                f"  + {data['name']} – {data['zip_code']} {data['town']} "
                f"({data['legal_form']})"
                + (f" ☎ {data['phone']}" if data['phone'] else "")))

        self.stdout.write(f"Geprüft: {checked}, neu im Einzugsgebiet: {len(added)}"
                          + (", nach Odoo gepusht" if push_odoo else ""))

        if added and not dry and not no_email:
            self._send_digest(added)
            self.stdout.write(self.style.SUCCESS(
                f"Digest an {settings.SHAB_DIGEST_EMAIL} gesendet."))
        elif dry:
            self.stdout.write(self.style.WARNING("DRY-RUN: nichts gespeichert/gesendet."))

    # ---- SHAB -------------------------------------------------------------
    def _list_refs(self, canton, date_from):
        """Liste der Publikations-Refs (id, ref) eines Kantons ab date_from."""
        out = []
        page = 0
        while True:
            params = {
                "publicationStates": "PUBLISHED",
                "rubrics": "HR",
                "subRubrics": "HR01",
                "cantons": canton,
                "pageRequest.size": 100,
                "pageRequest.page": page,
                "pageRequest.sortOrders[0].name": "publicationDate",
                "pageRequest.sortOrders[0].direction": "DESC",
            }
            try:
                r = requests.get(LIST_URL, params=params, headers=HEADERS, timeout=30)
                r.raise_for_status()
                root = ET.fromstring(r.content)
            except Exception as e:
                self.stderr.write(f"  ! Liste {canton} Seite {page}: {e}")
                break
            pubs = [p for p in root.iter() if _local(p.tag) == "publication"]
            if not pubs:
                break
            stop = False
            for p in pubs:
                ref = p.get("ref") or ""
                m = re.search(r"/publications/([a-f0-9-]+)/xml", ref)
                if not m:
                    continue
                pubdate = _text(p, "publicationDate")
                if pubdate and pubdate < date_from:
                    stop = True
                    continue
                out.append((m.group(1), ref))
            if stop or len(pubs) < 100:
                break
            page += 1
        return out

    def _fetch_parse(self, shab_id, ref):
        try:
            r = requests.get(ref, headers=HEADERS, timeout=30)
            r.raise_for_status()
            root = ET.fromstring(r.content)
        except Exception as e:
            self.stderr.write(f"  ! Detail {shab_id}: {e}")
            return None

        meta = _find(root, "meta")
        content = _find(root, "content")
        commons = _find(content, "commonsNew") or content
        company = _find(commons, "company")
        if company is None:
            return None
        address = _find(company, "address")

        code = _text(company, "legalForm")
        legal = LEGAL_FORMS.get(code, "")
        if not legal:
            txt = _text(content, "publicationText")
            m = re.search(r",\s*([^,]+?)\s*\(Neueintragung\)", txt)
            legal = m.group(1).strip() if m else code

        return {
            "shab_id": shab_id,
            "publication_number": _text(meta, "publicationNumber"),
            "publication_date": _text(meta, "publicationDate") or None,
            "shab_url": DETAIL_URL.format(id=shab_id),
            "name": _text(company, "name"),
            "uid": _text(company, "uid"),
            "legal_form": legal,
            "seat": _text(company, "seat"),
            "canton": _text(meta, "cantons"),
            "street": _text(address, "street"),
            "house_number": _text(address, "houseNumber"),
            "zip_code": _text(address, "swissZipCode"),
            "town": _text(address, "town"),
            "purpose": _text(commons, "purpose"),
            "phone": "",
            "email": "",
            "website": "",
        }

    # ---- Anreicherung (search.ch) ----------------------------------------
    def _enrich(self, data):
        key = getattr(settings, "SEARCH_CH_API_KEY", "")
        if not key or not data["name"]:
            return
        try:
            r = requests.get(SEARCH_CH_URL, headers=HEADERS, timeout=20, params={
                "was": data["name"],
                "wo": data["zip_code"] or data["town"],
                "key": key,
                "maxnum": 1,
            })
            if r.status_code != 200:
                return
            root = ET.fromstring(r.content)
            entry = _find(root, "entry")
            if entry is None:
                return
            phone = _text(entry, "phone")
            if phone:
                data["phone"] = phone
            for ex in entry.iter():
                if _local(ex.tag) == "extra":
                    t = ex.get("type")
                    v = (ex.text or "").strip()
                    if t == "email" and v and not data["email"]:
                        data["email"] = v
                    elif t == "website" and v and not data["website"]:
                        data["website"] = v
            if not data["website"]:
                data["website"] = _text(entry, "website")
        except Exception as e:
            self.stderr.write(f"  ~ search.ch {data['name']}: {e}")

    # ---- Anreicherung (Zefix) --------------------------------------------
    def _enrich_zefix(self, data):
        data.setdefault("zefix_status", "")
        data.setdefault("zefix_url", "")
        data.setdefault("zefix_excerpt_url", "")
        if not zefix.enabled() or not data.get("uid"):
            return
        info = zefix.by_uid(data["uid"])
        if not info:
            return
        data["zefix_status"] = info.get("status", "")
        data["zefix_url"] = info.get("zefix_url", "")
        data["zefix_excerpt_url"] = info.get("excerpt_url", "")
        if info.get("canton") and not data.get("canton"):
            data["canton"] = info["canton"]

    # ---- Digest-Mail ------------------------------------------------------
    def _send_digest(self, items):
        today = timezone.localdate().strftime("%d.%m.%Y")
        subject = f"{len(items)} neue Firma(en) im Einzugsgebiet ({today})"

        lines = []
        rows = []
        for d in items:
            addr = ", ".join(x for x in [
                f"{d['street']} {d['house_number']}".strip(),
                f"{d['zip_code']} {d['town']}".strip()] if x)
            contact = " · ".join(x for x in [d["phone"], d["email"], d["website"]] if x)
            lines.append(
                f"- {d['name']} ({d['legal_form']})\n"
                f"  {addr}\n"
                + (f"  {contact}\n" if contact else "")
                + f"  Zweck: {(d['purpose'] or '')[:200]}\n"
                f"  {d['shab_url']}\n")
            rows.append(f"""
              <tr>
                <td style="padding:14px 16px;border-bottom:1px solid #EEE;vertical-align:top">
                  <strong style="font-size:15px">{escape(d['name'])}</strong>
                  <span style="color:#888"> · {escape(d['legal_form'])}</span><br>
                  <span style="color:#444">{escape(addr)}</span><br>
                  {('<span style="color:#F48B2D">' + escape(contact) + '</span><br>') if contact else ''}
                  <span style="color:#666;font-size:13px">{escape((d['purpose'] or '')[:220])}</span><br>
                  <a href="{escape(d['shab_url'])}" style="font-size:12px;color:#888">SHAB-Eintrag</a>
                </td>
              </tr>""")

        text_body = (f"{len(items)} neue Firmengründung(en) im Einzugsgebiet:\n\n"
                     + "\n".join(lines))
        html_body = f"""<div style="font-family:Arial,sans-serif;max-width:640px">
          <h2 style="font-size:18px">{len(items)} neue Firma(en) im Einzugsgebiet</h2>
          <p style="color:#888;font-size:13px">Handelsregister-Neueintragungen (SHAB), {today}</p>
          <table style="width:100%;border-collapse:collapse;border:1px solid #EEE">{''.join(rows)}</table>
          <p style="color:#aaa;font-size:12px;margin-top:16px">
            Telefon/E-Mail wo verfügbar via search.ch. Pflege im Admin unter „Neue Firmen".</p>
        </div>"""

        msg = EmailMultiAlternatives(
            subject, text_body, settings.DEFAULT_FROM_EMAIL,
            [settings.SHAB_DIGEST_EMAIL])
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
