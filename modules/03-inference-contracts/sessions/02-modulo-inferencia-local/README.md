# Clase 2 — Taller: módulo local de inferencia

Resultado de aprendizaje: construir, ejecutar y probar durante dos horas un
script/módulo local reutilizable con `uv` que cargue un modelo ya entrenado e
infiera sobre filas nuevas de Kaggle.

[Abrir diapositivas del taller](slides/Semana_03_Clase_2_Taller_Modulo_de_Inferencia.pptx)

El entregable de la semana es un módulo local y un comando de línea de comandos.

## Secuencia de taller — 2 horas

### 1. Arranque y pruebas rojas — 15 min

```bash
uv sync
uv run pytest tests/test_inference_cli.py
```

Leed las pruebas como si fuerais consumidores: el comando debe aceptar un CSV,
usar el modelo entregado y producir otro CSV de predicciones.

### 2. Contratos y preprocesado — 30 min

Implementad `WineQualityRequest`, `WineQualityPrediction` y `WineFeatures`.
La creación y el orden del vector de características viven en `preprocess.py`,
nunca en el script de fichero.

### 3. Carga del artefacto y servicio — 25 min

Implementad `load_wine_quality_model()` e `infer_wine_quality()` en
`inference.py`. El cargador debe comprobar que las 11 características declaradas
en el artefacto coinciden con el contrato antes de inferir.

### 4. Script de inferencia por fichero — 30 min

Implementad el comando público:

```bash
uv run python -m model_inference.predict_file \
  --input assets/03-wine-quality/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

El CSV de salida debe incluir `sample_id`, `quality_band`, `confidence`,
`model_version` y `preprocessing_version`.

### 5. Extensión y cierre — 20 min

Resuelve la práctica `../../exercises/01-reusable-inference-api/README.md`:
hacer que el comando falle claramente cuando una fila no cumple el contrato y
asegurar que no deja un fichero de salida parcial. Ejecutad:

```bash
uv run pytest
uv run ruff check src scripts tests
uv run ruff format --check src scripts tests
```
