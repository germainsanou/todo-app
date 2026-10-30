"""Routes de l'API REST, montées sous /api/v1/."""

from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.todos.api.views import TodoViewSet
from apps.users.api.views import MeView, UserViewSet

app_name = "api"

router = DefaultRouter()
router.register("todos", TodoViewSet, basename="todo")
router.register("users", UserViewSet)

urlpatterns = [
    # Avant le routeur, sinon « me » serait pris pour l'identifiant d'un utilisateur
    path("users/me/", MeView.as_view(), name="users-me"),
    *router.urls,
]
