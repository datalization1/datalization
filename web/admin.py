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
    search_fields = (
        "title", "summary", "summary_en",
        "client_brief", "problem_brief", "problem_brief_en", "tech_stack",
    )
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("published",)

    fieldsets = (
        (None, {"fields": ("title", "category", "slug", "preview_animation", "image", "date", "published")}),
        (_("Client"), {
            "fields": ("client_brief",),
        }),
        (_("Deutsche Version"), {
            "fields": ("problem_brief", "summary", "result_points"),
            "description": _("Beim Result jeweils eine Aussage pro Zeile."),
        }),
        (_("English Version"), {
            "fields": ("problem_brief_en", "summary_en", "result_points_en"),
            "description": _("Optional. Falls leer, wird auf die deutsche Version zurückgegriffen."),
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
