<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import { allauth, errorMessages } from "@/api/allauth";
import FormErrors from "@/components/FormErrors.vue";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
const router = useRouter();

const code = ref("");
const errors = ref([]);
const notice = ref("");
const submitting = ref(false);

async function submit() {
  submitting.value = true;
  errors.value = [];
  try {
    const response = await auth.verifyEmail(code.value.trim());
    if (auth.isAuthenticated) {
      router.push({ name: "todos" });
    } else if (response.status === 401) {
      // Email vérifié, mais connexion non automatique
      router.push({ name: "login" });
    } else {
      errors.value = errorMessages(response);
    }
  } finally {
    submitting.value = false;
  }
}

async function resend() {
  errors.value = [];
  notice.value = "";
  const response = await allauth.resendEmailVerification();
  if (response.ok) {
    notice.value = "Un nouveau code vient de vous être envoyé.";
  } else if (response.status === 429) {
    errors.value = ["Un code vient d'être envoyé. Patientez quelques minutes avant d'en demander un autre."];
  } else if (response.status === 409) {
    // Nombre maximal de renvois atteint : se reconnecter déclenche l'envoi d'un nouveau code
    errors.value = ["Nombre maximal de renvois atteint. Reconnectez-vous pour recevoir un nouveau code."];
  } else {
    errors.value = errorMessages(response);
  }
}
</script>

<template>
  <main class="auth-page">
    <h1>Vérifiez votre email</h1>

    <template v-if="auth.pendingFlow === 'verify_email'">
      <p>Saisissez le code que nous venons de vous envoyer par email.</p>
      <p v-if="notice" class="notice">{{ notice }}</p>

      <form class="auth-form" @submit.prevent="submit">
        <label>
          Code
          <input v-model="code" autocomplete="one-time-code" autocapitalize="characters" required />
        </label>
        <FormErrors :errors="errors" />
        <button type="submit" :disabled="submitting">Valider</button>
      </form>

      <p class="auth-links">
        <button type="button" class="link" @click="resend">Renvoyer le code</button>
      </p>
    </template>

    <p v-else>
      Aucune vérification en cours.
      <RouterLink :to="{ name: 'login' }">Se connecter</RouterLink>
    </p>
  </main>
</template>
