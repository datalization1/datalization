from django.contrib import admin
from .models import CaseStudy, ContactMessage
from django.utils.translation import gettext_lazy as _

# web/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CaseStudy

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display  = ("title", "category", "date", "published")
    list_filter   = ("published", "category", "date")
    search_fields = ("title", "summary", "client_brief", "problem_brief", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (None, {"fields": ("title", "category", "slug", "summary", "image", "date", "published")}),
        (_("Client / Problem / Result"), {
            "fields": ("client_brief", "problem_brief", "result_points"),
            "description": _("Beim Result jeweils eine Aussage pro Zeile. "),
        }),
        (_("KPIs & Tech"), {
            "fields": ("kpis", "tech_stack"),
        }),
    )

    formfield_overrides = {
        # Grössere Textareas im Admin
        # Optional: auskommentieren falls nicht gewünscht
        # models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'rows': 6})},
    }
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("created","first_name","last_name","company","email","language","handled")
    list_filter = ("handled","language","created")
    search_fields = ("first_name","last_name","company","email","message")
    readonly_fields = ("created","first_name","last_name","company","email","message","language")
    actions = ["mark_as_handled"]

    @admin.action(description="Mark selected messages as processed")
    def mark_as_handled(self, request, queryset):
        queryset.update(handled=True)