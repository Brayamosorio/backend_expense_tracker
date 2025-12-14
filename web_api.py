from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src import db_mysql
from pathlib import Path
from datetime import datetime
import statistics
import json


app = FastAPI(
    title="Expense Tracker API",
    description="API sencilla para gestionar gastos con MySQL/MariaDB",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExpenseCreate(BaseModel):
    date: str
    category: str
    amount: float
    description: str | None = None


class ExpenseRead(ExpenseCreate):
    id: int

class BudgetPayload(BaseModel):
    amount: float


def _load_budget_file() -> Dict[str, Any]:
    budget_file = Path("budget.json")
    if budget_file.exists():
        try:
            return json.loads(budget_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"budget": 0, "last_updated": None}
    return {"budget": 0, "last_updated": None}


def _save_budget_file(amount: float) -> Dict[str, Any]:
    budget_file = Path("budget.json")
    data = {"budget": amount, "last_updated": datetime.now().strftime("%Y-%m-%d")}
    budget_file.write_text(json.dumps(data, indent=4), encoding="utf-8")
    return data


def _get_stats_from_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {
            "min": 0,
            "max": 0,
            "avg": 0,
            "std_dev": 0,
            "daily_avg": 0,
            "monthly_avg": 0,
            "top_category": None,
            "top_category_amount": 0,
            "days_without_expense": 0,
        }
    amounts = [r["amount"] for r in rows]
    min_v = min(amounts)
    max_v = max(amounts)
    avg_v = round(statistics.mean(amounts), 2)
    std_v = round(statistics.pstdev(amounts), 2)

    unique_dates = {r["date"] for r in rows if r.get("date")}
    unique_months = {(r["date"] or "")[:7] for r in rows if r.get("date")}
    daily_avg = round(sum(amounts) / len(unique_dates), 2) if unique_dates else sum(amounts)
    monthly_avg = round(sum(amounts) / len(unique_months), 2) if unique_months else sum(amounts)

    totals_by_cat: Dict[str, float] = {}
    for r in rows:
        cat = r["category"]
        totals_by_cat[cat] = totals_by_cat.get(cat, 0) + r["amount"]
    top_cat = max(totals_by_cat, key=totals_by_cat.get) if totals_by_cat else None
    top_cat_amount = round(totals_by_cat[top_cat], 2) if top_cat else 0

    # dias sin gasto
    parsed_dates = sorted(
        {datetime.strptime(d, "%Y-%m-%d") for d in unique_dates if d},
        key=lambda d: d,
    )
    gaps = 0
    if len(parsed_dates) >= 2:
        for i in range(1, len(parsed_dates)):
            diff = (parsed_dates[i] - parsed_dates[i - 1]).days
            if diff > 1:
                gaps += diff - 1

    return {
        "min": min_v,
        "max": max_v,
        "avg": avg_v,
        "std_dev": std_v,
        "daily_avg": daily_avg,
        "monthly_avg": monthly_avg,
        "top_category": top_cat,
        "top_category_amount": top_cat_amount,
        "days_without_expense": gaps,
        "total": sum(amounts),
    }


@app.get("/api/expenses", response_model=List[ExpenseRead])
def list_expenses():
    return db_mysql.get_all_expenses()


@app.get("/api/expenses/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: int):
    expense = db_mysql.get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.post("/api/expenses", response_model=ExpenseRead, status_code=201)
def create_expense(expense: ExpenseCreate):
    new_id = db_mysql.insert_expense(
        date_=expense.date,
        category=expense.category,
        amount=expense.amount,
        description=expense.description,
    )
    return ExpenseRead(id=new_id, **expense.dict())


@app.put("/api/expenses/{expense_id}", response_model=ExpenseRead)
def update_expense(expense_id: int, expense: ExpenseCreate):
    updated = db_mysql.update_expense(
        expense_id=expense_id,
        date_=expense.date,
        category=expense.category,
        amount=expense.amount,
        description=expense.description,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return ExpenseRead(id=expense_id, **expense.dict())


@app.delete("/api/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    deleted = db_mysql.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return


@app.get("/api/stats")
def get_stats():
    rows = db_mysql.get_all_expenses()
    return {"stats": _get_stats_from_rows(rows)}


@app.post("/api/budget")
def set_budget(payload: BudgetPayload):
    if payload.amount < 0:
        raise HTTPException(status_code=400, detail="amount must be positive")
    data = _save_budget_file(payload.amount)
    return data


@app.get("/api/budget/status")
def budget_status():
    budget_data = _load_budget_file()
    budget_amount = budget_data.get("budget", 0)
    if budget_amount <= 0:
        return {"status": "Sin presupuesto", "budget": 0, "spent": 0, "remaining": 0}
    rows = db_mysql.get_all_expenses()
    month_prefix = datetime.now().strftime("%Y-%m")
    spent = sum(r["amount"] for r in rows if (r.get("date") or "").startswith(month_prefix))
    remaining = max(budget_amount - spent, 0)
    status = "OK" if spent <= budget_amount else "Superado"
    return {
        "status": status,
        "budget": budget_amount,
        "spent": spent,
        "remaining": remaining,
        "month": month_prefix,
    }


@app.get("/api/alerts")
def alerts():
    rows = db_mysql.get_all_expenses()
    stats = _get_stats_from_rows(rows)
    # alerta inactividad
    if rows:
        last_date = max(r["date"] for r in rows if r.get("date"))
        last_dt = datetime.strptime(last_date, "%Y-%m-%d")
        diff = (datetime.now() - last_dt).days
        inactivity = f"No registras gastos hace {diff} dias." if diff >= 3 else "Actividad reciente registrada."
    else:
        inactivity = "No hay gastos registrados."

    budget_info = budget_status()
    alerts = [inactivity]
    if budget_info["status"] == "Superado":
        alerts.append(f"Presupuesto superado: {budget_info['spent']} / {budget_info['budget']}")
    return {"alerts": alerts, "stats": stats}
