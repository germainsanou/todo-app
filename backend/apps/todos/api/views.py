from rest_framework import viewsets

from apps.todos.models import Todo

from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """Tâches de l'utilisateur connecté : chacun ne voit que les siennes."""

    serializer_class = TodoSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # génération du schéma OpenAPI
            return Todo.objects.none()
        return Todo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
