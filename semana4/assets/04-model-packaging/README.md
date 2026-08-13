# Assets de la semana 4

La semana 4 reutiliza las cinco filas de inferencia de
../semana3/assets/03-wine-quality/inference_samples.csv. No se duplica el CSV
para mantener una única fuente de verdad entre las semanas 3 y 4.

El artefacto de modelo no se guarda en Git. Para la práctica, los tests crean un
clasificador pequeño; para la demo completa, el profesorado puede migrar el
`.joblib` de la semana 3 con:

```bash
uv run python -m model_packaging.migrate_legacy_artifact \
  --input models/wine_quality_classifier.joblib \
  --output models/wine_quality_bundle
```

El directorio generado contiene un manifiesto legible y un binario serializado,
y está cubierto por la regla `models/` del `.gitignore`.
