from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("painel/", views.painel, name="painel"),
    path(
        "conta/entrar/",
        auth_views.LoginView.as_view(template_name="registration/login.html", next_page="/painel/"),
        name="login",
    ),
    path("conta/sair/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("conta/negado/", views.home, name="acesso_negado"),
    path("health/", views.health, name="health"),
    path("admin/", admin.site.urls),
]
