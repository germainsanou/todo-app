<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import { errorMessages } from "@/api/allauth";
import FormErrors from "@/components/FormErrors.vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useRouter();

const email = ref("");
const password = ref("");
const passwordConfirm = ref("");
const errors = ref([]);
const submitting = ref(false);

async function submit() {
  errors.value = [];
  if (password.value !== passwordConfirm.value) {
    errors.value = ["Les deux mots de passe ne correspondent pas."];
    return;
  }
  submitting.value = true;
  try {
    const response = await auth.signup(email.value, password.value);
    if (auth.isAuthenticated) {
      router.push({ name: "todos" });
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
    <h1>Créer un compte</h1>

    <form class="auth-form" @submit.prevent="submit">
      <label>
        Email
        <input v-model="email" type="email" autocomplete="email" required />
      </label>
      <label>
        Mot de passe
        <input v-model="password" type="password" autocomplete="new-password" required />
      </label>
      <label>
        Confirmer le mot de passe
        <input v-model="passwordConfirm" type="password" autocomplete="new-password" required />
      </label>
      <FormErrors :errors="errors" />
      <button type="submit" :disabled="submitting">Créer mon compte</button>
    </form>

    <p class="auth-links">
      <RouterLink :to="{ name: 'login' }">J'ai déjà un compte</RouterLink>
    </p>
  </main>
</template>
