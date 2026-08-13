# Guion docente — Clase 2: taller de primera interfaz

**Resultado:** cada pareja entrega una app Streamlit básica que consume el
gateway de S4 y deja un punto de partida claro para la semana 6.

## Antes de empezar

- Distribuir únicamente `exercises/02-first-streamlit/problem/starter/`.
- Explicar que el gateway y los contratos ya vienen preparados; el foco es la
  pantalla y la llamada básica.
- Mantener cerrada la solución hasta el debrief.
- Ejecutar primero el gateway demo para que nadie dependa de un modelo binario.

## Secuencia de 120 minutos

| Minutos | Hito | Pista | Comprobación |
| ---: | --- | --- | --- |
| 0–10 | Arranque y lectura del starter | “Mira qué datos necesita el gateway.” | La pareja identifica los once campos. |
| 10–30 | Formulario | “Un widget debe corresponder a un campo del contrato.” | Los valores tienen nombres S3/S4. |
| 30–50 | Construcción de valores | “El formulario devuelve una petición, no un vector.” | No aparece preprocesado en `app.py`. |
| 50–75 | Llamada al gateway | “La UI invoca `predict`; no carga `joblib`.” | Se obtiene `PredictionPayload`. |
| 75–95 | Resultado | “Muestra categoría, confianza y versiones.” | La pantalla permite entender la respuesta. |
| 95–110 | Error básico | “No enseñes el traceback completo.” | Bundle ausente produce un mensaje útil. |
| 110–120 | Debrief | “¿Qué se pierde en el siguiente rerun?” | Lista de necesidades para S6. |

## Criterios de aceptación

```bash
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
```

La app se acepta cuando:

- arranca con el gateway demo;
- presenta los once campos del contrato;
- solo llama al modelo al enviar el formulario;
- muestra categoría, confianza y versiones;
- no contiene lógica de `predict`, `predict_proba` ni `joblib.load`;
- deja anotadas dos limitaciones que S6 deberá resolver.
