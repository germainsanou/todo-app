// Client HTTP commun à tous les appels vers Django.
//
// Le frontend est servi par le même domaine que l'API : l'authentification
// repose sur le cookie de session (HttpOnly) posé par Django. Aucun jeton
// n'est stocké côté navigateur. Pour les requêtes qui modifient des données,
// Django exige en plus le jeton CSRF, lu dans le cookie « csrftoken ».

const SAFE_METHODS = ["GET", "HEAD", "OPTIONS"];

function getCookie(name) {
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

/**
 * Envoie une requête JSON et renvoie { status, ok, data } sans lever
 * d'exception sur les codes 4xx : c'est à l'appelant de les interpréter
 * (allauth répond par exemple 401 pour « pas encore connecté »).
 */
export async function request(url, { method = "GET", body } = {}) {
  const headers = { Accept: "application/json" };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (!SAFE_METHODS.includes(method)) headers["X-CSRFToken"] = getCookie("csrftoken") ?? "";

  const response = await fetch(url, {
    method,
    headers,
    credentials: "same-origin",
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const data = response.status === 204 ? null : await response.json().catch(() => null);
  return { status: response.status, ok: response.ok, data };
}
