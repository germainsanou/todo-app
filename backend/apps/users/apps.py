from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "apps.users"
    verbose_name = "Utilisateurs"

    def ready(self):
        # Documente l'authentification par X-Session-Token dans le schéma OpenAPI
        from . import schema  # noqa: F401
