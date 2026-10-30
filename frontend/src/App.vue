<script setup>
import { onMounted, ref } from "vue";

const API_URL = "/api/todos/";

const todos = ref([]);
const title = ref("");
const error = ref(null);

async function loadTodos() {
  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error(`Erreur ${response.status}`);
    todos.value = await response.json();
    error.value = null;
  } catch {
    error.value = "Impossible de charger les tâches. Le backend est-il lancé ?";
  }
}

onMounted(loadTodos);

async function addTodo() {
  if (!title.value.trim()) return;
  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: title.value }),
  });
  title.value = "";
  loadTodos();
}

async function toggleTodo(todo) {
  await fetch(`${API_URL}${todo.id}/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed: !todo.completed }),
  });
  loadTodos();
}

async function deleteTodo(id) {
  await fetch(`${API_URL}${id}/`, { method: "DELETE" });
  loadTodos();
}
</script>

<template>
  <main class="app">
    <h1>Mes tâches ✅VUE</h1>

    <form class="add-form" @submit.prevent="addTodo">
      <input v-model="title" placeholder="Nouvelle tâche…" />
      <button type="submit">Ajouter</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>

    <ul class="todo-list">
      <li v-for="todo in todos" :key="todo.id" :class="{ done: todo.completed }">
        <label>
          <input
            type="checkbox"
            :checked="todo.completed"
            @change="toggleTodo(todo)"
          />
          {{ todo.title }}
        </label>
        <button @click="deleteTodo(todo.id)">Supprimer</button>
      </li>
    </ul>

    <p v-if="todos.length === 0 && !error">Aucune tâche pour l'instant.</p>
  </main>
</template>

<style scoped>
.app { max-width: 480px; margin: 40px auto; padding: 0 16px; text-align: left; }
.add-form { display: flex; gap: 8px; margin-bottom: 16px; }
.add-form input { flex: 1; padding: 8px; }
.todo-list { list-style: none; padding: 0; }
.todo-list li { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #444; }
.todo-list li.done label { text-decoration: line-through; opacity: 0.6; }
.error { color: #e55; }
</style>
