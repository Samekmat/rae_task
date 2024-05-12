from django.contrib.auth.views import LoginView
from django.urls import path

from .views import RegisterView, logout_view

app_name = "users"

urlpatterns = [
    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
