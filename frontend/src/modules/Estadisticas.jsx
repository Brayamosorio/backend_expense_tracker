export default function Estadisticas({
  stats,
  money,
  budgetStatus,
  budgetInput,
  setBudgetInput,
  onSaveBudget,
  alerts = [],
}) {
  return (
    <section className="grid gap-6">
      <div className="card p-6">
        <div className="kicker">ANALÍTICA</div>
        <h3 className="text-xl font-semibold">Reportes y estadísticas</h3>

        <div className="mt-4 grid gap-3 md:grid-cols-6">
          {[
            ["Total", stats?.total],
            ["Mínimo", stats?.min],
            ["Máximo", stats?.max],
            ["Promedio", stats?.avg],
            ["Std Dev", stats?.std_dev],
            ["Prom. mensual", stats?.monthly_avg],
          ].map(([k, v]) => (
            <div key={k} className="rounded-xl border border-white/10 bg-black/20 p-4">
              <p className="text-sm text-slate-300">{k}</p>
              <p className="mt-1 text-lg">{stats ? money(v) : "—"}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-xl font-semibold">Presupuesto y alertas</h3>
        <form onSubmit={onSaveBudget} className="mt-3 grid gap-3 md:grid-cols-[1fr_auto] md:items-end">
          <input
            className="input"
            type="number"
            placeholder="Presupuesto mensual COP"
            value={budgetInput}
            onChange={(e) => setBudgetInput(e.target.value)}
          />
          <button className="btn-primary" type="submit">
            Guardar
          </button>
        </form>

        <div className="mt-4 rounded-xl border border-white/10 bg-black/20 p-4 text-slate-100">
          {budgetStatus ? (
            <>
              <div className="text-sm text-slate-300">Estado presupuesto</div>
              <div className="mt-1 text-lg">
                {budgetStatus.status} — gastado {money(budgetStatus.spent)} / {money(budgetStatus.budget)}{" "}
                {budgetStatus.remaining !== undefined ? `(disp. ${money(budgetStatus.remaining)})` : ""}
              </div>
              <div className="text-xs text-slate-400">Mes: {budgetStatus.month}</div>
            </>
          ) : (
            "Sin presupuesto"
          )}
        </div>

        <div className="mt-3">
          <div className="label mb-1">Alertas</div>
          <ul className="space-y-1 text-sm text-slate-200">
            {alerts.length ? alerts.map((a, i) => <li key={i}>• {a}</li>) : <li>Sin alertas</li>}
          </ul>
        </div>
      </div>
    </section>
  );
}
