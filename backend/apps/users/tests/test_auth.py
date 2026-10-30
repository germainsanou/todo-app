"""
Parcours d'authentification complets, tels que les vivent les clients :
- web    → /_allauth/browser/v1 (cookie de session)
- mobile → /_allauth/app/v1     (en-tête X-Session-Token)
"""

import re

from allauth.account.models import EmailAddress
from django.core import mail
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User

BROWSER = "/_allauth/browser/v1"
APP = "/_allauth/app/v1"
ME_URL = "/api/v1/users/me/"
PASSWORD = "Un-mot-de-passe-solide-42"


def last_code():
    """Code à saisir contenu dans le dernier email envoyé (ex. ABCD-EFGH)."""
    return re.search(r"\b[A-Z0-9]{4}-[A-Z0-9]{4}\b", mail.outbox[-1].body).group()


def pending_flow(response):
    return next((f["id"] for f in response.json()["data"]["flows"] if f.get("is_pending")), None)


def create_verified_user(email="alice@exemple.com"):
    user = User.objects.create_user(email=email, password=PASSWORD)
    EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
    return user


class AuthTestCase(APITestCase):
    def setUp(self):
        # allauth limite le débit (ex. un email de vérification toutes les 3 min)
        # via le cache : on repart d'un compteur vierge à chaque test.
        cache.clear()


class BrowserAuthTests(AuthTestCase):
    def test_inscription_puis_verification_email(self):
        response = self.client.post(
            f"{BROWSER}/auth/signup", {"email": "alice@exemple.com", "password": PASSWORD}, format="json"
        )
        # Compte créé, mais pas encore connecté : l'email doit être vérifié
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(pending_flow(response), "verify_email")
        self.assertEqual(self.client.get(ME_URL).status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(f"{BROWSER}/auth/email/verify", {"key": last_code()}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["meta"]["is_authenticated"])

        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["email"], "alice@exemple.com")

    def test_renvoyer_le_code_de_verification(self):
        self.client.post(
            f"{BROWSER}/auth/signup", {"email": "alice@exemple.com", "password": PASSWORD}, format="json"
        )
        premier_code = last_code()

        # Juste après l'envoi, allauth refuse : un email de vérification au plus toutes les 3 min
        response = self.client.post(f"{BROWSER}/auth/email/verify/resend")
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        cache.clear()  # simule l'écoulement des 3 minutes
        response = self.client.post(f"{BROWSER}/auth/email/verify/resend")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 2)
        self.assertNotEqual(last_code(), premier_code)

        # L'ancien code n'est plus valable, le nouveau oui
        response = self.client.post(f"{BROWSER}/auth/email/verify", {"key": premier_code}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(f"{BROWSER}/auth/email/verify", {"key": last_code()}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mot_de_passe_trop_faible_refuse(self):
        response = self.client.post(
            f"{BROWSER}/auth/signup", {"email": "alice@exemple.com", "password": "123456"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.exists())

    def test_connexion_et_deconnexion(self):
        create_verified_user()
        response = self.client.post(
            f"{BROWSER}/auth/login", {"email": "alice@exemple.com", "password": PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(ME_URL).status_code, status.HTTP_200_OK)

        self.client.delete(f"{BROWSER}/auth/session")
        self.assertEqual(self.client.get(ME_URL).status_code, status.HTTP_403_FORBIDDEN)

    def test_mauvais_mot_de_passe(self):
        create_verified_user()
        response = self.client.post(
            f"{BROWSER}/auth/login", {"email": "alice@exemple.com", "password": "faux"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_connexion_bloquee_tant_que_email_non_verifie(self):
        User.objects.create_user(email="alice@exemple.com", password=PASSWORD)
        response = self.client.post(
            f"{BROWSER}/auth/login", {"email": "alice@exemple.com", "password": PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(pending_flow(response), "verify_email")

    def test_reinitialisation_du_mot_de_passe_par_code(self):
        create_verified_user()
        response = self.client.post(f"{BROWSER}/auth/password/request", {"email": "alice@exemple.com"}, format="json")
        self.assertEqual(pending_flow(response), "password_reset_by_code")

        nouveau = "Encore-un-mot-de-passe-solide-43"
        response = self.client.post(
            f"{BROWSER}/auth/password/reset", {"key": last_code(), "password": nouveau}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # réinitialisé, pas connecté
        self.assertTrue(User.objects.get().check_password(nouveau))

    def test_csrf_exige_pour_le_navigateur(self):
        self.client = self.client_class(enforce_csrf_checks=True)
        create_verified_user()
        response = self.client.post(
            f"{BROWSER}/auth/login", {"email": "alice@exemple.com", "password": PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AppAuthTests(AuthTestCase):
    def login(self):
        response = self.client.post(
            f"{APP}/auth/login", {"email": "alice@exemple.com", "password": PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.json()["meta"]["session_token"]

    def test_jeton_de_session_pour_mobile(self):
        create_verified_user()
        token = self.login()

        # Aucun cookie : l'API n'est accessible qu'avec le jeton
        self.client.cookies.clear()
        self.assertEqual(self.client.get(ME_URL).status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(ME_URL, headers={"X-Session-Token": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["email"], "alice@exemple.com")

    def test_deconnexion_invalide_le_jeton(self):
        create_verified_user()
        token = self.login()
        self.client.cookies.clear()
        self.client.delete(f"{APP}/auth/session", headers={"X-Session-Token": token})
        response = self.client.get(ME_URL, headers={"X-Session-Token": token})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserListApiTests(APITestCase):
    url = "/api/v1/users/"

    def setUp(self):
        self.user = create_verified_user()

    def test_reserve_aux_administrateurs(self):
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.get(f"{self.url}{self.user.id}/").status_code, status.HTTP_403_FORBIDDEN)

    def test_liste_pour_un_administrateur(self):
        admin = User.objects.create_superuser(email="admin@exemple.com", password=PASSWORD)
        self.client.force_authenticate(admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([u["email"] for u in response.json()["results"]], ["admin@exemple.com", "alice@exemple.com"])

    def test_lecture_seule(self):
        admin = User.objects.create_superuser(email="admin@exemple.com", password=PASSWORD)
        self.client.force_authenticate(admin)
        response = self.client.delete(f"{self.url}{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class MeApiTests(APITestCase):
    def setUp(self):
        self.user = create_verified_user()
        self.client.force_authenticate(self.user)

    def test_modifier_son_profil(self):
        response = self.client.patch(ME_URL, {"first_name": "Alice"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Alice")

    def test_email_non_modifiable_ici(self):
        self.client.patch(ME_URL, {"email": "pirate@exemple.com"}, format="json")
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "alice@exemple.com")
