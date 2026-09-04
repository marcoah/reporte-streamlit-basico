# Prompt básico: Reporte en Streamlit

Este prompt sirve como plantilla para pedirle a un asistente de IA (o usarlo vos mismo como guía) que genere un reporte básico en Streamlit conectado a una base de datos. Completá las variables antes de usarlo.

## Variables a definir

- `{BASE_DE_DATOS}`: motor y datos de conexión (ej: PostgreSQL, MySQL, SQL Server, SQLite). Incluir host, puerto, nombre de la base y, si aplica, driver a usar.
- `{TABLAS}`: listado de tablas disponibles y una breve descripción de qué contiene cada una (nombre de tabla, columnas relevantes, relaciones entre tablas si existen).
- `{TIPO_DE_REPORTE}`: qué tipo de reporte se quiere generar (ej: ventas, recursos humanos, inventario, finanzas, marketing, etc.) y qué preguntas de negocio debe responder.

## Prompt

```
Quiero que generes una aplicación en Streamlit que muestre un reporte de {TIPO_DE_REPORTE}.

Conexión a la base de datos:
{BASE_DE_DATOS}

Tablas disponibles:
{TABLAS}

Requisitos del reporte:
1. Conectate a la base de datos usando SQLAlchemy, leyendo los parámetros de conexión desde variables de entorno (no hardcodear credenciales).
2. Permití al usuario filtrar los datos según los campos relevantes para un reporte de {TIPO_DE_REPORTE} (por ejemplo, rango de fechas, categoría, región, etc., según las tablas disponibles).
3. Mostrá al menos:
   - Una tabla con el detalle de los datos filtrados.
   - Dos o tres métricas clave (KPIs) resumidas en la parte superior del reporte.
   - Uno o dos gráficos relevantes para el tipo de reporte (por ejemplo, evolución en el tiempo, comparación entre categorías).
4. Organizá el código de forma simple y legible, separando la conexión a la base de datos, la carga de datos y la interfaz de Streamlit.
5. Agregá manejo básico de errores para la conexión a la base de datos (mostrar un mensaje claro si falla la conexión).
6. Usá `st.cache_data` (o el mecanismo de cache correspondiente) para evitar volver a consultar la base de datos en cada interacción.

El resultado debe ser un código funcional y fácil de adaptar a otras bases de datos, tablas o tipos de reporte en el futuro.
```

## Ejemplo de uso

- `{BASE_DE_DATOS}` → "PostgreSQL, host db.miempresa.com, puerto 5432, base `ventas_db`"
- `{TABLAS}` → "`ventas` (id, fecha, monto, id_cliente, id_producto), `clientes` (id, nombre, region), `productos` (id, nombre, categoria)"
- `{TIPO_DE_REPORTE}` → "ventas, mostrando evolución mensual y ventas por región"

El código base que implementa una primera versión de este prompt está en la carpeta [`codigo/`](../codigo/).
