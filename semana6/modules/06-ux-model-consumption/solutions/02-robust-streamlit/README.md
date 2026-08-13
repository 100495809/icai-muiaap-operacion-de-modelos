# Solución — Interfaz robusta de inferencia

La solución separa la app Streamlit del controlador de UX y del gateway:

- `presentation.py`: copy de calidad, confianza, latencia y errores;
- `controller.py`: transiciones, medición y telemetría;
- `gateway.py`: demo determinista y adaptador del bundle de S4;
- `telemetry.py`: agregados sin payload;
- `app.py`: formulario y renderizado.

## Validación

Desde `semana6/`:

```bash
uv run pytest
uv run ruff check modules/06-ux-model-consumption/solutions
uv run ruff format --check modules/06-ux-model-consumption/solutions
```

La app puede ejecutarse con `uv sync --extra app` y el gateway demo. Para
consumir un bundle real de S4, define `MODEL_UI_BUNDLE` antes de lanzar
Streamlit.
