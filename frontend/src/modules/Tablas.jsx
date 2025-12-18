export default function Tablas({
  title = "Gastos",
  items,
  expenses,
  onReload,
  onEdit,
  onDelete,
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
  money,
}) {
  const rows = items ?? expenses ?? [];

  return (
    <section className="grid gap-6 lg:grid-cols-2">
      <div className="card p-6">
        <div className="flex justify-between items-center">
          <h3 className="text-xl font-semibold">{title}</h3>
          <button className="btn" onClick={onReload}>
            Recargar
          </button>
        </div>

        <div className="mt-4 overflow-auto rounded-xl border border-white/10">
          <table className="min-w-[720px] w-full text-sm">
            <thead className="bg-black/20">
              <tr>
                <th className="px-3 py-2 text-left">Descripcion</th>
                <th className="px-3 py-2 text-left">Categoria</th>
                <th className="px-3 py-2 text-left">Monto</th>
                <th className="px-3 py-2 text-left">Fecha</th>
                <th className="px-3 py-2 text-left">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {rows.length ? (
                rows.map((e, i) => (
                  <tr key={i} className="border-t border-white/10">
                    <td className="px-3 py-2">{e.description ?? ""}</td>
                    <td className="px-3 py-2">{e.category}</td>
                    <td className="px-3 py-2">{money ? money(e.amount) : `$${e.amount}`}</td>
                    <td className="px-3 py-2">{e.date}</td>
                    <td className="px-3 py-2 space-x-2">
                      <button className="btn" onClick={() => onEdit(e)} disabled={loading}>
                        Editar
                      </button>
                      <button className="btn" onClick={() => onDelete(e.id)} disabled={loading}>
                        Borrar
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="px-3 py-4 text-slate-400">
                    Sin datos
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card p-6">
        <h3 className="text-xl font-semibold">Filtros y busqueda</h3>

        <div className="mt-4 grid gap-4">
          <div className="flex gap-2">
            <input
              type="date"
              className="input"
              value={filterDate}
              onChange={(e) => setFilterDate && setFilterDate(e.target.value)}
            />
            <button className="btn" onClick={onFilterDate}>Filtrar fecha</button>
          </div>

          <div className="flex gap-2">
            <input
              type="month"
              className="input"
              value={filterMonth}
              onChange={(e) => setFilterMonth && setFilterMonth(e.target.value)}
            />
            <button className="btn" onClick={onFilterMonth}>Filtrar mes</button>
          </div>

          <div className="flex gap-2">
            <input
              className="input"
              placeholder="Ej: Comida"
              value={filterCategory}
              onChange={(e) => setFilterCategory && setFilterCategory(e.target.value)}
            />
            <button className="btn" onClick={onFilterCategory}>Total por categoria</button>
          </div>

          {filterMessage && (
            <p className="text-sm text-slate-200">{filterMessage}</p>
          )}
        </div>
      </div>
    </section>
  );
}
