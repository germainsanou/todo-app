from rest_framework import generics, permissions, viewsets

from apps.users.models import User

from .serializers import UserSerializer


class MeView(generics.RetrieveUpdateAPIView):
    """Profil de l'utilisateur connecté."""

    serializer_class = UserSerializer
    http_method_names = ["get", "patch", "head", "options"]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Liste et détail des comptes, réservés aux administrateurs (is_staff) :
    l'exposer à tous les utilisateurs révélerait les emails de chacun.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
