import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "/api/todos/";

function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState(null);

  async function loadTodos() {
    try {
      const response = await fetch(API_URL);
      if (!response.ok) throw new Error(`Erreur ${response.status}`);
      setTodos(await response.json());
      setError(null);
    } catch {
      setError("Impossible de charger les tâches. Le backend est-il lancé ?");
    }
  }

  useEffect(() => {
    loadTodos();
  }, []);

  async function addTodo(event) {
    event.preventDefault();
    if (!title.trim()) return;
    await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    setTitle("");
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

  return (
    <main className="app">
      <h1>Mes tâches ✅</h1>

      <form onSubmit={addTodo} className="add-form">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Nouvelle tâche…"
        />
        <button type="submit">Ajouter</button>
      </form>

      {error && <p className="error">{error}</p>}

      <ul className="todo-list">
        {todos.map((todo) => (
          <li key={todo.id} className={todo.completed ? "done" : ""}>
            <label>
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleTodo(todo)}
              />
              {todo.title}
            </label>
            <button onClick={() => deleteTodo(todo.id)}>Supprimer</button>
          </li>
        ))}
      </ul>

      {todos.length === 0 && !error && <p>Aucune tâche pour l'instant.</p>}
    </main>
  );
}

export default App;