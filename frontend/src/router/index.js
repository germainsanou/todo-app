import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "@/stores/auth";
import TodosView from "@/views/TodosView.vue";

// meta.requiresAuth : page réservée aux utilisateurs connectés
// meta.guestOnly    : page réservée aux visiteurs (connexion, inscription…)
const routes = [
  { path: "/", name: "todos", component: TodosView, meta: { requiresAuth: true } },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/auth/LoginView.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/signup",
    name: "signup",
    component: () => import("@/views/auth/SignupView.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/verify-email",
    name: "verify-email",
    component: () => import("@/views/auth/VerifyEmailView.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/password/reset",
    name: "password-reset",
    component: () => import("@/views/auth/PasswordResetRequestView.vue"),
    meta: { guestOnly: true },
  },
  {
    path: "/password/reset/confirm",
    name: "password-reset-confirm",
    component: () => import("@/views/auth/PasswordResetConfirmView.vue"),
    meta: { guestOnly: true },
  },
  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  // Les pages vivent à la racine du site (seuls les fichiers du build sont sous /static/)
  history: createWebHistory("/"),
  routes,
});

router.beforeEach(async (to) => {
  const auth = useAuthStore();
  if (!auth.initialized) await auth.fetchSession();

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "login", query: { next: to.fullPath } };
  }
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: "todos" };
  }
});

/** Destination après connexion : uniquement un chemin interne (pas de redirection ouverte). */
export function safeNext(next) {
  return typeof next === "string" && next.startsWith("/") && !next.startsWith("//") ? next : "/";
}

export default router;
