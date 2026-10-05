from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "smoothies.db"


def get_connection() -> sqlite3.Connection:
    """Create a connection to the local SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the local database tables and analytics views."""
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS smoothie_orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS fruit_nutrition (
                fruit_name TEXT PRIMARY KEY,
                calories REAL,
                sugar_g REAL,
                carbohydrates_g REAL,
                protein_g REAL,
                fat_g REAL,
                source_api TEXT,
                ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE VIEW IF NOT EXISTS daily_order_volume AS
            SELECT
                DATE(ordered_at) AS order_date,
                COUNT(*) AS order_count
            FROM smoothie_orders
            GROUP BY DATE(ordered_at);

            CREATE VIEW IF NOT EXISTS popular_ingredients AS
            SELECT
                TRIM(value) AS ingredient,
                COUNT(*) AS usage_count
            FROM smoothie_orders,
            json_each(
                '["' ||
                REPLACE(ingredients, ', ', '","') ||
                '"]'
            )
            GROUP BY TRIM(value);

            CREATE VIEW IF NOT EXISTS order_summary AS
            SELECT
                COUNT(*) AS total_orders,
                COUNT(DISTINCT customer_name) AS unique_customers,
                MIN(ordered_at) AS first_order,
                MAX(ordered_at) AS last_order
            FROM smoothie_orders;
            """
        )


def insert_order(customer_name: str, ingredients: list[str]) -> None:
    """Insert a validated smoothie order."""
    ingredient_string = ", ".join(ingredients)

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO smoothie_orders
                (customer_name, ingredients)
            VALUES (?, ?)
            """,
            (customer_name, ingredient_string),
        )


def get_order_summary():
    """Return aggregate order metrics."""
    import pandas as pd

    with get_connection() as connection:
        return pd.read_sql_query(
            """
            SELECT
                total_orders AS TOTAL_ORDERS,
                unique_customers AS UNIQUE_CUSTOMERS,
                first_order AS FIRST_ORDER,
                last_order AS LAST_ORDER
            FROM order_summary
            """,
            connection,
        )


def get_daily_orders():
    """Return daily order volume."""
    import pandas as pd

    with get_connection() as connection:
        return pd.read_sql_query(
            """
            SELECT
                order_date AS ORDER_DATE,
                order_count AS ORDER_COUNT
            FROM daily_order_volume
            ORDER BY order_date
            """,
            connection,
        )


def get_popular_ingredients():
    """Return the most frequently used smoothie ingredients."""
    import pandas as pd

    with get_connection() as connection:
        return pd.read_sql_query(
            """
            SELECT
                ingredient AS INGREDIENT,
                usage_count AS USAGE_COUNT
            FROM popular_ingredients
            ORDER BY usage_count DESC
            LIMIT 10
            """,
            connection,
        )