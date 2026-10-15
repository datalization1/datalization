"""Odoo-CRM-Anbindung (optional): Neugründungen als crm.lead nach Odoo pushen.

Nutzt die externe Odoo-API via XML-RPC. Aktiv, sobald ODOO_URL, ODOO_DB,
ODOO_USERNAME und ODOO_API_KEY in den Settings/der .env gesetzt sind.
"""
import xmlrpc.client

from django.conf import settings
from django.utils import timezone


def _config():
    return (
        getattr(settings, "ODOO_URL", "").rstrip("/"),
        getattr(settings, "ODOO_DB", ""),
        getattr(settings, "ODOO_USERNAME", ""),
        getattr(settings, "ODOO_API_KEY", ""),
    )


def enabled():
    return all(_config())


class OdooClient:
    """Dünner XML-RPC-Wrapper; authentifiziert einmal pro Instanz."""

    def __init__(self):
        self.url, self.db, self.user, self.key = _config()
        if not all((self.url, self.db, self.user, self.key)):
            raise RuntimeError("Odoo ist nicht konfiguriert (ODOO_URL/DB/USERNAME/API_KEY).")
        common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common", allow_none=True)
        self.uid = common.authenticate(self.db, self.user, self.key, {})
        if not self.uid:
            raise RuntimeError("Odoo-Authentifizierung fehlgeschlagen (Login/API-Key prüfen).")
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object", allow_none=True)
        self._country_ch = None
        self._tags = {}

    def _execute(self, model, method, *args, **kw):
        return self.models.execute_kw(self.db, self.uid, self.key, model, method, list(args), kw)

    def country_ch_id(self):
        if self._country_ch is None:
            res = self._execute("res.country", "search", [["code", "=", "CH"]], limit=1)
            self._country_ch = res[0] if res else False
        return self._country_ch

    def tag_id(self, name):
        """ID eines crm.tag (wird bei Bedarf angelegt)."""
        if name in self._tags:
            return self._tags[name]
        res = self._execute("crm.tag", "search", [["name", "=", name]], limit=1)
        tid = res[0] if res else self._execute("crm.tag", "create", {"name": name})
        self._tags[name] = tid
        return tid

    def create_broker_lead(self, company):
        """Legt einen crm.lead aus einer RealEstateLead-Instanz an (Monekey)."""
        desc = "\n".join(x for x in [
            f"Website: {company.website}" if company.website else "",
            f"Quelle: {company.source_url}" if company.source_url else "",
            f"Marktplatz: {company.marketplace}" if company.marketplace else "",
        ] if x)
        vals = {
            "name": f"{company.name} – Immobilien (Monekey)",
            "type": "lead",
            "partner_name": company.name,
            "street": company.street or False,
            "zip": company.zip_code or False,
            "city": company.city or False,
            "country_id": self.country_ch_id() or False,
            "phone": company.phone or False,
            "email_from": company.email or False,
            "website": company.website or False,
            "description": desc or False,
            "tag_ids": [(6, 0, [self.tag_id("Monekey – Immobilien")])],
        }
        return self._execute("crm.lead", "create", vals)

    def create_lead(self, company):
        """Legt einen crm.lead aus einer NewCompany-Instanz an, gibt die ID zurück."""
        street = " ".join(x for x in [company.street, company.house_number] if x).strip()
        desc = "\n".join(x for x in [
            f"Rechtsform: {company.legal_form}" if company.legal_form else "",
            f"UID: {company.uid}" if company.uid else "",
            f"Sitz: {company.seat} ({company.canton})" if company.seat else "",
            f"Gegründet / publiziert: {company.publication_date}" if company.publication_date else "",
            f"Zweck: {company.purpose}" if company.purpose else "",
            f"SHAB: {company.shab_url}" if company.shab_url else "",
        ] if x)
        vals = {
            "name": f"{company.name} – Neugründung {company.town}".strip(),
            "type": "lead",
            "partner_name": company.name,
            "street": street or False,
            "zip": company.zip_code or False,
            "city": company.town or False,
            "country_id": self.country_ch_id() or False,
            "phone": company.phone or False,
            "email_from": company.email or False,
            "website": company.website or False,
            "description": desc or False,
        }
        return self._execute("crm.lead", "create", vals)


def push_company(company, client=None):
    """Pusht eine NewCompany nach Odoo (sofern noch nicht gepusht).

    Gibt die Odoo-Lead-ID zurück oder None. Fehler werden nach oben geworfen,
    damit der Aufrufer sie je nach Kontext behandeln/loggen kann.
    """
    if company.odoo_lead_id:
        return company.odoo_lead_id
    client = client or OdooClient()
    lead_id = client.create_lead(company)
    company.odoo_lead_id = lead_id
    company.odoo_synced_at = timezone.now()
    company.save(update_fields=["odoo_lead_id", "odoo_synced_at"])
    return lead_id


def push_broker(company, client=None):
    """Pusht eine RealEstateLead (Monekey) nach Odoo, sofern noch nicht gepusht."""
    if company.odoo_lead_id:
        return company.odoo_lead_id
    client = client or OdooClient()
    lead_id = client.create_broker_lead(company)
    company.odoo_lead_id = lead_id
    company.odoo_synced_at = timezone.now()
    company.save(update_fields=["odoo_lead_id", "odoo_synced_at"])
    return lead_id
