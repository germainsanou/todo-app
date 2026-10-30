import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ command }) => ({
  plugins: [vue()],
  base: command === "build" ? "/static/" : "/",
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    // En développement, Vite relaie vers Django les appels d'API et d'authentification :
    // le navigateur ne voit qu'une seule origine, comme en production.
    proxy: {
      "/api": "http://127.0.0.1:8000",
      "/_allauth": "http://127.0.0.1:8000",
    },
  },
}))
