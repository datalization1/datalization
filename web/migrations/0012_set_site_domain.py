from django.conf import settings
from django.db import migrations
import os


def set_site_domain(apps, schema_editor):
    """Der Sites-Eintrag steht per Default auf example.com. Die Sitemap baut ihre
    URLs daraus, deshalb muss hier die echte Domain stehen."""
    Site = apps.get_model("sites", "Site")
    domain = os.getenv("SITE_DOMAIN", "www.datalization.ch")
    Site.objects.update_or_create(
        pk=getattr(settings, "SITE_ID", 1),
        defaults={"domain": domain, "name": "datalization"},
    )


def unset_site_domain(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    Site.objects.filter(pk=getattr(settings, "SITE_ID", 1)).update(
        domain="example.com", name="example.com"
    )


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0011_casestudy_problem_brief_en_and_more"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(set_site_domain, unset_site_domain),
    ]
