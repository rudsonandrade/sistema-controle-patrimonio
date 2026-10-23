from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    ordering = ("nome_completo", "matricula")
    list_display = ("matricula", "nome_completo", "email", "perfil", "is_active", "is_staff")
    list_filter = ("perfil", "is_active", "is_staff", "is_superuser")
    search_fields = ("matricula", "nome_completo", "email")

    fieldsets = (
        (None, {"fields": ("matricula", "password")}),
        (_("Dados pessoais"), {"fields": ("nome_completo", "email")}),
        (
            _("Permissões"),
            {
                "fields": (
                    "perfil",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Datas importantes"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("matricula", "nome_completo", "email", "perfil", "password1", "password2"),
            },
        ),
    )
