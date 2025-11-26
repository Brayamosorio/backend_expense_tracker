from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src import db_mysql


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
