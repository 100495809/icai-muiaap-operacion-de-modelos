# Ejemplo ejecutable — Bundle serializado y validado

La solución docente implementa un paquete de dos piezas:

```text
wine_quality_bundle/
├── manifest.json
└── model.joblib
```

El manifiesto es JSON porque una persona puede inspeccionarlo sin cargar el
estimador. El modelo se serializa con `joblib` porque el caso usa un estimador
de scikit-learn. El cargador valida el manifiesto, comprueba el estimador y solo
entonces deserializa el binario. Como en la semana 3, el binario debe proceder
de una fuente de confianza.

## Responsabilidades

| Archivo | Responsabilidad |
| --- | --- |
| `contracts.py` | Valida entradas y respuestas de calidad de vino. |
| `preprocess.py` | Conserva el orden estable de las 11 características. |
| `artifact.py` | Define el manifiesto, guarda/carga el bundle y valida inferencias. |
| `predict_file.py` | Orquesta CSV → validación → bundle → CSV, sin salidas parciales. |
| `migrate_legacy_artifact.py` | Convierte el payload `.joblib` de la semana 3 al nuevo bundle. |

## Reproducir la demo docente

Desde la raíz:

```bash
uv run pytest
uv run python -m model_packaging.migrate_legacy_artifact \
  --input models/wine_quality_classifier.joblib \
  --output models/wine_quality_bundle
uv run python -m model_packaging.predict_file \
  --bundle models/wine_quality_bundle \
  --input ../semana3/assets/03-wine-quality/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

La migración requiere que exista el artefacto de la semana 3; las pruebas no lo
requieren porque construyen un clasificador pequeño en `tmp_path`.
