"""Production (image Docker)."""

from .base import *  # noqa: F403
from .base import env

SECRET_KEY = env("DJANGO_SECRET_KEY")


# ---------- Sécurité ----------
# https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# Nginx indique dans l'en-tête X-Forwarded-Proto si la requête d'origine était en HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Redirection HTTP → HTTPS : généralement faite par Nginx (certbot), sinon activer ici
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=False)

# Cookies envoyés uniquement en HTTPS (à désactiver pour tester l'image en HTTP local)
SESSION_COOKIE_SECURE = env.bool("DJANGO_SECURE_COOKIES", default=True)
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE

# HSTS : à activer (ex. 31536000) une fois le HTTPS confirmé sur le domaine
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=False)
SECURE_CONTENT_TYPE_NOSNIFF = True


# ---------- Cache ----------
# Partagé entre les workers Gunicorn : indispensable pour que la limitation de
# débit d'allauth (tentatives de connexion, envoi de codes…) soit fiable.
# La table est créée au démarrage par `manage.py createcachetable`.

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    },
}


# ---------- Emails ----------

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "OPTIONS": {
            "host": env("DJANGO_EMAIL_HOST"),
            "port": env.int("DJANGO_EMAIL_PORT", default=587),
            "username": env("DJANGO_EMAIL_HOST_USER", default=""),
            "password": env("DJANGO_EMAIL_HOST_PASSWORD", default=""),
            "use_tls": env.bool("DJANGO_EMAIL_USE_TLS", default=True),
        },
    },
}


# ---------- Logs ----------
# Erreurs envoyées sur la sortie standard (visibles avec `docker compose logs`)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
