# Explicación — La app como adaptador fino

La app de S5 tiene una sola responsabilidad: traducir interacción humana a
una llamada al gateway y traducir el payload a una pantalla.

```text
Streamlit -> InferenceGateway -> S4
             PredictionPayload -> pantalla
```

El gateway empaquetado reutiliza el código de S4. Si la app empieza a conocer
el orden del vector, el contenido del `joblib` o `predict_proba`, se ha roto la
frontera que S6 necesitará para añadir estado sin duplicar inferencia.
