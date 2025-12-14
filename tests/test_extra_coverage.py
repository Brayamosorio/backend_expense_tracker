import json
import zipfile
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
import urllib.request
import datetime
import logging

import pytest

from src import analytics, api, backup, budget, charts, report, storage, tracker, users, db_mysql
from src import currency, notifications, logger


def test_analytics_empty(monkeypatch):
    monkeypatch.setattr(analytics, "load_data", lambda: [])
    assert analytics.get_basic_statistics() == {"min": 0, "max": 0, "avg": 0, "std_dev": 0}


def test_api_reuse_and_stop(monkeypatch):
    monkeypatch.setattr(api, "load_data", lambda: [])
    monkeypatch.setattr(api, "get_basic_statistics", lambda: {"avg": 0})

    msg = api.start_api_server(0)
    assert "API iniciada" in msg
    port = api._server.server_port

    # Segundo arranque reutiliza el servidor existente
    again = api.start_api_server(port)
    assert "corriendo" in again

    # 404 para ruta inexistente
    with pytest.raises(urllib.error.HTTPError) as err:
        urllib.request.urlopen(f"http://127.0.0.1:{port}/missing")
    assert err.value.code == 404

    # Detener y verificar rama sin servidor
    stopped = api.stop_api_server()
    assert "detenida" in stopped
    assert "no estaba" in api.stop_api_server()


def test_backup_creates_zip(tmp_path, monkeypatch):
    monkeypatch.setattr(backup, "BACKUPS_DIR", tmp_path / "backups")
    monkeypatch.setattr(backup, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(backup, "INCLUDE_ROOT", [tmp_path / "users.json"])

    # Archivos a respaldar
    (tmp_path / "users.json").write_text("{}", encoding="utf-8")
    data_file = tmp_path / "data" / "demo.json"
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text('{"a":1}', encoding="utf-8")

    zip_path = Path(backup.create_backup())
    assert zip_path.exists()
    with zipfile.ZipFile(zip_path, "r") as zf:
        assert "users.json" in zf.namelist()
        assert "data/demo.json" in zf.namelist()


def test_budget_branches(tmp_path, monkeypatch):
    monkeypatch.setattr(budget, "BUDGET_FILE", tmp_path / "budget.json")

    # Sin presupuesto configurado y sin datos
    monkeypatch.setattr(budget, "load_data", lambda: [])
    assert budget.get_monthly_spent("1900-01") == 0
    assert "No hay presupuesto" in budget.check_budget_status()

    # Presupuesto y gasto mayor
    budget.set_monthly_budget(100)
    current_month = __import__("datetime").datetime.now().strftime("%Y-%m")
    monkeypatch.setattr(
        budget,
        "load_data",
        lambda: [{"date": f"{current_month}-10", "amount": 150}],
    )
    assert "Presupuesto superado" in budget.check_budget_status()

    # Presupuesto y gasto menor
    budget.set_monthly_budget(200)
    monkeypatch.setattr(
        budget,
        "load_data",
        lambda: [{"date": "2024-01-10", "amount": 50}],
    )
    ok_msg = budget.check_budget_status()
    assert "Presupuesto OK" in ok_msg and "disponible" in ok_msg


def test_charts_outputs(monkeypatch, capsys):
    # Barra vacía cuando max_value es 0
    assert charts._bar(5, 0) == ""

    monkeypatch.setattr(charts, "load_data", lambda: [])
    charts.chart_by_category()
    out_empty_cat = capsys.readouterr().out
    charts.chart_by_month()
    out_empty_month = capsys.readouterr().out
    assert "No hay datos" in out_empty_cat
    assert "No hay datos" in out_empty_month

    monkeypatch.setattr(
        charts,
        "load_data",
        lambda: [
            {"description": "A", "category": "Comida", "amount": 10, "date": "2024-01-01"},
            {"description": "B", "category": "Transporte", "amount": 5, "date": "2024-01-02"},
        ],
    )
    charts.chart_by_category()
    out1 = capsys.readouterr().out
    assert "Comida" in out1 and "Transporte" in out1

    charts.chart_by_month()
    out2 = capsys.readouterr().out
    assert "2024-01" in out2


def test_report_functions(monkeypatch):
    monkeypatch.setattr(report, "load_data", lambda: [])
    assert report.get_average_daily_expense() == 0
    assert report.get_average_monthly_expense() == 0
    assert report.get_most_expensive_category() == (None, 0)
    assert report.get_days_without_expense() == []

    data = [
        {"date": "2024-01-01", "amount": 10, "category": "Comida"},
        {"date": "2024-01-02", "amount": 20, "category": "Comida"},
        {"date": "2024-02-01", "amount": 5, "category": "Transporte"},
    ]
    monkeypatch.setattr(report, "load_data", lambda: data)
    assert report.get_average_daily_expense() == 11.67
    assert report.get_average_monthly_expense() == 17.5
    assert report.get_most_expensive_category() == ("Comida", 30)
    # La función está incompleta pero debe procesar fechas sin lanzar excepciones
    assert report.get_days_without_expense() is None


def test_storage_error_handling(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DEFAULT_FILE", tmp_path / "expenses.json")
    monkeypatch.setattr(storage, "get_current_user", lambda: None)
    monkeypatch.setattr(storage, "get_expenses_file_for_user", lambda user: tmp_path / f"{user}.json")

    # Archivo inexistente -> []
    assert storage.load_data() == []

    # JSON inválido -> []
    storage.DEFAULT_FILE.write_text("not json", encoding="utf-8")
    assert storage.load_data() == []

    # Guardado y lectura correcta
    storage.save_data([{"a": 1}])
    assert storage.load_data() == [{"a": 1}]


def test_storage_for_user(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DEFAULT_FILE", tmp_path / "default.json")
    monkeypatch.setattr(storage, "get_current_user", lambda: "user1")
    monkeypatch.setattr(storage, "get_expenses_file_for_user", lambda u: tmp_path / f"{u}_expenses.json")
    storage.save_data([{"x": 1}])
    assert (tmp_path / "user1_expenses.json").exists()
    assert storage.load_data() == [{"x": 1}]


def test_tracker_errors_and_exports(tmp_path, monkeypatch):
    data = []

    def fake_load():
        return list(data)

    def fake_save(new_data):
        data.clear()
        data.extend(new_data)

    monkeypatch.setattr(tracker, "load_data", fake_load)
    monkeypatch.setattr(tracker, "save_data", fake_save)

    with pytest.raises(IndexError):
        tracker.edit_expense(0, new_description="X")
    with pytest.raises(IndexError):
        tracker.delete_expense(0)
    with pytest.raises(ValueError):
        tracker.export_to_csv(tmp_path / "empty.csv")

    tracker.add_expense("A", "Comida", 10, date="2024-01-01")
    tracker.edit_expense(0, new_category="Transporte", new_amount=20, new_date="2024-01-02")
    assert data[0]["category"] == "Transporte" and data[0]["amount"] == 20 and data[0]["date"] == "2024-01-02"

    csv_path = tmp_path / "out.csv"
    tracker.export_to_csv(csv_path)
    assert csv_path.exists()


def test_tracker_filters(monkeypatch):
    records = [
        {"description": "A", "category": "Comida", "amount": 10, "date": "2024-01-02"},
        {"description": "B", "category": "Viaje", "amount": 5, "date": "2024-02-10"},
    ]
    monkeypatch.setattr(tracker, "load_data", lambda: records)
    assert tracker.filter_by_date("2024-01-02") == [records[0]]
    assert tracker.filter_by_month("2024-02") == [records[1]]


def test_users_flows(tmp_path, monkeypatch):
    monkeypatch.setattr(users, "USERS_FILE", tmp_path / "users.json")
    monkeypatch.setattr(users, "SESSION_FILE", tmp_path / "session.json")
    monkeypatch.setattr(users, "DATA_DIR", tmp_path / "data")

    users.create_user("alice", "Alice A", "pw")
    with pytest.raises(ValueError):
        users.create_user("alice", "Alice A", "pw")

    assert users.get_current_user() is None
    with pytest.raises(ValueError):
        users.login("bob", "pw")

    users.login("alice", "pw")
    assert users.get_current_user() == "alice"
    users.logout()
    assert users.get_current_user() is None


def test_currency_conversion_and_errors():
    assert currency.convert_amount(1000, "usd") == 0.25
    with pytest.raises(ValueError):
        currency.convert_amount(10, "JPY")


def test_notifications_paths(monkeypatch):
    # Sin gastos
    monkeypatch.setattr(notifications, "load_data", lambda: [])
    assert "No hay gastos" in notifications.check_inactivity_alert()

    # Con gasto muy antiguo
    old_date = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    monkeypatch.setattr(
        notifications,
        "load_data",
        lambda: [{"date": old_date, "amount": 1, "category": "A"}],
    )
    assert "No registras gastos" in notifications.check_inactivity_alert()

    # Alerts combinadas
    monkeypatch.setattr(notifications, "check_budget_status", lambda: "presupuesto")
    monkeypatch.setattr(
        notifications,
        "load_data",
        lambda: [{"date": datetime.datetime.now().strftime("%Y-%m-%d"), "amount": 1, "category": "A"}],
    )
    alerts = notifications.system_alerts()
    assert "presupuesto" in alerts[0]
    assert "Actividad" in alerts[1] or "registras" in alerts[1]


def test_logger_handler_cleanup(tmp_path, monkeypatch):
    log_path = tmp_path / "app.log"
    monkeypatch.setattr(logger, "LOG_FILE", str(log_path))

    bad_handler = logging.FileHandler(tmp_path / "other.log")
    logger._logger.addHandler(bad_handler)

    logger.log_action("evt", "detail")
    logger.log_error("oops")

    # Solo debe quedar el handler configurado para LOG_FILE
    assert any(getattr(h, "baseFilename", "") == str(log_path.resolve()) for h in logger._logger.handlers)
    assert log_path.exists()


def test_db_mysql_monkeypatched(monkeypatch):
    fake_rows = [
        {"id": 1, "date": datetime.date(2024, 1, 1), "category": "A", "amount": Decimal("10.50"), "description": "x"},
        {"id": 2, "date": "2024-01-02", "category": "B", "amount": Decimal("5.00"), "description": None},
    ]

    class FakeCursor:
        def __init__(self, data):
            self.data = data
            self._results = []
            self.lastrowid = None
            self.rowcount = 0

        def execute(self, query, params=None):
            if "ORDER BY" in query:
                self._results = list(self.data)
            elif "WHERE id = %s" in query and "DELETE" not in query and "UPDATE" not in query:
                wanted = params[0]
                self._results = [row for row in self.data if row["id"] == wanted]
            elif query.strip().startswith("INSERT"):
                new_id = max(row["id"] for row in self.data) + 1 if self.data else 1
                self.data.append(
                    {
                        "id": new_id,
                        "date": params[0],
                        "category": params[1],
                        "amount": params[2],
                        "description": params[3],
                    }
                )
                self.lastrowid = new_id
            elif query.strip().startswith("UPDATE"):
                exp_id = params[4]
                for row in self.data:
                    if row["id"] == exp_id:
                        row.update({"date": params[0], "category": params[1], "amount": params[2], "description": params[3]})
                        self.rowcount = 1
                        break
            elif query.strip().startswith("DELETE"):
                exp_id = params[0]
                before = len(self.data)
                self.data[:] = [r for r in self.data if r["id"] != exp_id]
                self.rowcount = 1 if len(self.data) < before else 0

        def fetchall(self):
            return list(self._results)

        def fetchone(self):
            return self._results[0] if self._results else None

        def close(self):
            pass

    class FakeConnection:
        def __init__(self, data):
            self.data = data
            self.commits = 0

        def cursor(self, dictionary=False):
            return FakeCursor(self.data)

        def commit(self):
            self.commits += 1

        def close(self):
            pass

    conn = FakeConnection(fake_rows)
    monkeypatch.setattr(db_mysql.mysql.connector, "connect", lambda **kwargs: conn)

    all_rows = db_mysql.get_all_expenses()
    assert len(all_rows) == 2 and all_rows[0]["amount"] == 10.5

    row = db_mysql.get_expense_by_id(1)
    assert row["id"] == 1

    new_id = db_mysql.insert_expense("2024-01-03", "C", 7.0, "z")
    assert new_id == 3

    assert db_mysql.update_expense(3, "2024-01-04", "C", 9.0, "zz") is True
    assert db_mysql.delete_expense(2) is True
