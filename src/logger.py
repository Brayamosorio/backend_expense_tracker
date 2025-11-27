import logging
import os

LOG_FILE = "app.log"

_logger = logging.getLogger("expense_tracker")
_logger.setLevel(logging.INFO)


def _ensure_handler():
    """Configura el handler para que use el LOG_FILE actual (soporta monkeypatch en tests)."""
    expected_path = os.path.abspath(LOG_FILE)
    needs_handler = True
    for h in list(_logger.handlers):
        if getattr(h, "baseFilename", None) == expected_path:
            needs_handler = False
        else:
            _logger.removeHandler(h)
    if needs_handler:
        handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        _logger.addHandler(handler)


def log_action(action, details=""):
    """Registra una accion en el log."""
    _ensure_handler()
    _logger.info(f"{action}: {details}")


def log_error(error_message):
    """Registra un error."""
    _ensure_handler()
    _logger.error(error_message)
