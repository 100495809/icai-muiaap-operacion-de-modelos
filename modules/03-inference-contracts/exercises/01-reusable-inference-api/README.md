# Práctica — Inferencia por fichero con un modelo ya entrenado

Trabajad en parejas. El profesorado proporciona
`models/wine_quality_classifier.joblib` y las filas de
`assets/03-wine-quality/inference_samples.csv`. El entregable es un módulo local
que convierte esas filas en un CSV de predicciones reproducible.

## Objetivo

Implementar el comando:

```bash
uv run python -m model_inference.predict_file \
  --input assets/03-wine-quality/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

El resultado debe contener `sample_id`, `quality_band`, `confidence`,
`model_version` y `preprocessing_version`.

## Restricciones

- No modifiquéis ni reentrenéis el artefacto recibido.
- No leáis CSV ni construyáis vectores en `inference.py`.
- No cambiéis el orden de las once características del modelo.
- Rechazad columnas desconocidas y no generéis un CSV parcial ante una fila
  inválida.
- Conservad la versión del artefacto y del preprocesado junto a cada resultado.

## Parte A — Contrato primero (20 min)

1. Escribid una prueba que procese `red-001` correctamente.
2. Escribid una segunda prueba con todos los datos válidos y una columna extra.
3. Acordad qué mensaje mostrará el comando cuando una fila falle.

## Parte B — Implementación (55 min)

1. Implementad los contratos Pydantic y el vector de características.
2. Validar el formato y versión del artefacto antes de usarlo.
3. Conectad el modelo y el servicio.
4. Implementad `predict_file.py` con `argparse` y los dos CSV.

## Parte C — Verificación (15 min)

```bash
uv run pytest
uv run ruff check src scripts tests
uv run ruff format --check src scripts tests
```

## Extensión opcional

Añadid `--limit N` para inferir sólo las primeras `N` filas. Incluid una prueba
del comando. El límite pertenece a `predict_file.py`, nunca al modelo o al
preprocesado.

## Criterios de entrega

| Evidencia | Peso |
| --- | ---: |
| Contrato claro y validado | 35 % |
| Separación entre CLI, servicio, preprocesado y modelo | 30 % |
| Pruebas del comando local | 25 % |
| Explicación breve de una decisión | 10 % |
