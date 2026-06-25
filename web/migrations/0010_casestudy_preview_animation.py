from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0009_contactmessage_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="casestudy",
            name="preview_animation",
            field=models.FileField(blank=True, null=True, upload_to="cases/previews/"),
        ),
    ]
