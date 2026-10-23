from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Perfil

User = get_user_model()


class UserModelTests(TestCase):
    def test_cria_usuario_com_senha_criptografada(self):
        user = User.objects.create_user(
            matricula="123456",
            email="servidor@example.test",
            nome_completo="Servidor de Teste",
            password="senha-forte-de-teste-123",
        )

        self.assertEqual(user.perfil, Perfil.SOLICITANTE)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertNotEqual(user.password, "senha-forte-de-teste-123")
        self.assertTrue(user.check_password("senha-forte-de-teste-123"))
        self.assertEqual(str(user), "Servidor de Teste (123456)")

    def test_autentica_pela_matricula(self):
        User.objects.create_user(
            matricula="654321",
            email="atendente@example.test",
            nome_completo="Atendente de Teste",
            password="outra-senha-forte-456",
            perfil=Perfil.ATENDENTE,
        )

        usuario = authenticate(
            matricula="654321", password="outra-senha-forte-456"
        )

        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.perfil, Perfil.ATENDENTE)

    def test_matricula_unica(self):
        User.objects.create_user(
            matricula="111111",
            email="a@example.test",
            nome_completo="Usuário A",
            password="senha-forte-de-teste-123",
        )

        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                matricula="111111",
                email="b@example.test",
                nome_completo="Usuário B",
                password="senha-forte-de-teste-123",
            )

    def test_superusuario_recebe_perfil_administrador(self):
        admin = User.objects.create_superuser(
            matricula="000001",
            email="admin@example.test",
            nome_completo="Administrador de Teste",
            password="senha-forte-de-teste-123",
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.perfil, Perfil.ADMINISTRADOR)

    def test_matricula_obrigatoria(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                matricula="",
                email="semmatricula@example.test",
                nome_completo="Sem Matrícula",
                password="senha-forte-de-teste-123",
            )


class AdminUserTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            matricula="000002",
            email="admin2@example.test",
            nome_completo="Administrador Dois",
            password="senha-forte-de-teste-123",
        )

    def test_pagina_de_inclusao_de_usuario_abre(self):
        self.client.force_login(self.admin)
        resposta = self.client.get(reverse("admin:accounts_user_add"))
        self.assertEqual(resposta.status_code, 200)

    def test_pagina_de_alteracao_de_usuario_abre(self):
        self.client.force_login(self.admin)
        resposta = self.client.get(
            reverse("admin:accounts_user_change", args=[self.admin.pk])
        )
        self.assertEqual(resposta.status_code, 200)
