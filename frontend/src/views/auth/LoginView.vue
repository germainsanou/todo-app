<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { errorMessages } from "@/api/allauth";
import FormErrors from "@/components/FormErrors.vue";
import { safeNext } from "@/router";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

const email = ref("");
const password = ref("");
const errors = ref([]);
const submitting = ref(false);

async function submit() {
  submitting.value = true;
  errors.value = [];
  try {
    const response = await auth.login(email.value, password.value);
    if (auth.isAuthenticated) {
      router.push(safeNext(route.query.next));
    } else if (auth.pendingFlow === "verify_email") {
      router.push({ name: "verify-email" });
    } else {
      errors.value = errorMessages(response);
    }
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <main class="auth-page">
    <h1>Connexion</h1>
    <p v-if="route.query.reset" class="notice">Mot de passe modifié. Vous pouvez vous connecter.</p>

    <form class="auth-form" @submit.prevent="submit">
      <label>
        Email
        <input v-model="email" type="email" autocomplete="email" required />
      </label>
      <label>
        Mot de passe
        <input v-model="password" type="password" autocomplete="current-password" required />
      </label>
      <FormErrors :errors="errors" />
      <button type="submit" :disabled="submitting">Se connecter</button>
    </form>

    <p class="auth-links">
      <RouterLink :to="{ name: 'password-reset' }">Mot de passe oublié ?</RouterLink>
      <RouterLink :to="{ name: 'signup' }">Créer un compte</RouterLink>
    </p>
  </main>
</template>
