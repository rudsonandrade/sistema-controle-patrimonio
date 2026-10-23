from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET


def grupo_requerido(*grupos):
    def teste(usuario):
        if not usuario.is_authenticated:
            return False
        if usuario.is_superuser:
            return True
        if usuario.groups.filter(name__in=grupos).exists():
            return True
        return usuario.is_staff and not grupos

    def decorador(view_func):
        decorado = user_passes_test(
            teste,
            login_url=reverse("login"),
            redirect_field_name=None,
        )(view_func)
        return decorado

    return decorador


@require_GET
def home(request):
    return render(request, "home.html")


@require_GET
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse(
            {"status": "erro", "banco": "indisponivel"}, status=503
        )

    return JsonResponse(
        {
            "status": "ok",
            "banco": "ok",
            "aplicacao": "controle-emprestimos-il",
            "fase": "2",
        }
    )


@login_required(login_url="login")
def painel(request):
    return render(request, "painel.html")
