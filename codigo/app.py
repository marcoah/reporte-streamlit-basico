import pandas as pd
import plotly.express as px
import streamlit as st

from db import DB_TABLAS, TIPO_REPORTE, cargar_tabla

st.set_page_config(page_title=f"Reporte de {TIPO_REPORTE}", layout="wide")
st.title(f"Reporte de {TIPO_REPORTE}")

if not DB_TABLAS:
    st.error("No hay tablas configuradas. Completá DB_TABLAS en el archivo .env")
    st.stop()

tabla_seleccionada = st.sidebar.selectbox("Tabla", DB_TABLAS)

try:
    df = cargar_tabla(tabla_seleccionada)
except Exception as error:
    st.error(f"No se pudo conectar a la base de datos: {error}")
    st.stop()

if df.empty:
    st.warning("La tabla no tiene datos.")
    st.stop()

columnas_fecha = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()
columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
columnas_categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()

st.sidebar.header("Filtros")
df_filtrado = df.copy()

if columnas_fecha:
    col_fecha = st.sidebar.selectbox("Columna de fecha", columnas_fecha)
    fecha_min, fecha_max = df[col_fecha].min(), df[col_fecha].max()
    rango = st.sidebar.date_input("Rango de fechas", (fecha_min, fecha_max))
    if isinstance(rango, tuple) and len(rango) == 2:
        inicio, fin = rango
        df_filtrado = df_filtrado[
            (df_filtrado[col_fecha] >= pd.Timestamp(inicio))
            & (df_filtrado[col_fecha] <= pd.Timestamp(fin))
        ]

if columnas_categoricas:
    col_categoria = st.sidebar.selectbox("Columna categórica", columnas_categoricas)
    valores = st.sidebar.multiselect(
        "Valores", sorted(df[col_categoria].dropna().unique().tolist())
    )
    if valores:
        df_filtrado = df_filtrado[df_filtrado[col_categoria].isin(valores)]

st.subheader("Indicadores")
if columnas_numericas:
    cols_kpi = st.columns(min(len(columnas_numericas), 4))
    for col, nombre in zip(cols_kpi, columnas_numericas[:4]):
        col.metric(nombre, f"{df_filtrado[nombre].sum():,.2f}")
else:
    st.info("No se detectaron columnas numéricas para calcular indicadores.")

st.subheader("Detalle de datos")
st.dataframe(df_filtrado, use_container_width=True)

if columnas_numericas:
    st.subheader("Gráfico")
    col_valor = st.selectbox("Valor a graficar", columnas_numericas)
    if columnas_fecha:
        fig = px.line(
            df_filtrado.sort_values(columnas_fecha[0]),
            x=columnas_fecha[0],
            y=col_valor,
            title=f"Evolución de {col_valor}",
        )
    elif columnas_categoricas:
        agrupado = (
            df_filtrado.groupby(columnas_categoricas[0])[col_valor].sum().reset_index()
        )
        fig = px.bar(
            agrupado,
            x=columnas_categoricas[0],
            y=col_valor,
            title=f"{col_valor} por {columnas_categoricas[0]}",
        )
    else:
        fig = px.histogram(df_filtrado, x=col_valor, title=f"Distribución de {col_valor}")
    st.plotly_chart(fig, use_container_width=True)
