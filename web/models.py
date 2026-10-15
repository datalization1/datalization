# web/models.py
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _, get_language

class CaseStudy(models.Model):
    title       = models.CharField(max_length=160)
    category    = models.CharField(max_length=80, blank=True)
    slug        = models.SlugField(unique=True, blank=True)
    summary     = models.TextField(_("Solution (DE)"), blank=True,
        help_text=_("Deutsche Version des Lösungstexts."))
    summary_en  = models.TextField(_("Solution (EN)"), blank=True,
        help_text=_("English version of the solution text."))

    # ✨ NEU: Struktur à la Kreativstorm
    client_brief   = models.TextField(_("Client"), blank=True,
        help_text=_("Kurzbeschreibung des Kunden (keine Namen)."))
    problem_brief    = models.TextField(_("Problem (DE)"), blank=True,
        help_text=_("Deutsche Version: Welches Problem/Engpass bestand?"))
    problem_brief_en = models.TextField(_("Problem (EN)"), blank=True,
        help_text=_("English version of the challenge description."))
    result_points    = models.TextField(_("Result Bullet points (DE)"), blank=True,
        help_text=_("Deutsche Aufzählung, je Zeile ein Punkt."))
    result_points_en = models.TextField(_("Result Bullet points (EN)"), blank=True,
        help_text=_("English bullet points, one per line."))

    preview_animation = models.FileField(upload_to="cases/previews/", blank=True, null=True)
    image       = models.ImageField(upload_to="cases/", blank=True, null=True)
    date        = models.DateField()
    published   = models.BooleanField(
        _("Aktiv"),
        default=True,
        help_text=_("Steuert, ob diese Case Study auf der Website angezeigt wird."),
    )

    # Optional: vorhandene Felder beibehalten
    kpis        = models.JSONField(blank=True, null=True)
    tech_stack  = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)

    def _pick(self, de_value, en_value):
        lang = (get_language() or "").split("-")[0]
        if lang == "en" and en_value:
            return en_value
        return de_value

    @property
    def problem_localized(self):
        return self._pick(self.problem_brief, self.problem_brief_en)

    @property
    def summary_localized(self):
        return self._pick(self.summary, self.summary_en)

    def result_list(self):
        """Resultat-Zeilen als Liste (für Bullets), sprachabhängig."""
        source = self._pick(self.result_points, self.result_points_en)
        if not source:
            return []
        return [ln.strip() for ln in source.splitlines() if ln.strip()]

    @property
    def safe_image_url(self):
        if not self.image or not getattr(self.image, "name", ""):
            return ""
        try:
            if not self.image.storage.exists(self.image.name):
                return ""
            return self.image.url
        except Exception:
            return ""

    @property
    def safe_preview_animation_url(self):
        if not self.preview_animation or not getattr(self.preview_animation, "name", ""):
            return ""
        try:
            if not self.preview_animation.storage.exists(self.preview_animation.name):
                return ""
            return self.preview_animation.url
        except Exception:
            return ""

    class Meta:
        ordering = ["-date"]


class ContactMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    
    first_name = models.CharField(_("First name"), max_length=80)
    last_name = models.CharField(_("Last name"), max_length=80)
    company = models.CharField(_("Company"), max_length=150, blank=True, null=True)
    
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
    message = models.TextField(_("Message"))
    language = models.CharField(_("Language"), max_length=5, default="de")

    handled = models.BooleanField(_("Processed"), default=False)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Contact message")
        verbose_name_plural = _("Contact messages")

    def __str__(self):
        company_str = f" ({self.company})" if self.company else ""
        return f"{self.first_name} {self.last_name}{company_str} – {self.created:%Y-%m-%d}"


class StartRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(_("First name"), max_length=80)
    last_name = models.CharField(_("Last name"), max_length=80)
    company = models.CharField(_("Company"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
    branches = models.CharField(_("Branches"), max_length=255, blank=True, null=True)
    pains = models.CharField(_("Challenges"), max_length=255, blank=True, null=True)
    start_mode = models.CharField(_("Start mode"), max_length=80, blank=True, null=True)
    notes = models.TextField(_("Notes"), blank=True, null=True)
    language = models.CharField(_("Language"), max_length=5, default="de")

    handled = models.BooleanField(_("Processed"), default=False)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Start request")
        verbose_name_plural = _("Start requests")

    def __str__(self):
        company_str = f" ({self.company})" if self.company else ""
        return f"{self.first_name} {self.last_name}{company_str} – {self.created:%Y-%m-%d}"
        
class Page(models.Model):
    slug = models.SlugField(primary_key=True)
    title_de = models.CharField(max_length=160)
    title_en = models.CharField(max_length=160)
    body_de  = models.TextField(blank=True)
    body_en  = models.TextField(blank=True)


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

    # Lead-Pflege
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    notes = models.TextField(_("Notizen"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Odoo-CRM-Sync
    odoo_lead_id = models.IntegerField(_("Odoo-Lead-ID"), null=True, blank=True)
    odoo_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
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
        verbose_name = _("Akquise-Lead (Datalization)")
        verbose_name_plural = _("Akquise-Leads (Datalization)")
        ordering = ("priority", "name")

    def __str__(self):
        return f"{self.name} ({self.city})"
