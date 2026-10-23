from django.test import TestCase
from django.urls import reverse


class HealthTests(TestCase):
    def test_health_retorna_ok(self):
        resposta = self.client.get(reverse("health"))

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["status"], "ok")
        self.assertEqual(resposta.json()["banco"], "ok")

    def test_home_abre(self):
        resposta = self.client.get(reverse("home"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Controle de Empréstimos")
