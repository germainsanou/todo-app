"""Développement local."""

from .base import *  # noqa: F403
from .base import INSTALLED_APPS, env

DEBUG = True

# Outils de développement : show_urls (liste des routes), shell_plus…
INSTALLED_APPS += ["django_extensions"]

SECRET_KEY = env("DJANGO_SECRET_KEY", default="dev-only-insecure-key")

# Documentation interactive de l'API d'authentification : /_allauth/openapi.html
HEADLESS_SERVE_SPECIFICATION = True

# Emails envoyés à MailDev (https://github.com/maildev/maildev) :
# `npx maildev`, puis consulter http://localhost:1080
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": env("DJANGO_EMAIL_HOST", default="localhost"),
            "port": env.int("DJANGO_EMAIL_PORT", default=1025),
            "use_tls": False,
        },
    },
}
