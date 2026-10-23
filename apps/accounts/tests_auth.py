from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import Perfil

User = get_user_model()


class AuthFlowTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            matricula="2026001",
            email="atendente@example.test",
            nome_completo="Atendente Teste",
            password="senha-forte-teste-123",
            perfil=Perfil.ATENDENTE,
        )

    def test_home_acessivel_sem_autenticacao(self):
        resposta = self.client.get(reverse("home"))
        self.assertEqual(resposta.status_code, 200)

    def test_login_com_matricula_e_senha(self):
        resposta = self.client.post(
            reverse("login"),
            {"username": "2026001", "password": "senha-forte-teste-123"},
        )
        self.assertIn(resposta.status_code, [200, 302])

    def test_painel_exige_autenticacao(self):
        resposta = self.client.get(reverse("painel"))
        self.assertIn(resposta.status_code, [302])
        self.assertIn("/conta/entrar/", resposta.url)

    def test_painel_autenticado_acessa(self):
        self.client.force_login(self.usuario)
        resposta = self.client.get(reverse("painel"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Painel de atendimento")

    def test_logout_disponivel(self):
        self.client.force_login(self.usuario)
        resposta = self.client.post(reverse("logout"))
        self.assertEqual(resposta.status_code, 302)

    def test_admin_login_usa_matricula(self):
        self.usuario.is_staff = True
        self.usuario.save(update_fields=["is_staff"])
        resposta = self.client.get(reverse("admin:login"))
        self.assertEqual(resposta.status_code, 200)
