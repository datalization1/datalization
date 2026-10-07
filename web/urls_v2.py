"""
URL-Konfiguration für die Website v2.0.

Eigener Namespace "v2", eingehängt unter dem Präfix /v2/ (siehe
datalization_site/urls.py). Verändert web/urls.py NICHT.
"""
from django.urls import path
from . import views_v2

app_name = "v2"

urlpatterns = [
    path("", views_v2.v2_home, name="home"),
    path("odoo/", views_v2.v2_odoo, name="odoo"),
    path("odoo/wieso-odoo/", views_v2.v2_odoo_wieso, name="odoo_wieso"),
    path("odoo/einfuehrung/", views_v2.v2_odoo_einfuehrung, name="odoo_einfuehrung"),
    path("odoo/vergleich/", views_v2.v2_odoo_vergleich, name="odoo_vergleich"),
    path("data-analytics/", views_v2.v2_data_analytics, name="data_analytics"),
    path("digitalisierung/", views_v2.v2_digitalisierung, name="digitalisierung"),
    path("monekey/", views_v2.v2_monekey, name="monekey"),
    path("odoo-partner-zofingen/", views_v2.v2_odoo_partner, name="odoo_partner"),
    path("ueber-datalization/", views_v2.v2_ueber_datalization, name="ueber_datalization"),
    path("impressum/", views_v2.v2_impressum, name="impressum"),
    path("datenschutz/", views_v2.v2_datenschutz, name="datenschutz"),
    path("geschaeftssoftware-kmu/", views_v2.v2_seo_erp_kmu, name="seo_erp_kmu"),
    path("buchhaltungssoftware-kmu/", views_v2.v2_seo_buchhaltung, name="seo_buchhaltung"),
    path("odoo-fuer-treuhaender/", views_v2.v2_seo_treuhand, name="seo_treuhand"),
    path("odoo-handwerk-gewerbe/", views_v2.v2_seo_handwerk, name="seo_handwerk"),
    path("odoo-partner-olten/", views_v2.v2_seo_olten, name="seo_olten"),
    path("kontakt/", views_v2.v2_kontakt, name="kontakt"),
    path("booking/", views_v2.v2_booking, name="booking"),
    path("booking/submit/", views_v2.v2_booking_submit, name="booking_submit"),
]
