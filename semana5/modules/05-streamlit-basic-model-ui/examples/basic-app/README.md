# Ejemplo — primera interfaz de modelo

La solución de S5 muestra el recorrido mínimo:

```text
st.form -> collect_values -> InferenceGateway.predict -> render_prediction
```

En S6 esta misma app conservará el formulario, pero la llamada y el resultado
pasarán por `st.session_state`, una máquina de estados y un gateway cacheado.
