# Explicación — Módulo de inferencia local

El ejercicio separa responsabilidades para que el mismo modelo pueda usarse
desde otros scripts en el futuro:

```text
contracts.py  valida datos nuevos
preprocess.py construye el vector de características
inference.py  carga el .joblib e invoca predict/predict_proba
predict_file.py conecta CSV, preprocesado e inferencia
```

La frontera comprobable es el comando `python -m model_inference.predict_file`.
