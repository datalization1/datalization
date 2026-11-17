from django import forms
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage, StartRequest

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
