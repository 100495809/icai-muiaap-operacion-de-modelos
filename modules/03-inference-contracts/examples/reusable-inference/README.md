# Ejemplo ejecutable — Módulo local de inferencia

La referencia ejecutable está en
`../../solutions/01.02-wine-quality-inference-module/src/model_inference/`.
Carga un clasificador de calidad de vino ya entrenado y procesa un CSV de
muestras nuevas con `uv`. El alumnado trabaja, en cambio, con el *starter* de
la práctica 01.02.

## Mapa del módulo

| Archivo | Responsabilidad |
| --- | --- |
| `contracts.py` | Define y valida las 11 medidas de una muestra y su predicción. |
| `preprocess.py` | Construye y ordena las medidas en el vector del modelo. |
| `inference.py` | Carga el artefacto y predice sobre el vector preparado. |
| `predict_file.py` | Lee CSV, llama a preprocesado e inferencia, y escribe otro CSV. |

## Ejecución

Desde la raíz del repositorio, el artefacto entregado por el profesorado debe
estar en `models/wine_quality_classifier.joblib`; está excluido de Git.

```bash
uv sync
uv run python -m model_inference.predict_file \
  --input assets/03-wine-quality/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

Antes de cambiar el código, ejecuta el contrato automatizado:

```bash
uv run pytest
```
