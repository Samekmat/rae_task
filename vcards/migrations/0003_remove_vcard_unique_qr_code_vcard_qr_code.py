# Generated by Django 5.0.4 on 2024-04-28 19:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vcards", "0002_remove_vcard_unique_vcard_file"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vcard",
            name="unique_qr_code",
        ),
        migrations.AddField(
            model_name="vcard",
            name="qr_code",
            field=models.ImageField(default=None, upload_to="qr_codes/"),
            preserve_default=False,
        ),
    ]
