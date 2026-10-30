import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { allauth } from "@/api/allauth";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  // Étape en attente côté allauth : "verify_email", "password_reset_by_code"…
  const pendingFlow = ref(null);
  const initialized = ref(false);

  const isAuthenticated = computed(() => user.value !== null);

  // allauth répond 200 si l'utilisateur est connecté, 401 sinon (avec la liste
  // des étapes possibles / en attente) et 410 si la session a expiré.
  function applyAuthResponse(response) {
    if (response.status === 200) {
      user.value = response.data.data.user;
      pendingFlow.value = null;
    } else if (response.status === 401 || response.status === 410) {
      user.value = null;
      pendingFlow.value = response.data?.data?.flows?.find((flow) => flow.is_pending)?.id ?? null;
    }
    return response;
  }

  async function fetchSession() {
    try {
      applyAuthResponse(await allauth.getSession());
    } finally {
      initialized.value = true;
    }
  }

  const login = async (email, password) => applyAuthResponse(await allauth.login(email, password));
  const signup = async (email, password) => applyAuthResponse(await allauth.signup(email, password));
  const verifyEmail = async (key) => applyAuthResponse(await allauth.verifyEmail(key));
  const logout = async () => applyAuthResponse(await allauth.logout());
  const requestPasswordReset = async (email) =>
    applyAuthResponse(await allauth.requestPasswordReset(email));
  const resetPassword = async (key, password) =>
    applyAuthResponse(await allauth.resetPassword(key, password));

  return {
    user,
    pendingFlow,
    initialized,
    isAuthenticated,
    fetchSession,
    login,
    signup,
    verifyEmail,
    logout,
    requestPasswordReset,
    resetPassword,
  };
});
