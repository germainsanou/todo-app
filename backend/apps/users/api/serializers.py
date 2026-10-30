from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "date_joined"]
        # L'email se modifie via allauth (/_allauth/.../account/email) pour être revérifié
        read_only_fields = ["id", "email", "date_joined"]
