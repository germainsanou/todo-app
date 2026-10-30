from rest_framework import status
from rest_framework.test import APITestCase

from apps.todos.models import Todo
from apps.users.models import User


class TodoApiTests(APITestCase):
    url = "/api/v1/todos/"

    def setUp(self):
        self.user = User.objects.create_user(email="alice@exemple.com", password="motdepasse")
        self.client.force_authenticate(self.user)

    def test_authentification_obligatoire(self):
        self.client.force_authenticate(None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_liste_vide(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["results"], [])

    def test_creer_une_tache(self):
        response = self.client.post(self.url, {"title": "Écrire des tests"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        todo = Todo.objects.get()
        self.assertEqual(todo.owner, self.user)
        self.assertFalse(todo.completed)

    def test_titre_obligatoire(self):
        response = self.client.post(self.url, {"title": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cocher_une_tache(self):
        todo = Todo.objects.create(owner=self.user, title="À faire")
        response = self.client.patch(f"{self.url}{todo.id}/", {"completed": True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        todo.refresh_from_db()
        self.assertTrue(todo.completed)

    def test_supprimer_une_tache(self):
        todo = Todo.objects.create(owner=self.user, title="À supprimer")
        response = self.client.delete(f"{self.url}{todo.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)


    def test_pagination(self):
        Todo.objects.bulk_create(Todo(owner=self.user, title=f"Tâche {i}") for i in range(25))

        page1 = self.client.get(self.url).json()
        self.assertEqual(page1["count"], 25)
        self.assertEqual(len(page1["results"]), 20)
        self.assertIsNotNone(page1["next"])

        page2 = self.client.get(self.url, {"page": 2}).json()
        self.assertEqual(len(page2["results"]), 5)
        self.assertIsNone(page2["next"])

        response = self.client.get(self.url, {"page_size": 10})
        self.assertEqual(len(response.json()["results"]), 10)

    def test_page_inexistante(self):
        response = self.client.get(self.url, {"page": 99})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TodoIsolationTests(APITestCase):
    """Un utilisateur ne doit jamais voir ni modifier les tâches d'un autre."""

    def setUp(self):
        alice = User.objects.create_user(email="alice@exemple.com", password="motdepasse")
        self.bob = User.objects.create_user(email="bob@exemple.com", password="motdepasse")
        self.todo_alice = Todo.objects.create(owner=alice, title="Secret d'Alice")
        self.client.force_authenticate(self.bob)

    def test_liste_ne_contient_que_ses_taches(self):
        Todo.objects.create(owner=self.bob, title="Tâche de Bob")
        titles = [t["title"] for t in self.client.get("/api/v1/todos/").json()["results"]]
        self.assertEqual(titles, ["Tâche de Bob"])

    def test_acces_a_la_tache_d_un_autre_impossible(self):
        url = f"/api/v1/todos/{self.todo_alice.id}/"
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.patch(url, {"completed": True}, format="json").status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.client.delete(url).status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Todo.objects.filter(pk=self.todo_alice.pk).exists())

    def test_proprietaire_non_modifiable(self):
        response = self.client.post("/api/v1/todos/", {"title": "x", "owner": self.todo_alice.owner_id}, format="json")
        self.assertEqual(Todo.objects.get(pk=response.json()["id"]).owner, self.bob)
