# web/models.py
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# web/models.py
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

class CaseStudy(models.Model):
    title       = models.CharField(max_length=160)
    category    = models.CharField(max_length=80, blank=True)
    slug        = models.SlugField(unique=True, blank=True)
    summary     = models.TextField(blank=True)

    # ✨ NEU: Struktur à la Kreativstorm
    client_brief   = models.TextField(_("Client"), blank=True,
        help_text=_("Kurzbeschreibung des Kunden (keine Namen)."))
    problem_brief  = models.TextField(_("Problem"), blank=True,
        help_text=_("Welches Problem/Engpass bestand?"))
    result_points  = models.TextField(_("Result (Bullet points)"), blank=True,
        help_text=_("Eine Aufzählung, je Zeile ein Punkt."))

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

    def result_list(self):
        """Resultat-Zeilen als Liste (für Bullets)."""
        if not self.result_points:
            return []
        # Split by lines, trim and drop empties
        return [ln.strip() for ln in self.result_points.splitlines() if ln.strip()]

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
