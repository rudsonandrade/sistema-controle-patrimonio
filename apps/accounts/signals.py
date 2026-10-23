from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Perfil


@receiver(post_migrate)
def criar_grupos_perfis(sender, **kwargs):
    if sender.label != "accounts":
        return

    grupos = [
        Perfil.ADMINISTRADOR,
        Perfil.ATENDENTE,
        Perfil.AUDITOR,
        Perfil.SOLICITANTE,
    ]
    for nome in grupos:
        Group.objects.get_or_create(name=nome)
