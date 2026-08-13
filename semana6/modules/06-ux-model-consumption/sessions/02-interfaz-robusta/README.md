# Clase 2 — Taller: interfaz robusta de inferencia

**Duración:** 2 horas de práctica

## Resultado de aprendizaje

La pareja implementa una interfaz de consumo separando presentación, estado,
telemetría y gateway de inferencia. La solución comunica errores sin detalles
internos, muestra confianza y latencia, conserva las versiones del bundle y
queda preparada para sustituir el gateway local por HTTP en S7.

## Punto de partida

El starter de la práctica 02 ya contiene:

- los nombres de las once características de S3;
- la forma de salida de S3/S4;
- un `DemoGateway` para probar la UX sin descargar un modelo;
- el esqueleto de una app Streamlit;
- pruebas públicas de controlador, vista, errores y telemetría.

La pareja completa `presentation.py` y `controller.py`, y conecta esos
componentes en `app.py`. No debe copiar la carga del `joblib` ni el
preprocesado: el modo empaquetado delega en S4.

## Secuencia del taller — 120 minutos

| Minutos | Hito | Trabajo de las parejas | Comprobación |
| ---: | --- | --- | --- |
| 0–10 | Leer el contrato | Ejecutan la suite roja y leen los nombres de los tests. | Identifican los cuatro seams públicos. |
| 10–30 | Estados y confianza | Implementan `build_prediction_view()` y las políticas de confianza/latencia. | 0.42 pide revisión; 0.74 es orientativa; 0.93 no se presenta como garantía. |
| 30–55 | Errores accionables | Implementan `to_user_facing_error()` y conservan `request_id`. | No se muestra traceback ni payload. |
| 55–85 | Controlador | Implementan `PredictionController.submit()` y emiten `loading` antes del resultado. | Se observan `loading → success` y `loading → error`. |
| 85–105 | Telemetría | Registran agregados de éxito, error y latencia. | El snapshot no contiene valores de las once features. |
| 105–115 | Streamlit | Conectan formulario, gateway y renderizado. | La UI solo orquesta; no contiene `predict` ni `joblib.load`. |
| 115–120 | Debrief | Intercambian la app y revisan estados y mensajes. | `pytest`, Ruff y criterios de aceptación pasan. |

## Comandos de aceptación

Desde una copia del starter:

```bash
uv sync
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
```

Para ejecutar la app, instala Streamlit como dependencia opcional del proyecto
de la semana y lanza `app.py`. Durante la clase puede usarse el gateway demo;
para el bundle real, define `MODEL_UI_BUNDLE` con el directorio de S4.

## Debrief

Preguntas de cierre:

1. ¿Qué tendría que cambiar para que el gateway llamase a una API REST?
2. ¿Qué diferencia hay entre una confianza alta y una decisión autorizada?
3. ¿Qué métrica de latencia registrarías en producción además de la media?
4. ¿Qué datos de la interacción no deben llegar a MLflow ni a la telemetría de
   esta UI?
