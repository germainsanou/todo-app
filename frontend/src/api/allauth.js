// API d'authentification django-allauth (mode headless, client « browser »).
// Référence : https://docs.allauth.org/en/latest/headless/openapi-specification/
// En développement, la documentation interactive est sur /_allauth/openapi.html

import { request } from "./http";

const BASE = "/_allauth/browser/v1";

export const allauth = {
  getSession: () => request(`${BASE}/auth/session`),
  logout: () => request(`${BASE}/auth/session`, { method: "DELETE" }),

  login: (email, password) =>
    request(`${BASE}/auth/login`, { method: "POST", body: { email, password } }),
  signup: (email, password) =>
    request(`${BASE}/auth/signup`, { method: "POST", body: { email, password } }),

  verifyEmail: (key) => request(`${BASE}/auth/email/verify`, { method: "POST", body: { key } }),
  resendEmailVerification: () => request(`${BASE}/auth/email/verify/resend`, { method: "POST" }),

  requestPasswordReset: (email) =>
    request(`${BASE}/auth/password/request`, { method: "POST", body: { email } }),
  resetPassword: (key, password) =>
    request(`${BASE}/auth/password/reset`, { method: "POST", body: { key, password } }),
};

/** Messages d'erreur à afficher à partir d'une réponse allauth. */
export function errorMessages(response) {
  if (response.status === 429) return ["Trop de tentatives. Réessayez dans quelques minutes."];
  const errors = response.data?.errors;
  if (errors?.length) return errors.map((error) => error.message);
  return [`Erreur inattendue (${response.status}). Réessayez plus tard.`];
}
