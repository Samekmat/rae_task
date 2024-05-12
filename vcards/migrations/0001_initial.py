# Generated by Django 5.0.4 on 2024-04-28 17:28

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("surname", models.CharField(max_length=100)),
                ("company_name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=254)),
                ("image", models.ImageField(upload_to="images/")),
                ("unique_url", models.CharField(max_length=100, unique=True)),
                (
                    "unique_qr_code",
                    models.ImageField(unique=True, upload_to="qr_codes/"),
                ),
                (
                    "unique_vcard_file",
                    models.FileField(unique=True, upload_to="vcard_files/"),
                ),
            ],
        ),
    ]
