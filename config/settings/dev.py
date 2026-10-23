"""Configurações de desenvolvimento local."""

from .base import *  # noqa: F403

DEBUG = env_bool("DJANGO_DEBUG", True)  # noqa: F405

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,[::1]"
    ).split(",")
    if host.strip()
]

# O runserver já serve arquivos estáticos; WhiteNoise é usado em produção.
MIDDLEWARE = [
    middleware
    for middleware in MIDDLEWARE  # noqa: F405
    if middleware != "whitenoise.middleware.WhiteNoiseMiddleware"
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
