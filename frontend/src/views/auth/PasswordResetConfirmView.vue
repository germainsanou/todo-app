<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import { errorMessages } from "@/api/allauth";
import FormErrors from "@/components/FormErrors.vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useRouter();

const code = ref("");
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
    const response = await auth.resetPassword(code.value.trim(), password.value);
    if (auth.isAuthenticated) {
      router.push({ name: "todos" });
    } else if (response.status === 401) {
      // Mot de passe changé ; l'utilisateur doit se reconnecter
      router.push({ name: "login", query: { reset: "1" } });
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
    <h1>Nouveau mot de passe</h1>

    <template v-if="auth.pendingFlow === 'password_reset_by_code'">
      <p>Saisissez le code reçu par email et choisissez un nouveau mot de passe.</p>

      <form class="auth-form" @submit.prevent="submit">
        <label>
          Code
          <input v-model="code" autocomplete="one-time-code" autocapitalize="characters" required />
        </label>
        <label>
          Nouveau mot de passe
          <input v-model="password" type="password" autocomplete="new-password" required />
        </label>
        <label>
          Confirmer le mot de passe
          <input v-model="passwordConfirm" type="password" autocomplete="new-password" required />
        </label>
        <FormErrors :errors="errors" />
        <button type="submit" :disabled="submitting">Changer le mot de passe</button>
      </form>
    </template>

    <p v-else>
      Aucune réinitialisation en cours.
      <RouterLink :to="{ name: 'password-reset' }">Demander un code</RouterLink>
    </p>
  </main>
</template>
