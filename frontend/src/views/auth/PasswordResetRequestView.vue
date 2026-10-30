<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import { errorMessages } from "@/api/allauth";
import FormErrors from "@/components/FormErrors.vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useRouter();

const email = ref("");
const errors = ref([]);
const submitting = ref(false);

async function submit() {
  submitting.value = true;
  errors.value = [];
  try {
    const response = await auth.requestPasswordReset(email.value);
    // Par sécurité, la réponse est la même que le compte existe ou non
    if (auth.pendingFlow === "password_reset_by_code") {
      router.push({ name: "password-reset-confirm" });
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
    <h1>Mot de passe oublié</h1>
    <p>Indiquez votre email : si un compte existe, vous recevrez un code de réinitialisation.</p>

    <form class="auth-form" @submit.prevent="submit">
      <label>
        Email
        <input v-model="email" type="email" autocomplete="email" required />
      </label>
      <FormErrors :errors="errors" />
      <button type="submit" :disabled="submitting">Envoyer le code</button>
    </form>

    <p class="auth-links">
      <RouterLink :to="{ name: 'login' }">Retour à la connexion</RouterLink>
    </p>
  </main>
</template>
