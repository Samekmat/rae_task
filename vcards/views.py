from typing import Dict

import vobject
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.http import FileResponse, HttpResponse
from django.views.generic import CreateView, DetailView, View
from django.urls import reverse_lazy
from formtools.wizard.views import SessionWizardView

from .models import VCard
from .forms import VCardForm, StepOneForm, StepTwoForm, StepThreeForm, StepFourForm
import qrcode
from io import BytesIO
from django.core.files import File


class VCardCreateView(LoginRequiredMixin, CreateView):
    model = VCard
    form_class = VCardForm
    template_name = 'vcards/create_vcard.html'

    def generate_qr_code(self, data: str) -> bytes:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        return buffer.getvalue()

    def generate_vcard(self, vcard_data: Dict[str, str]) -> str:
        vcard = vobject.vCard()
        vcard.add('fn').value = vcard_data['name'] + ' ' + vcard_data['surname']
        vcard.add('org').value = vcard_data['company_name']
        vcard.add('tel').value = vcard_data['phone']
        vcard.add('email').value = vcard_data['email']
        return vcard.serialize()

    def form_valid(self, form):
        vcard_instance = form.save(commit=False)
        vcard_data = form.cleaned_data

        vcard_string = self.generate_vcard(vcard_data)

        vcard_instance.vcard_file.save(f'contact_{vcard_data['name']}_{vcard_data['surname']}_{vcard_data['company_name']}.vcf', ContentFile(vcard_string))

        qr_data = self.request.build_absolute_uri(vcard_instance.unique_url)
        qr_code_data = self.generate_qr_code(qr_data)

        vcard_instance.qr_code.save(f'{vcard_instance.unique_url}.png', File(BytesIO(qr_code_data)))

        vcard_instance.save()

        return super().form_valid(form)

    def get_success_url(self):
        vcard = self.object
        return reverse_lazy('vcards:vcard_detail', kwargs={'pk': vcard.pk})


class VCardDetailView(LoginRequiredMixin, DetailView):
    model = VCard
    template_name = 'vcards/vcard_detail.html'
    context_object_name = 'vcard'

    def get_success_url(self):
        return reverse_lazy('multi_step_form', kwargs={'unique_url': self.object.unique_url})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['multi_step_form_url'] = reverse_lazy('multi_step_form', kwargs={'unique_url': self.object.unique_url})
        return context


class MultiStepFormView(LoginRequiredMixin, SessionWizardView):
    form_list = [StepOneForm, StepTwoForm, StepThreeForm, StepFourForm]
    template_name = 'forms/multi_step_form.html'

    def done(self, form_list, **kwargs):
        #  integracja z ceremeo odnośnie wysyłki smsa po zakończeniu wielokrokowego formularza
        return HttpResponse("Wyślij sms")

    def process_step(self, form):
        api_url = 'https://url_systemu/api/v1/lead/'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Token your_token"
        }
        data = form.cleaned_data
        print(data)
        # request do api, jeśli nie otrzyma response nie puści formularza do kolejengo kroku
        # requests.post(api_url, data=data, headers=headers)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unique_url = self.kwargs.get('unique_url')
        try:
            context['vcard'] = VCard.objects.get(unique_url=unique_url)
        except VCard.DoesNotExist:
            context['vcard'] = None
        return context


class DownloadVCardFileView(LoginRequiredMixin, View):
    def get(self, request, unique_url):
        vcard = VCard.objects.get(unique_url=unique_url)
        vcard_file = vcard.vcard_file
        return FileResponse(open(vcard_file.path, 'rb'), as_attachment=True)
