from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("", include("vcards.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
