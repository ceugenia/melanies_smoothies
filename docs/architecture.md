# Architecture

## Overview

The Smoothie Analytics Platform is an end-to-end data engineering
application for collecting smoothie orders, validating data,
integrating external nutrition data, and presenting analytics through
Streamlit.

The project supports local development with SQLite and a Snowflake
implementation for cloud-based data engineering and analytics.

## Local Architecture

```text
FruityVice REST API
        |
        v
     Python
        |
        v
     SQLite
        |
        v
   SQL Analytics
        |
        v
    Streamlit