from django.db import models


class VCard(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='images/')
    unique_url = models.CharField(max_length=100, unique=True)
    unique_qr_code = models.ImageField(upload_to='qr_codes/', unique=True)
    vcard_file = models.FileField(upload_to='vcard_files/')

