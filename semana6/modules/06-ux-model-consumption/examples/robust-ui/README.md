# Ejemplo ejecutable — UI robusta de inferencia

La referencia docente se organiza así:

```text
app.py
  -> PredictionController
       -> InferenceGateway
            -> DemoGateway o bundle de S4
       -> PredictionView / UserFacingError
       -> TelemetrySnapshot
```

## Comportamientos que se deben observar

1. Una petición emite `loading` y termina en `success` o `error`.
2. La vista conserva la categoría, la confianza, la latencia y las versiones.
3. La confianza baja muestra una recomendación de revisión.
4. Un error de contrato no muestra traceback ni los valores introducidos.
5. La telemetría conserva contadores, códigos, latencias y versiones, pero no
   el payload.

El `PackagedBundleGateway` localiza el módulo de S4 y delega en su contrato y
función `infer_wine_quality()`. Esta es la costura que S7 puede implementar con
HTTP sin cambiar `PredictionController` ni la presentación.
