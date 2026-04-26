import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Page title
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Snowflake session
session = get_active_session()

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Pull fruit names for multiselect
fruit_rows = session.table("smoothies.public.fruit_options") \
    .select(col("FRUIT_NAME")) \
    .collect()

fruit_list = [row["FRUIT_NAME"] for row in fruit_rows]

# Limit to 5 fruits
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + " "

        # Get SEARCH_ON value for API
        search_row = session.table("smoothies.public.fruit_options") \
            .filter(col("FRUIT_NAME") == fruit_chosen) \
            .select(col("SEARCH_ON")) \
            .collect()

        search_on = search_row[0]["SEARCH_ON"]

        st.subheader(f"{fruit_chosen} Nutrition Information")

        api_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        st.dataframe(api_response.json(), use_container_width=True)

    submit_order = st.button("Submit Order")

    if submit_order:

        insert_stmt = f"""
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES
        ('{ingredients_string}', '{name_on_order}')
        """

        session.sql(insert_stmt).collect()

        st.success(
            f"Your Smoothie is ordered, {name_on_order}!",
            icon="✅"
        )
