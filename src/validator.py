from datetime import datetime


def validate_amount(amount):
    """Verifica que el monto sea positivo."""
    if amount < 0:
        raise ValueError("El monto debe ser un numero positivo.")


def validate_date(date_str):
    """Valida que la fecha este en formato YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Formato de fecha invalido. Use YYYY-MM-DD.")


def validate_code_max_length(code: str, max_len: int = 3) -> bool:
    """Valida que el codigo tenga maximo `max_len` caracteres."""
    if not isinstance(code, str):
        raise TypeError("code must be a string")

    if len(code) == 0:
        raise ValueError("code cannot be empty")

    if len(code) > max_len:
        raise ValueError(f"code must be at most {max_len} characters")

    return True
