import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ command }) => ({
  plugins: [vue()],
  base: command === "build" ? "/static/" : "/",
  server: {
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
}))
