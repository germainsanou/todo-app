import { request } from "./http";

const URL = "/api/v1/todos/";

export const todosApi = {
  list: () => request(URL),
  create: (title) => request(URL, { method: "POST", body: { title } }),
  update: (id, fields) => request(`${URL}${id}/`, { method: "PATCH", body: fields }),
  remove: (id) => request(`${URL}${id}/`, { method: "DELETE" }),
};
