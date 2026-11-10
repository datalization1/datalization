# leadgen/admin.py
# CRM-/Lead-Admin (NewCompany, RealEstateLead, AcquisitionLead) – aus web ausgegliedert.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# ---------------------------------------------------------------------------
# Neue Firmen (SHAB-Handelsregister-Monitor) – Lead-Liste
# ---------------------------------------------------------------------------
from .models import NewCompany


@admin.register(NewCompany)
class NewCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "town", "canton", "legal_form", "zefix_status",
                    "publication_date", "contact_person", "phone", "email", "status", "in_odoo")
    list_filter = ("status", "zefix_status", "canton", "publication_date", "legal_form", "town")
    search_fields = ("name", "town", "zip_code", "uid", "purpose", "phone", "email")
    list_editable = ("status",)
    date_hierarchy = "publication_date"
    ordering = ("-publication_date", "-created_at")
    list_per_page = 50
    actions = ("push_to_odoo", "export_csv")
    readonly_fields = ("shab_id", "publication_number", "publication_date", "shab_url",
                       "name", "uid", "legal_form", "seat", "canton",
                       "street", "house_number", "zip_code", "town", "purpose",
                       "contact_person", "zefix_status", "zefix_url", "zefix_excerpt_url",
                       "created_at", "odoo_lead_id", "odoo_synced_at")
    fieldsets = (
        (_("Firma"), {"fields": ("name", "legal_form", "uid", ("zip_code", "town"),
                                  ("street", "house_number"), "seat", "canton", "purpose")}),
        (_("Kontakt"), {"fields": ("contact_person", "phone", "email", "website")}),
        (_("Zefix (Handelsregister)"), {"fields": ("zefix_status", "zefix_url", "zefix_excerpt_url")}),
        (_("Lead"), {"fields": ("status", "notes")}),
        (_("Odoo CRM"), {"fields": ("odoo_lead_id", "odoo_synced_at")}),
        (_("Quelle"), {"fields": ("publication_date", "publication_number", "shab_url", "shab_id", "created_at"),
                       "classes": ("collapse",)}),
    )

    @admin.display(description="Odoo", boolean=True)
    def in_odoo(self, obj):
        return bool(obj.odoo_lead_id)

    @admin.action(description=_("Als CSV exportieren (Excel)"))
    def export_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        resp = HttpResponse(content_type="text/csv; charset=utf-8")
        resp["Content-Disposition"] = "attachment; filename=shab_neugruendungen.csv"
        resp.write("﻿")  # BOM, damit Excel Umlaute korrekt zeigt
        w = csv.writer(resp, delimiter=";")
        w.writerow(["Firma", "Rechtsform", "PLZ", "Ort", "Kanton", "Gründungsdatum",
                    "Kontaktperson", "UID", "Register-Status", "Telefon", "E-Mail",
                    "Zweck", "Zefix-Link", "SHAB-Link", "In Odoo"])
        for o in queryset:
            pd = o.publication_date.strftime("%d.%m.%Y") if o.publication_date else ""
            w.writerow([o.name, o.legal_form, o.zip_code, o.town, o.canton, pd,
                        o.contact_person, o.uid, o.zefix_status, o.phone, o.email,
                        (o.purpose or "")[:300], o.zefix_url, o.shab_url,
                        "ja" if o.odoo_lead_id else ""])
        return resp

    @admin.action(description=_("Ausgewählte als Leads nach Odoo pushen"))
    def push_to_odoo(self, request, queryset):
        from django.contrib import messages
        from leadgen import odoo_crm
        if not odoo_crm.enabled():
            self.message_user(request, _("Odoo ist nicht konfiguriert "
                              "(ODOO_URL/DB/USERNAME/API_KEY)."), level=messages.ERROR)
            return
        try:
            client = odoo_crm.OdooClient()
        except Exception as e:
            self.message_user(request, f"Odoo-Verbindung fehlgeschlagen: {e}",
                              level=messages.ERROR)
            return
        pushed, skipped, failed = 0, 0, 0
        for obj in queryset:
            if obj.odoo_lead_id:
                skipped += 1
                continue
            try:
                odoo_crm.push_company(obj, client=client)
                pushed += 1
            except Exception as e:
                failed += 1
                self.message_user(request, f"{obj.name}: {e}", level=messages.WARNING)
        self.message_user(
            request,
            _("Odoo: %(p)d gepusht, %(s)d bereits vorhanden, %(f)d fehlgeschlagen.")
            % {"p": pushed, "s": skipped, "f": failed},
            level=messages.SUCCESS if not failed else messages.WARNING)


# ---------------------------------------------------------------------------
# Immobilienfirmen (Monekey-Leads) – importierte Maklerliste
# ---------------------------------------------------------------------------
from .models import RealEstateLead


@admin.register(RealEstateLead)
class RealEstateLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "zip_code", "city", "phone", "website",
                    "marketplace", "status", "in_odoo")
    list_filter = ("status", "marketplace", "city")
    search_fields = ("name", "city", "zip_code", "phone", "email", "website")
    list_editable = ("status",)
    ordering = ("name",)
    list_per_page = 50
    actions = ("push_to_odoo",)
    readonly_fields = ("external_id", "name", "zip_code", "city", "street",
                       "full_address", "website", "phone", "email", "source_url",
                       "marketplace", "created_at", "odoo_lead_id", "odoo_synced_at")
    fieldsets = (
        (_("Firma"), {"fields": ("name", ("zip_code", "city"), "street", "full_address")}),
        (_("Kontakt"), {"fields": ("phone", "email", "website")}),
        (_("Lead"), {"fields": ("status", "notes")}),
        (_("Odoo CRM"), {"fields": ("odoo_lead_id", "odoo_synced_at")}),
        (_("Quelle"), {"fields": ("marketplace", "source_url", "external_id", "created_at"),
                       "classes": ("collapse",)}),
    )

    @admin.display(description="Odoo", boolean=True)
    def in_odoo(self, obj):
        return bool(obj.odoo_lead_id)

    @admin.action(description=_("Ausgewählte als Leads nach Odoo pushen (Monekey)"))
    def push_to_odoo(self, request, queryset):
        from django.contrib import messages
        from leadgen import odoo_crm
        if not odoo_crm.enabled():
            self.message_user(request, _("Odoo ist nicht konfiguriert."),
                              level=messages.ERROR)
            return
        try:
            client = odoo_crm.OdooClient()
        except Exception as e:
            self.message_user(request, f"Odoo-Verbindung fehlgeschlagen: {e}",
                              level=messages.ERROR)
            return
        pushed = skipped = failed = 0
        for obj in queryset:
            if obj.odoo_lead_id:
                skipped += 1
                continue
            try:
                odoo_crm.push_broker(obj, client=client)
                pushed += 1
            except Exception as e:
                failed += 1
                self.message_user(request, f"{obj.name}: {e}", level=messages.WARNING)
        self.message_user(
            request,
            _("Odoo: %(p)d gepusht, %(s)d bereits vorhanden, %(f)d fehlgeschlagen.")
            % {"p": pushed, "s": skipped, "f": failed},
            level=messages.SUCCESS if not failed else messages.WARNING)


# ---------------------------------------------------------------------------
# Akquise-Leads (Datalization) – kuratierte Kleinbetriebe aus der Region
# ---------------------------------------------------------------------------
from .models import AcquisitionLead


@admin.register(AcquisitionLead)
class AcquisitionLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "segment", "priority", "phone", "status", "in_odoo")
    list_filter = ("priority", "status", "city", "segment")
    search_fields = ("name", "city", "segment", "phone", "approach")
    list_editable = ("status",)
    ordering = ("priority", "name")
    list_per_page = 50
    actions = ("push_to_odoo",)
    readonly_fields = ("ext_key", "name", "segment", "city", "address", "phone",
                       "priority", "size_note", "employees", "size_source", "approach",
                       "created_at", "odoo_lead_id", "odoo_synced_at")
    fieldsets = (
        (_("Firma"), {"fields": ("name", "segment", ("city", "address"), "phone")}),
        (_("Einschätzung"), {"fields": ("priority", "size_note", "employees", "size_source", "approach")}),
        (_("Lead"), {"fields": ("status", "notes")}),
        (_("Odoo CRM"), {"fields": ("odoo_lead_id", "odoo_synced_at")}),
        (_("Quelle"), {"fields": ("ext_key", "created_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Odoo", boolean=True)
    def in_odoo(self, obj):
        return bool(obj.odoo_lead_id)

    @admin.action(description=_("Ausgewählte als Leads nach Odoo pushen"))
    def push_to_odoo(self, request, queryset):
        from django.contrib import messages
        from leadgen import odoo_crm
        if not odoo_crm.enabled():
            self.message_user(request, _("Odoo ist nicht konfiguriert."), level=messages.ERROR)
            return
        try:
            client = odoo_crm.OdooClient()
        except Exception as e:
            self.message_user(request, f"Odoo-Verbindung fehlgeschlagen: {e}", level=messages.ERROR)
            return
        pushed = skipped = failed = 0
        for obj in queryset:
            if obj.odoo_lead_id:
                skipped += 1
                continue
            try:
                odoo_crm.push_acquisition(obj, client=client)
                pushed += 1
            except Exception as e:
                failed += 1
                self.message_user(request, f"{obj.name}: {e}", level=messages.WARNING)
        self.message_user(
            request,
            _("Odoo: %(p)d gepusht, %(s)d bereits vorhanden, %(f)d fehlgeschlagen.")
            % {"p": pushed, "s": skipped, "f": failed},
            level=messages.SUCCESS if not failed else messages.WARNING)
