# Explicación — Separar UI, estado y gateway

La app de S6 se organiza alrededor de una frontera pequeña:

```text
Streamlit -> PredictionController -> InferenceGateway -> S4
                 |       |
                 |       └── TelemetrySnapshot
                 └── UiState / PredictionView / UserFacingError
```

`PredictionController` no sabe que existe Streamlit. Esto permite probar
transiciones y errores con una función normal y deja a S7 sustituir el gateway
por un cliente HTTP.

El gateway empaquetado es un adaptador: construye el `WineQualityRequest` de S4,
llama a `infer_wine_quality()` y transforma su salida al payload que la UI
necesita. La UI no conoce `joblib`, `predict_proba` ni el orden de features.
