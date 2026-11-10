# App-Split website/leadgen (10.11.2026):
# Die 3 Lead-Models verlassen die State-Verwaltung der `web`-App. Die physischen
# Tabellen (web_newcompany/-realestatelead/-acquisitionlead) bleiben UNANGETASTET
# und werden künftig von der `leadgen`-App verwaltet (siehe leadgen/0001_initial).
# Darum SeparateDatabaseAndState mit leeren database_operations: kein DROP, kein
# Daten-Umzug – nur der Django-Projektzustand ändert sich.
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_merge_20261023_2004'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='AcquisitionLead'),
                migrations.DeleteModel(name='NewCompany'),
                migrations.DeleteModel(name='RealEstateLead'),
            ],
            database_operations=[],
        ),
    ]
