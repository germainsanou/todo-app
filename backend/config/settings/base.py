"""
Réglages communs à tous les environnements.

Chaque environnement a son propre module qui importe celui-ci :
- config.settings.local       → développement (par défaut avec manage.py)
- config.settings.test        → tests automatisés
- config.settings.production  → serveur (par défaut avec wsgi.py / asgi.py)

Toute valeur qui change d'un déploiement à l'autre se lit dans les variables
d'environnement (voir .env.example à la racine du dépôt).
"""

from pathlib import Path

import environ

# backend/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()


# ---------- Général ----------
# https://docs.djangoproject.com/en/6.1/ref/settings/

DEBUG = False

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------- Applications ----------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "allauth",
    "allauth.account",
    "allauth.headless",
]

LOCAL_APPS = [
    "apps.users",
    "apps.todos",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ---------- Base de données ----------
# DATABASE_URL, ex. postgres://user:motdepasse@hote:5432/nom

DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DJANGO_CONN_MAX_AGE", default=600)


# ---------- Authentification ----------
# Modèle utilisateur personnalisé, défini dès le départ comme le recommande
# la documentation Django (impossible à changer proprement plus tard).

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------- django-allauth (mode headless) ----------
# https://docs.allauth.org/en/latest/headless/
# Les clients appellent l'API sous /_allauth/ :
# - /_allauth/browser/v1/... : frontend web, authentifié par cookie de session + CSRF
# - /_allauth/app/v1/...     : application mobile, authentifiée par l'en-tête X-Session-Token

HEADLESS_ONLY = True
HEADLESS_CLIENTS = ("browser", "app")

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*"]
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# Codes à saisir plutôt que liens cliquables : même parcours sur le web et sur
# mobile, sans avoir à gérer de liens profonds (deep links) dans l'app.
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED = True
# Bouton « Renvoyer le code » : 2 renvois maximum (désactivé par défaut dans allauth)
ACCOUNT_EMAIL_VERIFICATION_SUPPORTS_RESEND = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="")
# La limitation de débit (ACCOUNT_RATE_LIMITS) et la protection contre
# l'énumération des comptes sont actives par défaut.


# ---------- Django REST Framework ----------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # Frontend web : cookie de session (avec vérification CSRF)
        "rest_framework.authentication.SessionAuthentication",
        # Application mobile : jeton de session allauth
        "allauth.headless.contrib.rest_framework.authentication.XSessionTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "config.pagination.StandardPagination",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": "/api/v[0-9]+",
    "SERVE_INCLUDE_SCHEMA": False,
}


# ---------- Emails ----------
# https://docs.djangoproject.com/en/6.1/topics/email/

DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL", default="webmaster@localhost")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}


# ---------- Fichiers statiques ----------
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Build du frontend (npm run build), servi par Django sous /static/
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"
STATICFILES_DIRS = [FRONTEND_DIST]

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
