# Generated by Django 5.0.4 on 2024-04-28 20:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vcards", "0004_alter_vcard_qr_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vcard",
            name="qr_code",
            field=models.ImageField(upload_to="qr_codes/"),
        ),
    ]
