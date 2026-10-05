from __future__ import annotations


def validate_customer_name(name: str) -> str:
    """Validate and normalize a customer name."""

    cleaned = name.strip()

    if not cleaned:
        raise ValueError("Customer name cannot be empty.")

    if len(cleaned) > 100:
        raise ValueError("Customer name must be 100 characters or fewer.")

    return cleaned


def validate_ingredients(ingredients: list[str]) -> list[str]:
    """Validate smoothie ingredients."""

    cleaned = [
        ingredient.strip().lower()
        for ingredient in ingredients
        if ingredient.strip()
    ]

    if not cleaned:
        raise ValueError("At least one ingredient is required.")

    if len(cleaned) > 5:
        raise ValueError("A smoothie can contain a maximum of five ingredients.")

    return cleaned