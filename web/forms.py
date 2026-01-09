from django import forms
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage, StartRequest

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "company", "email", "phone", "message"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": _("Vorname"), "class": "form-input"}),
            "last_name":  forms.TextInput(attrs={"placeholder": _("Nachname"), "class": "form-input"}),
            "company":    forms.TextInput(attrs={"placeholder": _("Firma (optional)"), "class": "form-input"}),
            "email":      forms.EmailInput(attrs={"placeholder": _("Ihre E-Mail"), "class": "form-input"}),
            "phone":      forms.TextInput(attrs={"placeholder": _("Telefon (optional)"), "class": "form-input", "type": "tel"}),
            "message":    forms.Textarea(attrs={"rows": 6, "placeholder": _("Ihre Nachricht…"), "class": "form-textarea"}),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip()
        validate_email(email)
        return email


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
