# Explicación — Del contrato de S4 al formulario

La práctica no cambia el modelo. Decide cómo representar en una pantalla los
once campos de `WineQualityRequest` y cómo conservar la forma del
`PredictionPayload`.

La clave es separar:

```text
label humano -> nombre de contrato -> tipo/rango -> valor enviado
```

En S5 se diseña el formulario. En S6 se estudiará qué parte de esa información
debe sobrevivir a los reruns de Streamlit.
