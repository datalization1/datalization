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

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("web:case_detail", kwargs={"slug": self.slug})


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
    service = models.CharField(
        _("Requested service"), max_length=60, blank=True,
        help_text=_("Auswahl aus dem Kontaktformular."),
    )
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
