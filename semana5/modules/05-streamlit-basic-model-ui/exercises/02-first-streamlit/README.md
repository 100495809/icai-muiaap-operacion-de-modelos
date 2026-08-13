# Práctica 02 — Primera interfaz Streamlit

Esta práctica convierte el contrato de la práctica 01 en una app web mínima.
El alumnado trabaja en `problem/starter/`; la solución docente queda separada.

## Objetivo

Implementar una app que:

- dibuje un formulario con las once features;
- envíe una petición solo al pulsar el botón;
- consuma `InferenceGateway`;
- muestre la categoría, confianza y versiones;
- comunique un error básico sin enseñar el traceback completo.

## Orden recomendado

1. `collect_values()`;
2. `render_prediction()`;
3. `main()` y prueba con el `DemoGateway`;
4. modo bundle con `MODEL_UI_BUNDLE`;
5. nota de transición a S6.

No implementes `predict`, `predict_proba`, `joblib.load` ni el preprocesado en
`app.py`.

## Comandos

```bash
cd problem/starter
uv sync
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

## Evidencia

- test suite verde;
- pantalla con un resultado;
- pantalla o registro de bundle no disponible;
- lista de dos limitaciones que se resolverán en S6.
