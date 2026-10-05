from __future__ import annotations

import requests
import streamlit as st
from api import get_fruit_data
from database import (
    get_daily_orders,
    get_order_summary,
    get_popular_ingredients,
    initialize_database,
    insert_order,
)
from validation import validate_customer_name, validate_ingredients

st.set_page_config(
    page_title="Smoothie Analytics",
    page_icon="🥤",
    layout="wide",
)


def render_dashboard() -> None:
    """Display order analytics."""
    st.subheader("Analytics Overview")

    summary = get_order_summary()

    if summary.empty:
        st.info("No orders have been recorded yet.")
        return

    metrics = summary.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Orders",
        int(metrics["TOTAL_ORDERS"]),
    )

    col2.metric(
        "Unique Customers",
        int(metrics["UNIQUE_CUSTOMERS"]),
    )

    first_order = metrics["FIRST_ORDER"]

    if first_order:
        col3.metric(
            "First Order",
            str(first_order)[:10],
        )

    st.subheader("Daily Order Volume")

    daily_orders = get_daily_orders()

    if not daily_orders.empty:
        daily_orders = daily_orders.set_index("ORDER_DATE")
        st.bar_chart(daily_orders["ORDER_COUNT"])

    st.subheader("Popular Ingredients")

    ingredients = get_popular_ingredients()

    if not ingredients.empty:
        st.dataframe(
            ingredients,
            use_container_width=True,
            hide_index=True,
        )


def render_order_form() -> None:
    """Display the smoothie order form."""
    st.subheader("Create Smoothie Order")

    customer_name = st.text_input(
        "Customer name",
        placeholder="Enter customer name",
    )

    ingredients = st.multiselect(
        "Choose ingredients",
        [
            "banana",
            "apple",
            "orange",
            "mango",
            "pineapple",
            "strawberry",
            "kiwi",
            "watermelon",
        ],
    )

    if st.button("Submit Order", type="primary"):
        try:
            customer = validate_customer_name(customer_name)
            selected = validate_ingredients(ingredients)

            insert_order(
                customer_name=customer,
                ingredients=selected,
            )

            st.success(
                "Smoothie order successfully stored in the local database!"
            )

        except ValueError as exc:
            st.error(str(exc))

        except Exception as exc:
            st.error(f"Unable to save order: {exc}")


def render_nutrition_api() -> None:
    """Display fruit nutrition API lookup."""
    st.subheader("Fruit Nutrition API")

    fruit = st.text_input(
        "Enter a fruit",
        placeholder="banana",
    )

    if st.button("Get Nutrition") and fruit:
        try:
            data = get_fruit_data(fruit)
            st.json(data)

        except requests.RequestException:
            st.error("Unable to reach the nutrition API.")

        except Exception as exc:
            st.error(f"Error: {exc}")


def main() -> None:
    """Run the Streamlit application."""
    initialize_database()

    st.title("🥤 Smoothie Analytics Platform")

    st.caption(
        "Local data engineering application using "
        "Python, SQL, SQLite, REST APIs, and Streamlit."
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Create Order",
            "Nutrition API",
        ],
    )

    if page == "Dashboard":
        render_dashboard()

    elif page == "Create Order":
        render_order_form()

    elif page == "Nutrition API":
        render_nutrition_api()


if __name__ == "__main__":
    main()