from django.urls import path
from . import views

app_name = "web"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("services/data-analytics/", views.service_data_analytics, name="service_data_analytics"),
    path("services/softwareentwicklung/", views.service_software, name="service_software"),
    path("services/digitalisierung/", views.service_digitalisierung, name="service_digitalisierung"),
    path("services/beratung-strategie/", views.service_beratung, name="service_beratung"),
    path("start/", views.start, name="start"),
    path("start/submit/", views.start_submit, name="start_submit"),
    path("match/", views.match, name="match"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"), 

    path("cases/", views.case_list, name="cases"),
    path("cases/<slug:slug>/", views.case_detail, name="case_detail"),
    
    path("impressum/", views.impressum, name="impressum"),
    path("datenschutz/", views.privacy, name="privacy"),
]
