from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import frontend

urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentification (inscription, connexion, emails, mot de passe…) : django-allauth headless
    path("_allauth/", include("allauth.headless.urls")),
    # API métier
    path("api/v1/", include("config.api_router")),
]

if settings.DEBUG:
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
        path("api/docs/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
    ]

urlpatterns += [
    # Toutes les autres URL renvoient l'application Vue.js, dont le routeur
    # prend le relais (/login, /signup…).
    re_path(r"^(?!(?:api|admin|_allauth|static)/).*$", frontend, name="frontend"),
]
