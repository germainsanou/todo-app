# Frontend Vue.js + Vite

Interface de l'application, écrite en [Vue 3](https://vuejs.org/) (Composition API, composants monofichiers `.vue` avec `<script setup>`) et compilée par [Vite](https://vite.dev/).

## Commandes

```bash
npm install       # installer les dépendances
npm run dev       # serveur de dev sur http://localhost:5173 (les appels /api sont redirigés vers Django sur :8000)
npm run lint      # analyse du code avec Oxlint (plugin vue activé)
npm run build     # build de production dans dist/, servi ensuite par Django sous /static/
```

## Organisation

- `index.html` : page d'entrée, contient `<div id="app">`
- `src/main.js` : crée l'application Vue (avec Pinia et Vue Router) et la monte sur `#app`
- `src/App.vue` : composant racine (en-tête + `<RouterView>`)
- `src/api/` : appels HTTP. `http.js` gère le cookie de session et l'en-tête CSRF ; `allauth.js` couvre l'authentification
- `src/stores/` : état partagé avec [Pinia](https://pinia.vuejs.org/), par exemple `auth.js` pour l'utilisateur connecté
- `src/router/` : routes [Vue Router](https://router.vuejs.org/). `meta.requiresAuth` réserve une page aux utilisateurs connectés
- `src/views/` : une vue par page ; `views/auth/` contient connexion, inscription, vérification d'email et mot de passe oublié
- `src/components/` : composants réutilisables
- `vite.config.js` : plugin Vue, alias `@` → `src/`, `base: "/static/"` au build, proxy `/api` et `/_allauth` vers Django en dev

Django renvoie `index.html` pour toutes les URL qui ne commencent pas par
`/api/`, `/admin/`, `/_allauth/` ou `/static/`. Le routeur Vue prend ensuite le relais.

## Outillage conseillé

VS Code avec l'extension officielle [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar).
