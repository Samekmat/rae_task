from django.db import models


class VCard(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the name.")
    surname = models.CharField(max_length=100, help_text="Enter the surname.")
    company_name = models.CharField(max_length=100, help_text="Enter the company name.")
    phone = models.CharField(max_length=20, help_text="Enter the phone number.")
    email = models.EmailField(help_text="Enter the email address.")
    image = models.ImageField(upload_to='images/', help_text="Upload an image.")
    unique_url = models.CharField(max_length=100, unique=True, help_text="Enter a unique URL.")
    qr_code = models.ImageField(upload_to='qr_codes/', help_text="Upload a QR code image.")
    vcard_file = models.FileField(upload_to='vcard_files/', help_text="Upload a vCard file.")
