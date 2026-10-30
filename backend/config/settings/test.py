"""Tests automatisés (python manage.py test)."""

from .base import *  # noqa: F403

SECRET_KEY = "test-only-insecure-key"

# Hachage rapide : les tests créent beaucoup d'utilisateurs
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Les emails envoyés sont consultables dans django.core.mail.outbox
MAILERS = {
    "default": {"BACKEND": "django.core.mail.backends.locmem.EmailBackend"},
}
