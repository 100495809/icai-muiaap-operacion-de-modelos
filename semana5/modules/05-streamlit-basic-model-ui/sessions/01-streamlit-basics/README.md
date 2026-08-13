# Clase 1 — Streamlit básico y primera interfaz

**Duración:** 1 hora de teoría participativa + 1 hora de demo guiada

## Resultado de aprendizaje

La pareja puede construir el recorrido mínimo de una interfaz de inferencia:
formulario → petición validada → gateway → resultado visible.

## Puente desde S3 y S4

1. S3 ya ofrece el contrato de entrada y el módulo local.
2. S4 ya ofrece el bundle y `infer_wine_quality()`.
3. S5 solo añade una capa de interacción humana.

## Contenidos

- qué es una app Streamlit;
- modelo de ejecución y rerun;
- widgets básicos y tipos de datos;
- `st.form` y `st.form_submit_button`;
- columnas, métricas y mensajes;
- adaptación del gateway local a una pantalla;
- límite de S5: todavía no hay estado explícito ni caché avanzada.

El notebook docente muestra el flujo con `DemoGateway`, por lo que se puede
ejecutar sin distribuir un modelo binario.

[Abrir notebook guiado](notebooks/01-streamlit-basics-guiada.ipynb)

[Abrir práctica de diseño](../../exercises/01-ui-form-contract/problem/README.md)
