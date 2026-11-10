# leadgen/models.py
# Lead-Gen-/CRM-Models (SHAB-Neugründungen, Makler-Leads, Akquise-Leads).
# Am 10.11.2026 aus der `web`-App ausgegliedert (App-Split website/leadgen).
# Die physischen DB-Tabellen heissen weiterhin web_* (siehe Meta.db_table),
# damit der Split OHNE Datenbewegung auskommt (SeparateDatabaseAndState).
from django.db import models
from django.utils.translation import gettext_lazy as _


class NewCompany(models.Model):
    """Neu gegründete Firma aus dem SHAB (Handelsregister-Neueintragung HR01).

    Wird vom Management-Command `fetch_new_companies` befüllt und im Admin
    als Lead-Liste gepflegt. Telefon/E-Mail/Website werden – wenn möglich –
    über die search.ch-Telefonbuch-API angereichert (nicht im HR enthalten).
    """

    STATUS_NEW = "new"
    STATUS_CONTACTED = "contacted"
    STATUS_NO_INTEREST = "no_interest"
    STATUS_CUSTOMER = "customer"
    STATUS_CHOICES = [
        (STATUS_NEW, _("Neu")),
        (STATUS_CONTACTED, _("Kontaktiert")),
        (STATUS_NO_INTEREST, _("Kein Interesse")),
        (STATUS_CUSTOMER, _("Kunde")),
    ]

    # SHAB-Herkunft (Dedupe über shab_id)
    shab_id = models.CharField(max_length=64, unique=True)
    publication_number = models.CharField(max_length=40, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    shab_url = models.URLField(blank=True)

    # Firmendaten aus dem Handelsregister
    name = models.CharField(max_length=255)
    uid = models.CharField("UID", max_length=20, blank=True)
    legal_form = models.CharField(_("Rechtsform"), max_length=80, blank=True)
    seat = models.CharField(_("Sitz"), max_length=120, blank=True)
    canton = models.CharField(_("Kanton"), max_length=2, blank=True)
    street = models.CharField(_("Strasse"), max_length=160, blank=True)
    house_number = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField("PLZ", max_length=10, blank=True)
    town = models.CharField(_("Ort"), max_length=120, blank=True)
    purpose = models.TextField(_("Zweck"), blank=True)

    # Angereichert (search.ch) – nicht im Handelsregister enthalten
    phone = models.CharField(_("Telefon"), max_length=40, blank=True)
    email = models.EmailField(_("E-Mail"), blank=True)
    website = models.URLField(_("Website"), blank=True)
    contact_person = models.CharField(_("Kontaktperson"), max_length=255, blank=True)

    # Lead-Pflege
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    notes = models.TextField(_("Notizen"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Zefix-Anreicherung (Handelsregister-Index)
    zefix_status = models.CharField(_("Register-Status"), max_length=20, blank=True)
    zefix_url = models.URLField(_("Zefix-Link"), max_length=400, blank=True)
    zefix_excerpt_url = models.URLField(_("HR-Auszug"), max_length=400, blank=True)

    # Odoo-CRM-Sync
    odoo_lead_id = models.IntegerField(_("Odoo-Lead-ID"), null=True, blank=True)
    odoo_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "web_newcompany"          # Tabelle bleibt (kein Daten-Umzug)
        verbose_name = _("Neue Firma")
        verbose_name_plural = _("Neue Firmen")
        ordering = ("-publication_date", "-created_at")

    def __str__(self):
        return f"{self.name} ({self.town})"

    @property
    def address_line(self):
        parts = [p for p in [f"{self.street} {self.house_number}".strip(),
                             f"{self.zip_code} {self.town}".strip()] if p]
        return ", ".join(parts)


class RealEstateLead(models.Model):
    """Immobilien-/Maklerfirma als Monekey-Lead (importiert aus Maklerliste).

    Eigener Lead-Strom (Zielgruppe Monekey), getrennt von den SHAB-
    Neugründungen. Enthält i. d. R. bereits Telefon und Website.
    """

    STATUS_CHOICES = NewCompany.STATUS_CHOICES  # gleiche Status-Logik

    external_id = models.CharField(max_length=40, unique=True)  # z. B. immoscout-ID
    name = models.CharField(max_length=255)
    zip_code = models.CharField("PLZ", max_length=10, blank=True)
    city = models.CharField(_("Ort"), max_length=120, blank=True)
    street = models.CharField(_("Strasse"), max_length=200, blank=True)
    full_address = models.CharField(_("Adresse"), max_length=300, blank=True)
    website = models.CharField(_("Website"), max_length=300, blank=True)
    phone = models.CharField(_("Telefon"), max_length=60, blank=True)
    email = models.CharField(_("E-Mail"), max_length=200, blank=True)
    source_url = models.URLField(_("Quelle"), max_length=400, blank=True)
    marketplace = models.CharField(_("Marktplatz"), max_length=40, blank=True)

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default="new")
    notes = models.TextField(_("Notizen"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    odoo_lead_id = models.IntegerField(_("Odoo-Lead-ID"), null=True, blank=True)
    odoo_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "web_realestatelead"
        verbose_name = _("Immobilienfirma (Monekey)")
        verbose_name_plural = _("Immobilienfirmen (Monekey)")
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} ({self.city})"


class AcquisitionLead(models.Model):
    """Kurierter Akquise-Lead (Kleinbetrieb) aus der Region – für Datalization.

    Importiert aus einer gepflegten Excel-Liste (Blatt 'Leads'). Enthält
    Segment, Priorität, Grössen-Einschätzung und einen passenden
    Gesprächseinstieg. Prio kann auch 'Monekey'/'Partner' sein – danach
    richtet sich der Odoo-Tag beim Push.
    """

    STATUS_CHOICES = NewCompany.STATUS_CHOICES

    ext_key = models.CharField(max_length=200, unique=True)  # name+ort normalisiert
    name = models.CharField(max_length=255)
    segment = models.CharField(_("Segment"), max_length=160, blank=True)
    city = models.CharField(_("Ort"), max_length=120, blank=True)
    address = models.CharField(_("Adresse"), max_length=300, blank=True)
    phone = models.CharField(_("Telefon"), max_length=60, blank=True)
    priority = models.CharField(_("Prio"), max_length=20, blank=True)  # A/B/C/Monekey/Partner
    size_note = models.CharField(_("Grösse"), max_length=200, blank=True)
    employees = models.CharField(_("Mitarbeitende"), max_length=80, blank=True)
    size_source = models.CharField(_("Quelle Grösse"), max_length=200, blank=True)
    approach = models.TextField(_("Gesprächseinstieg"), blank=True)

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default="new")
    notes = models.TextField(_("Notizen"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    odoo_lead_id = models.IntegerField(_("Odoo-Lead-ID"), null=True, blank=True)
    odoo_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "web_acquisitionlead"
        verbose_name = _("Akquise-Lead (Datalization)")
        verbose_name_plural = _("Akquise-Leads (Datalization)")
        ordering = ("priority", "name")

    def __str__(self):
        return f"{self.name} ({self.city})"
