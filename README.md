# reporte-streamlit-basico

Esqueleto básico para armar un reporte con streamlit

## Estructura

- [`prompt/basico.md`](prompt/basico.md): prompt reutilizable para generar (con un asistente de IA) un reporte en Streamlit, con variables para definir la base de datos, las tablas y el tipo de reporte (ventas, recursos humanos, etc.).
- [`codigo/`](codigo/): implementación base en Python del reporte.
  - `requirements.txt`: dependencias del proyecto.
  - `.env.example`: plantilla de configuración (conexión a la base, tablas, tipo de reporte). Copiar como `.env` y completar.
  - `db.py`: conexión a la base de datos y carga de datos con cache.
  - `app.py`: aplicación de Streamlit (filtros, KPIs, tabla y gráfico).

## Uso rápido

```bash
cd codigo
pip install -r requirements.txt
cp .env.example .env   # completar DB_URL, DB_TABLAS y TIPO_REPORTE
streamlit run app.py
```
