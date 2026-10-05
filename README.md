# 🥤 Smoothie Analytics Platform

An end-to-end data engineering and analytics application built with Python, SQL, REST APIs, SQLite, Streamlit, and Snowflake.

## Project Overview

This project demonstrates a complete data workflow from external API integration and data validation to database storage, analytical SQL, automated testing, and interactive visualization.

The application supports two environments:

- Local development using SQLite
- Cloud implementation using Snowflake

## Tech Stack

- Python
- SQL
- SQLite
- Snowflake
- Snowpark Python
- Streamlit
- REST APIs
- Pandas
- Pytest
- Ruff
- GitHub Actions

## Architecture

### Local Development

```text
REST API
    ↓
  Python
    ↓
  SQLite
    ↓
SQL Analytics
    ↓
Streamlit