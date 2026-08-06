# Solución — Módulo local de inferencia de vino

Esta es la referencia completa para el profesorado de la práctica 01.02. No se
entrega al alumnado antes del debrief: ellos trabajan en
`../../exercises/01-local-inference/01.02-wine-quality-inference-module/problem/starter/`.

La solución implementa esta cadena:

```text
CSV -> contracts.py -> preprocess.py -> inference.py -> predictions.csv
```

Desde la raíz del repositorio, con el artefacto docente disponible en
`models/wine_quality_classifier.joblib`:

```bash
uv run python -m model_inference.predict_file \
  --input assets/03-wine-quality/inference_samples.csv \
  --output .tmp/wine_predictions.csv
uv run pytest
```

`scripts/train_instructor_wine_model.py` permite reproducir el artefacto antes
de clase. Los artefactos generados no se suben a Git.
