# Clase 2 — Taller: modelo serializado y ejecutable

Resultado de aprendizaje: implementar un bundle local que guarda y carga un
estimador, valida el manifiesto y las respuestas, y ofrece un comando de
inferencia que no produce salida parcial.

El starter ya contiene los contratos y el preprocesado de la semana 3. La
pareja completa la nueva frontera en artifact.py y predict_file.py, guiada por
las pruebas.

La secuencia es concepto breve y pruebas rojas; construcción acompañada;
extensión autónoma con artefactos y filas inválidas; y debrief comparando
responsabilidades con la solución docente.

## Secuencia del taller — 2 horas

### 1. Arranque y pruebas rojas — 10 min

~~~bash
cd exercises/01-model-packaging/01.02-serializable-inference-module/problem/starter
uv sync
uv run pytest
~~~

Leed los nombres de las pruebas como el contrato público: el bundle debe poder
inspeccionarse, cargarse y consumirse.

### 2. Manifiesto y guardado — 38 min

Implementad ArtifactManifest, create_manifest() y save_model_bundle(). El
manifiesto debe prohibir campos desconocidos y fijar el orden de las once
características. El guardado escribe manifest.json y model.joblib dentro del
directorio del bundle.

### 3. Carga e inferencia — 38 min

Implementad load_model_bundle() e infer_wine_quality(). La carga valida el JSON
antes de deserializar; la inferencia reutiliza WineQualityRequest y
preprocess_wine_request(), y devuelve WineQualityPrediction.

### 4. CLI y errores — 34 min

Implementad el comando:

~~~bash
uv run python -m model_packaging.predict_file \
  --bundle models/wine_quality_bundle \
  --input ../semana3/assets/03-wine-quality/inference_samples.csv \
  --output .tmp/wine_predictions.csv
~~~

Todas las filas se validan antes de abrir el fichero de salida. El comando debe
rechazar una columna extra, una segunda fila inválida y una salida de modelo no
permitida.

### 5. Debrief — 20 min

Comparad la cadena de la semana 3 con la de esta semana:

~~~text
CSV -> contrato -> preprocesado -> bundle validado -> predicción validada -> CSV
~~~

La siguiente extensión será consumir exactamente esta función desde una
interfaz web, sin copiar el código de carga.

## Comprobación final

~~~bash
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
~~~
