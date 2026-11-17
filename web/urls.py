from django.urls import path
from django.views.generic import RedirectView
from . import views

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
    # Stillgelegt: die selbstgebaute Admin leitet jetzt auf die Django-Admin.
    # View/Templates (views.custom_admin, custom_admin*.html) bleiben vorerst,
    # sind aber nicht mehr verdrahtet. Name bleibt, damit reverse()-Aufrufe halten.
    path("custom-admin/", RedirectView.as_view(url="/admin/", permanent=False), name="custom_admin"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"), 

    path("cases/", views.case_list, name="cases"),
    path("cases/<slug:slug>/", views.case_detail, name="case_detail"),
    
    path("impressum/", views.impressum, name="impressum"),
    path("datenschutz/", views.privacy, name="privacy"),
]
