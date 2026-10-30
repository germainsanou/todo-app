from drf_spectacular.extensions import OpenApiAuthenticationExtension


class XSessionTokenScheme(OpenApiAuthenticationExtension):
    """Jeton obtenu via /_allauth/app/v1/auth/login, utilisé par l'application mobile."""

    target_class = "allauth.headless.contrib.rest_framework.authentication.XSessionTokenAuthentication"
    name = "sessionToken"

    def get_security_definition(self, auto_schema):
        return {"type": "apiKey", "in": "header", "name": "X-Session-Token"}
