import { useMemo, useState } from "react";
import Tablas from "./Tablas";

const subTabs = ["Dashboards", "Registro", "Tablas"];

export default function Operaciones({
  expenses,
  filteredExpenses,
  stats,
  money,
  form,
  setForm,
  onCreate,
  onEdit,
  onDelete,
  onCancel,
  editingId,
  loading,
  filterDate,
  setFilterDate,
  filterMonth,
  setFilterMonth,
  filterCategory,
  setFilterCategory,
  onFilterDate,
  onFilterMonth,
  onFilterCategory,
  filterMessage,
  onReload,
}) {
  const [view, setView] = useState("Dashboards");

  const computedStats = useMemo(() => {
    if (stats) return stats;
    const list = Array.isArray(expenses) ? expenses : [];
    if (!list.length) return { total: 0, min: 0, max: 0, avg: 0 };
    const amounts = list.map((e) => Number(e.amount) || 0);
    const total = amounts.reduce((a, b) => a + b, 0);
    return {
      total,
      min: Math.min(...amounts),
      max: Math.max(...amounts),
      avg: amounts.length ? total / amounts.length : 0,
    };
  }, [stats, expenses]);

  const cards = [
    ["Total", money(computedStats.total)],
    ["Minimo", money(computedStats.min)],
    ["Maximo", money(computedStats.max)],
    ["Promedio", money(computedStats.avg)],
  ];

  return (
    <section className="grid gap-4">
      <div className="flex gap-3">
        {subTabs.map((t) => (
          <button
            key={t}
            onClick={() => setView(t)}
            className={[
              "btn",
              view === t ? "outline outline-2 outline-sky-400/30" : "",
            ].join(" ")}
          >
            {t}
          </button>
        ))}
      </div>

      {view === "Dashboards" && (
        <div className="card p-6">
          <div className="kicker">GASTOS</div>
          <h3 className="text-xl font-semibold">Resumen de gastos</h3>
          <div className="mt-4 grid gap-3 md:grid-cols-2 lg:grid-cols-4">
            {cards.map(([k, v]) => (
              <div key={k} className="rounded-xl border border-white/10 bg-black/20 p-4">
                <p className="text-sm text-slate-300">{k}</p>
                <p className="mt-1 text-lg">{v}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {view === "Registro" && (
        <div className="card p-6">
          <div className="kicker">GASTOS</div>
          <h3 className="text-xl font-semibold">Registro de gastos</h3>
          <form onSubmit={onCreate} className="mt-4 grid gap-4">
            <div>
              <div className="label mb-2">Descripcion</div>
              <input
                className="input"
                value={form.description}
                onChange={(e) => setForm({ ...form, description: e.target.value })}
                placeholder="Ej: Cena con amigos"
              />
            </div>

            <div>
              <div className="label mb-2">Categoria</div>
              <input
                className="input"
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
                placeholder="Comida, Transporte, etc."
              />
            </div>

            <div>
              <div className="label mb-2">Monto</div>
              <input
                className="input"
                type="number"
                value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })}
                placeholder="0.00"
              />
            </div>

            <div>
              <div className="label mb-2">Fecha</div>
              <input
                className="input"
                type="date"
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
              />
            </div>

            <div className="flex gap-2">
              <button className="btn-primary" type="submit" disabled={loading}>
                {editingId ? "Guardar cambios" : "Agregar gasto"}
              </button>
              {editingId && (
                <button type="button" className="btn" onClick={onCancel}>
                  Cancelar
                </button>
              )}
            </div>
          </form>
        </div>
      )}

      {view === "Tablas" && (
        <Tablas
          title="Gastos"
          items={filteredExpenses}
          onReload={onReload}
          onEdit={onEdit}
          onDelete={onDelete}
          loading={loading}
          filterDate={filterDate}
          setFilterDate={setFilterDate}
          filterMonth={filterMonth}
          setFilterMonth={setFilterMonth}
          filterCategory={filterCategory}
          setFilterCategory={setFilterCategory}
          onFilterDate={onFilterDate}
          onFilterMonth={onFilterMonth}
          onFilterCategory={onFilterCategory}
          filterMessage={filterMessage}
          money={money}
        />
      )}
    </section>
  );
}
