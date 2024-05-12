from django import forms
from django.core.validators import RegexValidator

from .models import VCard


class VCardForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Twoje imię i nazwisko'}))

    class Meta:
        model = VCard
        fields = ['full_name', 'company_name', 'phone', 'email', 'image', 'unique_url']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Nazwa firmy'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Numer telefonu'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Adres email'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*', 'title': 'Zdjęcie (najlepiej kwadrat)'}),
            'unique_url': forms.TextInput(attrs={'placeholder': 'Adres vcard'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get('full_name')
        if full_name:
            name_parts = full_name.split(' ', 1)
            cleaned_data['name'] = name_parts[0]
            cleaned_data['surname'] = name_parts[1] if len(name_parts) > 1 else ''
        return cleaned_data


class StepOneForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Wpisz swój numer telefonu..'}), initial="+48", validators=[RegexValidator(r'^\+48\d{9}$',
                            message="Wpisz poprawny polski numer zaczynający się od +48.")])


class StepTwoForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Twoje imię i nazwisko'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Adres email'}))
    company = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Firma / miejsce kontaktu'}))

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get('full_name')
        if full_name:
            name_parts = full_name.split(' ', 1)
            cleaned_data['name'] = name_parts[0]
            cleaned_data['surname'] = name_parts[1] if len(name_parts) > 1 else ''
        return cleaned_data


class StepThreeForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Data'}))
    topic = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Temat'}))


class StepFourForm(forms.Form):
    CHOICES = (
        ('OK', 'OK'),
        ('NIE_OK', 'Nie OK')
    )
    decision = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)


