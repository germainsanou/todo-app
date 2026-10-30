from django.test import TestCase

from apps.users.models import User


class UserManagerTests(TestCase):
    def test_creer_un_utilisateur(self):
        user = User.objects.create_user(email="Alice@EXEMPLE.com", password="motdepasse")
        self.assertEqual(user.email, "Alice@exemple.com")  # domaine normalisé
        self.assertTrue(user.check_password("motdepasse"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(hasattr(user, "username") and user.username)

    def test_email_obligatoire(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="motdepasse")

    def test_creer_un_superutilisateur(self):
        admin = User.objects.create_superuser(email="admin@exemple.com", password="motdepasse")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
