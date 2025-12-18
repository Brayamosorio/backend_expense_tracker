async function http(path, options) {
  const res = await fetch(path, options);
  const raw = await res.text(); // lee una sola vez
  let data = null;
  try {
    data = raw ? JSON.parse(raw) : null;
  } catch {
    data = null;
  }

  if (!res.ok) {
    const detail =
      (data && (data.detail ?? data.message)) || (raw || "Error");
    throw new Error(detail);
  }

  if (res.status === 204) return null;
  return data;
}

export const api = {
  listExpenses() {
    return http("/api/expenses");
  },
  createExpense(payload) {
    return http("/api/expenses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  },
  getStats() {
    return http("/api/stats");
  },
  getAlerts() {
    return http("/api/alerts");
  },
  listIncomes() {
    return http("/api/incomes");
  },
  createIncome(payload) {
    return http("/api/incomes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  },
  updateIncome(id, payload) {
    return http(`/api/incomes/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  },
  deleteIncome(id) {
    return http(`/api/incomes/${id}`, { method: "DELETE" });
  },
  setBudget(amount) {
    return http("/api/budget", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ amount }),
    });
  },
  getBudgetStatus() {
    return http("/api/budget/status");
  },
  deleteExpense(id) {
    return http(`/api/expenses/${id}`, { method: "DELETE" });
  },
  updateExpense(id, payload) {
    return http(`/api/expenses/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  },
};
