from django import forms
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from .models import CaseStudy, ContactMessage, ContentBlock, StartRequest


class CaseStudyForm(forms.ModelForm):
    class Meta:
        model = CaseStudy
        fields = ["title", "category", "slug", "date", "published",
                  "image", "preview_animation", "client_brief",
                  "problem_brief", "summary", "result_points",
                  "problem_brief_en", "summary_en", "result_points_en",
                  "tech_stack"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "f-input"}),
            "category": forms.TextInput(attrs={"class": "f-input"}),
            "slug": forms.TextInput(attrs={"class": "f-input", "placeholder": _("leer = aus Titel")}),
            "date": forms.DateInput(attrs={"class": "f-input", "type": "date"}),
            "tech_stack": forms.TextInput(attrs={"class": "f-input"}),
            "client_brief": forms.Textarea(attrs={"class": "f-textarea", "rows": 2}),
            "problem_brief": forms.Textarea(attrs={"class": "f-textarea", "rows": 3}),
            "summary": forms.Textarea(attrs={"class": "f-textarea", "rows": 3}),
            "result_points": forms.Textarea(attrs={"class": "f-textarea", "rows": 4}),
            "problem_brief_en": forms.Textarea(attrs={"class": "f-textarea", "rows": 3}),
            "summary_en": forms.Textarea(attrs={"class": "f-textarea", "rows": 3}),
            "result_points_en": forms.Textarea(attrs={"class": "f-textarea", "rows": 4}),
        }


class ContentBlockForm(forms.ModelForm):
    class Meta:
        model = ContentBlock
        fields = ["key", "label", "text_de", "text_en", "image"]
        widgets = {
            "key": forms.TextInput(attrs={"class": "f-input", "placeholder": "home_hero_title"}),
            "label": forms.TextInput(attrs={"class": "f-input"}),
            "text_de": forms.Textarea(attrs={"class": "f-textarea", "rows": 4}),
            "text_en": forms.Textarea(attrs={"class": "f-textarea", "rows": 4}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        # 'service' = das im Kontaktformular gewählte Anliegen/Thema (<select name="service">).
        # Fehlte hier bisher → wurde nie gespeichert → in der Mail stand «Anliegen: -».
        fields = ["first_name", "last_name", "company", "email", "phone", "service", "message"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": _("Vorname"), "class": "form-input"}),
            "last_name":  forms.TextInput(attrs={"placeholder": _("Nachname"), "class": "form-input"}),
            "company":    forms.TextInput(attrs={"placeholder": _("Firma (optional)"), "class": "form-input"}),
            "email":      forms.EmailInput(attrs={"placeholder": _("Ihre E-Mail"), "class": "form-input"}),
            "phone":      forms.TextInput(attrs={"placeholder": _("Telefon (optional)"), "class": "form-input", "type": "tel"}),
            "message":    forms.Textarea(attrs={"rows": 6, "placeholder": _("Ihre Nachricht…"), "class": "form-textarea"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Anliegen ist serverseitig Pflicht (das Modellfeld ist blank=True).
        self.fields["service"].required = True
        self.fields["service"].error_messages["required"] = _("Bitte wählen Sie ein Anliegen.")

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        validate_email(email)
        return email

    def clean_service(self):
        # Leerer Select-Default ("Bitte wählen") zählt als fehlendes Pflichtfeld.
        service = (self.cleaned_data.get("service") or "").strip()
        if not service:
            raise forms.ValidationError(_("Bitte wählen Sie ein Anliegen."))
        return service


class StartForm(forms.ModelForm):
    class Meta:
        model = StartRequest
        fields = [
            "first_name",
            "last_name",
            "company",
            "email",
            "phone",
            "branches",
            "pains",
            "start_mode",
            "notes",
            "language",
        ]

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        validate_email(email)
        return email
