import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_URL = os.getenv("DB_URL", "")
DB_TABLAS = [t.strip() for t in os.getenv("DB_TABLAS", "").split(",") if t.strip()]
TIPO_REPORTE = os.getenv("TIPO_REPORTE", "general")


@st.cache_resource
def get_engine():
    if not DB_URL:
        raise ValueError("Falta configurar DB_URL en el archivo .env")
    return create_engine(DB_URL)


@st.cache_data
def cargar_tabla(nombre_tabla: str, limite: int = 10000) -> pd.DataFrame:
    engine = get_engine()
    query = text(f"SELECT * FROM {nombre_tabla} LIMIT :limite")
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params={"limite": limite})
