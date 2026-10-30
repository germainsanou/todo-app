<script setup>
import { useRouter } from "vue-router";

import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useRouter();

async function logout() {
  await auth.logout();
  router.push({ name: "login" });
}
</script>

<template>
  <header class="app-header">
    <RouterLink to="/" class="brand">Todo App</RouterLink>
    <div v-if="auth.isAuthenticated" class="session">
      <span>{{ auth.user.email }}</span>
      <button type="button" @click="logout">Se déconnecter</button>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
.app-header { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 12px 16px; border-bottom: 1px solid var(--border); }
.brand { font-weight: 600; color: var(--text-h); text-decoration: none; }
.session { display: flex; align-items: center; gap: 12px; }
</style>
