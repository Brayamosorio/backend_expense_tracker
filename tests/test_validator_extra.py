import pytest

from src.validator import (
    validate_amount,
    validate_code_max_length,
    validate_date,
)


def test_validate_code_max_length_empty():
    with pytest.raises(ValueError):
        validate_code_max_length("")


def test_validate_code_max_length_type_error():
    with pytest.raises(TypeError):
        validate_code_max_length(123)  # type: ignore[arg-type]


def test_validate_code_max_length_custom_len_ok():
    assert validate_code_max_length("AB", max_len=2) is True


def test_validate_code_max_length_custom_len_fail():
    with pytest.raises(ValueError):
        validate_code_max_length("ABCD", max_len=2)


def test_validate_amount_zero_is_allowed():
    validate_amount(0)


def test_validate_amount_negative_float_raises():
    with pytest.raises(ValueError):
        validate_amount(-0.1)


def test_validate_date_leap_year_valid():
    validate_date("2024-02-29")


def test_validate_date_invalid_month():
    with pytest.raises(ValueError):
        validate_date("2025-13-01")


def test_validate_date_invalid_day():
    with pytest.raises(ValueError):
        validate_date("2025-11-31")


def test_validate_date_non_string_type():
    with pytest.raises((TypeError, ValueError)):
        validate_date(None)  # type: ignore[arg-type]
