from __future__ import annotations

from decimal import Decimal
from typing import Any, Dict, List, Optional

import mysql.connector
from mysql.connector import Error


def get_connection():
    """Crea y devuelve una conexión MySQL/MariaDB (ajusta user/password si usas credenciales)."""
    return mysql.connector.connect(
        host="localhost",
        user="root",  # cambia si tienes otro usuario
        password="",  # pon tu contraseña si la tienes
        database="expense_tracker",
    )


def get_all_expenses() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, date, category, amount, description FROM expenses ORDER BY date DESC, id DESC"
    )
    rows = [_normalize_row(r) for r in cursor.fetchall()]
    cursor.close()
    conn.close()
    return rows


def get_expense_by_id(expense_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, date, category, amount, description FROM expenses WHERE id = %s",
        (expense_id,),
    )
    raw = cursor.fetchone()
    row = _normalize_row(raw) if raw else None
    cursor.close()
    conn.close()
    return row if row else None


def insert_expense(date_: str, category: str, amount: float, description: Optional[str]) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO expenses (date, category, amount, description)
        VALUES (%s, %s, %s, %s)
        """,
        (date_, category, amount, description),
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def update_expense(
    expense_id: int, date_: str, category: str, amount: float, description: Optional[str]
) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE expenses
        SET date = %s, category = %s, amount = %s, description = %s
        WHERE id = %s
        """,
        (date_, category, amount, description, expense_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return updated


def delete_expense(expense_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return deleted


def get_all_incomes() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, date, category, amount, description FROM incomes ORDER BY date DESC, id DESC"
    )
    rows = [_normalize_row(r) for r in cursor.fetchall()]
    cursor.close()
    conn.close()
    return rows


def get_income_by_id(income_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, date, category, amount, description FROM incomes WHERE id = %s",
        (income_id,),
    )
    raw = cursor.fetchone()
    row = _normalize_row(raw) if raw else None
    cursor.close()
    conn.close()
    return row if row else None


def insert_income(date_: str, category: str, amount: float, description: Optional[str]) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO incomes (date, category, amount, description)
        VALUES (%s, %s, %s, %s)
        """,
        (date_, category, amount, description),
    )
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return new_id


def update_income(
    income_id: int, date_: str, category: str, amount: float, description: Optional[str]
) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE incomes
        SET date = %s, category = %s, amount = %s, description = %s
        WHERE id = %s
        """,
        (date_, category, amount, description, income_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return updated


def delete_income(income_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incomes WHERE id = %s", (income_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return deleted


def _normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Convierte valores a tipos serializables para la API."""
    normalized = dict(row)
    if isinstance(normalized.get("date"), (str, bytes)):
        normalized["date"] = str(normalized["date"])
    elif normalized.get("date") is not None:
        normalized["date"] = normalized["date"].isoformat()
    if isinstance(normalized.get("amount"), Decimal):
        normalized["amount"] = float(normalized["amount"])
    return normalized
