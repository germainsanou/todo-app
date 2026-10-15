from rest_framework import status
from rest_framework.test import APITestCase

from .models import Todo


class TodoApiTests(APITestCase):
    url = "/api/todos/"

    def test_liste_vide(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_creer_une_tache(self):
        response = self.client.post(self.url, {"title": "Écrire des tests"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)
        self.assertFalse(Todo.objects.get().completed)

    def test_titre_obligatoire(self):
        response = self.client.post(self.url, {"title": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cocher_une_tache(self):
        todo = Todo.objects.create(title="À faire")
        response = self.client.patch(f"{self.url}{todo.id}/", {"completed": True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertTrue(todo.completed)

    def test_supprimer_une_tache(self):
        todo = Todo.objects.create(title="À supprimer")
        response = self.client.delete(f"{self.url}{todo.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)