from django.urls import path
from . import views

app_name = "web"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("cases/", views.case_list, name="cases"),
    path("cases/<slug:slug>/", views.case_detail, name="case_detail"),
]