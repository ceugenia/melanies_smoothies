from __future__ import annotations

from typing import Any

import requests

API_URL = "https://www.fruityvice.com/api/fruit"


def get_fruit_data(fruit_name: str) -> dict[str, Any]:
    """Retrieve nutrition information for a fruit from the public API."""

    url = f"{API_URL}/{fruit_name.strip().lower()}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError("Unexpected API response format.")

    return data