from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import Perfil, User


class Command(BaseCommand):
    help = "Configura grupos de perfis e aplica permissões iniciais."

    def handle(self, *args, **options):
        with transaction.atomic():
            for perfil in Perfil.values:
                grupo, _ = Group.objects.get_or_create(name=perfil)

            for usuario in User.objects.all():
                if usuario.is_superuser and usuario.perfil != Perfil.ADMINISTRADOR:
                    usuario.perfil = Perfil.ADMINISTRADOR
                    usuario.save(update_fields=["perfil"])
                if usuario.perfil and usuario.perfil != Perfil.SOLICITANTE:
                    grupo = Group.objects.get(name=usuario.perfil)
                    usuario.groups.add(grupo)
                elif usuario.perfil == Perfil.SOLICITANTE:
                    grupo, _ = Group.objects.get_or_create(name=Perfil.SOLICITANTE)
                    usuario.groups.add(grupo)

        self.stdout.write(self.style.SUCCESS("Grupos e perfis configurados."))
