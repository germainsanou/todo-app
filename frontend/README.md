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
- `src/main.js` : crée l'application Vue et la monte sur `#app`
- `src/App.vue` : composant racine
- `vite.config.js` : plugin Vue, `base: "/static/"` au build, proxy `/api` en dev

## Outillage conseillé

VS Code avec l'extension officielle [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar).
