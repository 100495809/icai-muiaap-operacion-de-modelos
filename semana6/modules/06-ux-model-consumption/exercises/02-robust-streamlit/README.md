# Práctica 02 — Interfaz Streamlit robusta

Esta práctica convierte la matriz UX de la clase 1 en un componente reutilizable
y probado. El alumnado trabaja únicamente en
`problem/starter/`; la solución docente está en `solutions/02-robust-streamlit/`.

## Objetivo

Implementar una frontera de consumo que:

- emita `loading` antes de pedir una predicción;
- clasifique la confianza con una política explícita;
- muestre la latencia como señal técnica separada del resultado;
- traduzca fallos técnicos a mensajes accionables;
- conserve `model_version`, `preprocessing_version` y `request_id`;
- registre solo métricas agregadas;
- permita cambiar el gateway local por un cliente HTTP en S7.

## Antes de empezar

1. Lee el [contrato UX de la práctica 01](../01-ui-contract/problem/README.md).
2. Ejecuta la suite roja en `starter/`.
3. Inspecciona el protocolo `InferenceGateway` y el `DemoGateway`.
4. No implementes una nueva función de `predict` ni cargues el `joblib` desde
   Streamlit.

## Orden recomendado

1. `presentation.py`: niveles de confianza, latencia y copy seguro.
2. `errors.py` y `presentation.py`: errores estables, recuperación y
   `request_id`.
3. `controller.py`: transición `loading → success/error`, medición y
   telemetría.
4. `app.py`: formulario, spinner, renderizado y gateway.

## Comandos

```bash
cd problem/starter
uv sync
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
```

La app puede ejecutarse con Streamlit como extensión:

```bash
uv run --with 'streamlit>=1.40,<2.0' streamlit run app.py
```

Sin `MODEL_UI_BUNDLE`, la app usa `DemoGateway`, que permite probar la UX sin
artefacto binario. Con `MODEL_UI_BUNDLE=/ruta/al/wine_quality_bundle`, el
gateway empaquetado delega la carga y la inferencia en el módulo de S4.

## Evidencia que se entrega

- tests verdes;
- captura de resultado normal y confianza baja;
- captura de error de contrato con acción de recuperación;
- versión de modelo/preprocesado y latencia visibles;
- snapshot de telemetría sin valores de las features.
