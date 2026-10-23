from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class Perfil(models.TextChoices):
    ADMINISTRADOR = "administrador", "Administrador do sistema"
    ATENDENTE = "atendente", "Servidor responsável pelo atendimento"
    AUDITOR = "auditor", "Gestor ou auditor autorizado"
    SOLICITANTE = "solicitante", "Solicitante"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, matricula, email, nome_completo, password=None, **extra_fields):
        if not matricula:
            raise ValueError("A matrícula é obrigatória.")
        if not nome_completo:
            raise ValueError("O nome completo é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(
            matricula=matricula.strip(),
            email=email,
            nome_completo=nome_completo.strip(),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, email, nome_completo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("perfil", Perfil.ADMINISTRADOR)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário precisa de is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário precisa de is_superuser=True.")

        return self.create_user(matricula, email, nome_completo, password, **extra_fields)


class User(AbstractUser):
    """Usuário do sistema, identificado pela matrícula institucional."""

    username = None
    matricula = models.CharField("matrícula", max_length=20, unique=True)
    nome_completo = models.CharField("nome completo", max_length=150)
    email = models.EmailField("e-mail", unique=True)
    perfil = models.CharField(
        "perfil",
        max_length=20,
        choices=Perfil.choices,
        default=Perfil.SOLICITANTE,
        db_index=True,
    )

    USERNAME_FIELD = "matricula"
    REQUIRED_FIELDS = ["email", "nome_completo"]

    objects = UserManager()

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"
        ordering = ("nome_completo", "matricula")

    def __str__(self):
        return f"{self.nome_completo} ({self.matricula})"

    @property
    def nome_exibicao(self):
        return self.nome_completo or self.matricula

    def save(self, *args, **kwargs):
        if self.email:
            self.email = type(self).objects.normalize_email(self.email)
        super().save(*args, **kwargs)
