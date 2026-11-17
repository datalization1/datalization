from django.urls import path
from . import views
from . import admin_views

app_name = "web"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("services/it-support/", views.service_it_support, name="service_it_support"),
    path("services/data-analytics/", views.service_data_analytics, name="service_data_analytics"),
    path("services/softwareentwicklung/", views.service_software, name="service_software"),
    path("services/digitalisierung/", views.service_digitalisierung, name="service_digitalisierung"),
    path("services/beratung-strategie/", views.service_beratung, name="service_beratung"),
    path("monekey/", views.monekey, name="monekey"),
    path("start/", views.start, name="start"),
    path("start/submit/", views.start_submit, name="start_submit"),
    path("booking/", views.booking, name="booking"),
    path("match/", views.match, name="match"),
    # Eigenständige Datalization-Admin (unabhängig von der Django-Admin).
    path("custom-admin/login/", admin_views.admin_login, name="admin_login"),
    path("custom-admin/logout/", admin_views.admin_logout, name="admin_logout"),
    path("custom-admin/", admin_views.admin_dashboard, name="custom_admin"),
    path("custom-admin/kontakte/", admin_views.admin_contacts, name="admin_contacts"),
    path("custom-admin/buchungen/", admin_views.admin_bookings, name="admin_bookings"),
    path("custom-admin/referenzen/", admin_views.admin_cases, name="admin_cases"),
    path("custom-admin/referenzen/neu/", admin_views.admin_case_edit, name="admin_case_new"),
    path("custom-admin/referenzen/<int:pk>/", admin_views.admin_case_edit, name="admin_case_edit"),
    path("custom-admin/inhalte/", admin_views.admin_content, name="admin_content"),
    path("custom-admin/inhalte/neu/", admin_views.admin_content_edit, name="admin_content_new"),
    path("custom-admin/inhalte/<int:pk>/", admin_views.admin_content_edit, name="admin_content_edit"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"), 

    path("cases/", views.case_list, name="cases"),
    path("cases/<slug:slug>/", views.case_detail, name="case_detail"),
    
    path("impressum/", views.impressum, name="impressum"),
    path("datenschutz/", views.privacy, name="privacy"),
]
