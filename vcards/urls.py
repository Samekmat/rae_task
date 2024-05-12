from django.urls import path
from .views import VCardCreateView, VCardDetailView, MultiStepFormView, DownloadVCardFileView

app_name = "vcards"

urlpatterns = [
    path('create/', VCardCreateView.as_view(), name='create_vcard'),
    path('detail/<int:pk>/', VCardDetailView.as_view(), name='vcard_detail'),
    path('<str:unique_url>/', MultiStepFormView.as_view(), name='multi_step_form'),
    path('download-vcard/<str:unique_url>/', DownloadVCardFileView.as_view(), name='download_vcard'),
]
