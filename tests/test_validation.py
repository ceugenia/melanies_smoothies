import pytest

from app.validation import (
    validate_customer_name,
    validate_ingredients,
)


def test_customer_name_is_trimmed():
    assert validate_customer_name("  Constanza  ") == "Constanza"


def test_empty_customer_name_fails():
    with pytest.raises(ValueError):
        validate_customer_name("")


def test_ingredients_are_normalized():
    result = validate_ingredients(
        [" Banana ", "STRAWBERRY"]
    )

    assert result == ["banana", "strawberry"]


def test_empty_ingredients_fail():
    with pytest.raises(ValueError):
        validate_ingredients([])