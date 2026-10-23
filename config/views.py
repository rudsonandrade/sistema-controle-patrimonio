from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


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
            "fase": "1",
        }
    )
