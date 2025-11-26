from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src import analytics, tracker


app = FastAPI(title="Expense Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExpenseIn(BaseModel):
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    date: Optional[str] = None


class ExpenseOut(ExpenseIn):
    id: int


def _with_index(expenses):
    """Attach list index as public id."""
    return [{"id": idx, **exp} for idx, exp in enumerate(expenses)]


@app.get("/api/expenses", response_model=List[ExpenseOut])
def list_expenses():
    expenses = tracker.list_expenses()
    return _with_index(expenses)


@app.get("/api/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense(expense_id: int):
    expenses = tracker.list_expenses()
    if expense_id < 0 or expense_id >= len(expenses):
        raise HTTPException(status_code=404, detail="Gasto no encontrado.")
    return {"id": expense_id, **expenses[expense_id]}


@app.post("/api/expenses", response_model=ExpenseOut, status_code=201)
def create_expense(expense: ExpenseIn):
    created = tracker.add_expense(
        description=expense.description,
        category=expense.category,
        amount=expense.amount,
        date=expense.date,
    )
    expenses = tracker.list_expenses()
    return {"id": len(expenses) - 1, **created}


@app.put("/api/expenses/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, expense: ExpenseIn):
    try:
        updated = tracker.edit_expense(
            expense_id,
            new_description=expense.description,
            new_category=expense.category,
            new_amount=expense.amount,
            new_date=expense.date,
        )
    except IndexError:
        raise HTTPException(status_code=404, detail="Gasto no encontrado.")
    return {"id": expense_id, **updated}


@app.delete("/api/expenses/{expense_id}", response_model=ExpenseOut)
def delete_expense(expense_id: int):
    try:
        removed = tracker.delete_expense(expense_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="Gasto no encontrado.")
    return {"id": expense_id, **removed}


@app.get("/api/stats")
def get_stats():
    return analytics.get_basic_statistics()
