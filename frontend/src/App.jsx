import { useEffect, useMemo, useState } from "react";
import { api } from "./api";
import Operaciones from "./modules/Operaciones";
import Ingresos from "./modules/Ingresos";

const items = ["Operaciones", "Ingresos"];

function Sidebar({ active, onChange }) {
  return (
    <aside className="w-full md:w-[260px] md:h-screen border-b md:border-b-0 md:border-r border-white/10 bg-black/20 backdrop-blur-xl p-6">
      <div className="kicker">MODULOS</div>
      <h2 className="mt-2 text-lg font-semibold text-slate-100">Panel</h2>

      <div className="mt-6 space-y-2">
        {items.map((it) => (
          <button
            key={it}
            onClick={() => onChange(it)}
            className={[
              "w-full rounded-2xl border border-white/10 px-4 py-3 text-left text-slate-100 transition",
              "bg-white/[.02] hover:bg-white/[.06]",
              active === it ? "outline outline-2 outline-sky-400/30" : "",
            ].join(" ")}
          >
            {it}
          </button>
        ))}
      </div>
    </aside>
  );
}

function Header() {
  return (
    <div className="card p-8">
      <div className="kicker">EXPENSE TRACKER</div>
      <h1 className="mt-2 text-4xl font-bold text-slate-100">hola mundo</h1>
      <p className="mt-2 text-slate-300">
        Agrega, revisa y edita tus gastos sin instalar nada.
      </p>

      <div className="mt-5 flex flex-wrap gap-3">
        <button className="btn">API /api/expenses</button>
        <button className="btn">FastAPI + React</button>
      </div>
    </div>
  );
}

function money(n) {
  const v = Number(n ?? 0);
  return v.toLocaleString("es-CO", { style: "currency", currency: "COP" });
}

export default function App() {
  const [active, setActive] = useState("Operaciones");

  // data
  const [expenses, setExpenses] = useState([]);
  const [filteredExpenses, setFilteredExpenses] = useState([]);
  const [stats, setStats] = useState(null);
  const [incomes, setIncomes] = useState([]);
  const [filteredIncomes, setFilteredIncomes] = useState([]);

  // ui state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // form
  const today = useMemo(() => new Date().toISOString().slice(0, 10), []);
  const [form, setForm] = useState({
    date: today,
    category: "Comida",
    amount: 0,
    description: "",
  });
  const [editingId, setEditingId] = useState(null);

  const [incomeForm, setIncomeForm] = useState({
    date: today,
    category: "Ingreso",
    amount: 0,
    description: "",
  });
  const [editingIncomeId, setEditingIncomeId] = useState(null);

  // filters gastos
  const [filterDate, setFilterDate] = useState("");
  const [filterMonth, setFilterMonth] = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const [filterMessage, setFilterMessage] = useState("");

  // filters ingresos
  const [incomeFilterDate, setIncomeFilterDate] = useState("");
  const [incomeFilterMonth, setIncomeFilterMonth] = useState("");
  const [incomeFilterCategory, setIncomeFilterCategory] = useState("");
  const [incomeFilterMessage, setIncomeFilterMessage] = useState("");

  async function loadAll() {
    setError("");
    setLoading(true);
    try {
      const [list, st] = await Promise.all([api.listExpenses(), api.getStats()]);
      setExpenses(list || []);
      setFilteredExpenses(list || []);
      setStats(st?.stats ?? null);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadIncomes() {
    try {
      const data = await api.listIncomes();
      setIncomes(data || []);
      setFilteredIncomes(data || []);
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    loadAll();
    loadIncomes();
  }, []);

  // --- CRUD gastos ---
  async function onSave(e) {
    e.preventDefault();
    setError("");
    try {
      const payload = {
        date: form.date,
        category: form.category.trim(),
        amount: Number(form.amount),
        description: form.description.trim() || null,
      };
      if (editingId) {
        await api.updateExpense(editingId, payload);
      } else {
        await api.createExpense(payload);
      }
      setForm({ date: today, category: "Comida", amount: 0, description: "" });
      setEditingId(null);
      await loadAll();
      setFilterMessage("");
    } catch (e2) {
      setError(e2.message);
    }
  }

  async function onDelete(id) {
    setError("");
    try {
      await api.deleteExpense(id);
      await loadAll();
    } catch (e) {
      setError(e.message);
    }
  }

  function onEdit(exp) {
    setEditingId(exp.id);
    setForm({
      date: exp.date || today,
      category: exp.category || "",
      amount: exp.amount ?? 0,
      description: exp.description || "",
    });
  }

  function onCancelEdit() {
    setEditingId(null);
    setForm({ date: today, category: "Comida", amount: 0, description: "" });
  }

  // --- CRUD ingresos ---
  async function onSaveIncome(e) {
    e.preventDefault();
    setError("");
    try {
      const payload = {
        date: incomeForm.date,
        category: incomeForm.category.trim(),
        amount: Number(incomeForm.amount),
        description: incomeForm.description.trim() || null,
      };
      if (editingIncomeId) {
        await api.updateIncome(editingIncomeId, payload);
      } else {
        await api.createIncome(payload);
      }
      setIncomeForm({ date: today, category: "Ingreso", amount: 0, description: "" });
      setEditingIncomeId(null);
      await loadIncomes();
      setIncomeFilterMessage("");
    } catch (err) {
      setError(err.message);
    }
  }

  async function onDeleteIncome(id) {
    setError("");
    try {
      await api.deleteIncome(id);
      await loadIncomes();
    } catch (err) {
      setError(err.message);
    }
  }

  function onEditIncome(inc) {
    setEditingIncomeId(inc.id);
    setIncomeForm({
      date: inc.date || today,
      category: inc.category || "",
      amount: inc.amount ?? 0,
      description: inc.description || "",
    });
  }

  function onCancelIncome() {
    setEditingIncomeId(null);
    setIncomeForm({ date: today, category: "Ingreso", amount: 0, description: "" });
  }

  // --- filtros gastos ---
  function applyFilterDate() {
    if (!filterDate) {
      setFilterMessage("Ingresa una fecha para filtrar.");
      return;
    }
    setFilterMonth("");
    setFilterCategory("");
    const filtered = expenses.filter((e) => e.date === filterDate);
    setFilteredExpenses(filtered);
    setFilterMessage(`Filtrado por fecha ${filterDate}: ${filtered.length} resultado(s).`);
  }

  function applyFilterMonth() {
    if (!filterMonth) {
      setFilterMessage("Ingresa un mes YYYY-MM.");
      return;
    }
    setFilterDate("");
    const filtered = expenses.filter((e) => (e.date || "").startsWith(filterMonth));
    setFilteredExpenses(filtered);
    setFilterMessage(`Filtrado por mes ${filterMonth}: ${filtered.length} resultado(s).`);
  }

  function applyFilterCategory() {
    if (!filterCategory) {
      setFilterMessage("Ingresa una categoria.");
      return;
    }
    let source = expenses;
    if (filterMonth) {
      source = source.filter((e) => (e.date || "").startsWith(filterMonth));
    }
    const filtered = source.filter(
      (e) => (e.category || "").toLowerCase() === filterCategory.toLowerCase()
    );
    setFilteredExpenses(filtered);
    const total = filtered.reduce((acc, e) => acc + Number(e.amount || 0), 0);
    setFilterMessage(
      `Total en ${filterCategory}${filterMonth ? ` (${filterMonth})` : ""}: ${money(total)}`
    );
  }

  function resetFilters() {
    setFilteredExpenses(expenses);
    setFilterDate("");
    setFilterMonth("");
    setFilterCategory("");
    setFilterMessage("");
  }

  // --- filtros ingresos ---
  function applyIncomeFilterDate() {
    if (!incomeFilterDate) {
      setIncomeFilterMessage("Ingresa una fecha para filtrar.");
      return;
    }
    setIncomeFilterMonth("");
    setIncomeFilterCategory("");
    const filtered = incomes.filter((e) => e.date === incomeFilterDate);
    setFilteredIncomes(filtered);
    setIncomeFilterMessage(`Filtrado por fecha ${incomeFilterDate}: ${filtered.length} resultado(s).`);
  }

  function applyIncomeFilterMonth() {
    if (!incomeFilterMonth) {
      setIncomeFilterMessage("Ingresa un mes YYYY-MM.");
      return;
    }
    setIncomeFilterDate("");
    const filtered = incomes.filter((e) => (e.date || "").startsWith(incomeFilterMonth));
    setFilteredIncomes(filtered);
    setIncomeFilterMessage(`Filtrado por mes ${incomeFilterMonth}: ${filtered.length} resultado(s).`);
  }

  function applyIncomeFilterCategory() {
    if (!incomeFilterCategory) {
      setIncomeFilterMessage("Ingresa una categoria.");
      return;
    }
    let source = incomes;
    if (incomeFilterMonth) {
      source = source.filter((e) => (e.date || "").startsWith(incomeFilterMonth));
    }
    const filtered = source.filter(
      (e) => (e.category || "").toLowerCase() === incomeFilterCategory.toLowerCase()
    );
    setFilteredIncomes(filtered);
    const total = filtered.reduce((acc, e) => acc + Number(e.amount || 0), 0);
    setIncomeFilterMessage(
      `Total en ${incomeFilterCategory}${incomeFilterMonth ? ` (${incomeFilterMonth})` : ""}: ${money(total)}`
    );
  }

  function resetIncomeFilters() {
    setFilteredIncomes(incomes);
    setIncomeFilterDate("");
    setIncomeFilterMonth("");
    setIncomeFilterCategory("");
    setIncomeFilterMessage("");
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,#0f2a44,#081726_60%)] text-slate-100 overflow-x-hidden">
      <div className="flex flex-col md:grid md:grid-cols-[260px_1fr]">
        <Sidebar active={active} onChange={setActive} />

        <main className="p-4 md:p-8 w-full overflow-x-hidden">
          <Header />

          {error && (
            <div className="mt-4 rounded-2xl border border-red-500/30 bg-red-500/10 p-4 text-red-200">
              {error}
            </div>
          )}

          <div className="mt-6">
            {active === "Operaciones" && (
              <Operaciones
                expenses={expenses}
                filteredExpenses={filteredExpenses}
                stats={stats}
                money={money}
                form={form}
                setForm={setForm}
                onCreate={onSave}
                onEdit={onEdit}
                onDelete={onDelete}
                onCancel={onCancelEdit}
                editingId={editingId}
                loading={loading}
                filterDate={filterDate}
                setFilterDate={setFilterDate}
                filterMonth={filterMonth}
                setFilterMonth={setFilterMonth}
                filterCategory={filterCategory}
                setFilterCategory={setFilterCategory}
                onFilterDate={applyFilterDate}
                onFilterMonth={applyFilterMonth}
                onFilterCategory={applyFilterCategory}
                filterMessage={filterMessage}
                onReload={() => {
                  resetFilters();
                  loadAll();
                }}
              />
            )}

            {active === "Ingresos" && (
              <Ingresos
                incomes={incomes}
                filteredIncomes={filteredIncomes}
                money={money}
                form={incomeForm}
                setForm={setIncomeForm}
                onCreate={onSaveIncome}
                onEdit={onEditIncome}
                onDelete={onDeleteIncome}
                onCancel={onCancelIncome}
                editingId={editingIncomeId}
                loading={loading}
                filterDate={incomeFilterDate}
                setFilterDate={setIncomeFilterDate}
                filterMonth={incomeFilterMonth}
                setFilterMonth={setIncomeFilterMonth}
                filterCategory={incomeFilterCategory}
                setFilterCategory={setIncomeFilterCategory}
                onFilterDate={applyIncomeFilterDate}
                onFilterMonth={applyIncomeFilterMonth}
                onFilterCategory={applyIncomeFilterCategory}
                filterMessage={incomeFilterMessage}
                onReload={() => {
                  resetIncomeFilters();
                  loadIncomes();
                }}
              />
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
