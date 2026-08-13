# Clase 2 — Taller: módulo local de inferencia

Resultado de aprendizaje: construir, ejecutar y probar durante dos horas un
script/módulo local reutilizable con `uv` que cargue un modelo ya entrenado e
infiera sobre filas nuevas de Kaggle. El alumnado programa sobre el *starter*;
la referencia queda separada para el debrief docente.

[Abrir diapositivas del taller](slides/Semana_03_Clase_2_Taller_Modulo_de_Inferencia.pptx)

El entregable de la semana es un módulo local y un comando de línea de comandos.
Sigue el [guion docente](../../guides/class-2-workshop.md) para facilitar el
taller sin entregar la solución.

Secuencia: concepto breve al leer las pruebas; construcción acompañada por
parejas sobre el *starter*; extensión autónoma con los casos de error; y
debrief comparando su módulo con la referencia docente. El docente da pistas,
no escribe la implementación de las parejas.

## Secuencia de taller — 2 horas

### 1. Arranque y pruebas rojas — 15 min

```bash
cd ../../exercises/01-local-inference/01.02-wine-quality-inference-module/problem/starter
uv sync
uv run pytest
```

Leed las pruebas como si fuerais consumidores: el comando debe aceptar un CSV,
usar el modelo entregado y producir otro CSV de predicciones.

### 2. Contratos y preprocesado — 30 min

Implementad `WineQualityRequest`, `WineQualityPrediction` y `WineFeatures`.
La creación y el orden del vector de características viven en `preprocess.py`,
nunca en el script de fichero.

### 3. Carga del artefacto e inferencia — 25 min

Implementad `load_wine_quality_model()` e `infer_wine_quality()` en
`inference.py`. El cargador debe comprobar que las 11 características declaradas
en el artefacto coinciden con el contrato antes de inferir.

### 4. Script de inferencia por fichero — 30 min

Implementad el comando público desde `starter/`:

```bash
uv run python -m model_inference.predict_file \
  --input assets/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

El CSV de salida debe incluir `sample_id`, `quality_band`, `confidence`,
`model_version` y `preprocessing_version`.

### 5. Extensión y cierre — 20 min

Haced pasar los cinco tests de la práctica: el comando debe fallar claramente
cuando una fila no cumple el contrato y no dejar un fichero de salida parcial.
Ejecutad:

```bash
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
```

La solución comentada está en
[`../../solutions/01.02-wine-quality-inference-module/`](../../solutions/01.02-wine-quality-inference-module/)
y se usa solo en el debrief.
