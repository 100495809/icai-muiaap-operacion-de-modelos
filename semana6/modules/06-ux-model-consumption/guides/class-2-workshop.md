# Guion docente — Clase 2: taller de interfaz robusta

**Resultado:** cada pareja entrega un controlador probado y una app Streamlit
que consume el mismo gateway local que mañana podrá ser sustituido por HTTP.

## Antes de empezar

- Distribuir únicamente
  `exercises/02-robust-streamlit/problem/starter/`.
- Mantener cerrada la solución hasta el debrief.
- Explicar que las pruebas del starter son la especificación del comportamiento,
  no una implementación para copiar.
- No distribuir un `.joblib`: los tests y el `DemoGateway` permiten trabajar sin
  artefactos binarios. El bundle real de S4 se usa como extensión docente.

## Secuencia de 120 minutos

| Minutos | Hito | Pista que se puede dar | Comprobación |
| ---: | --- | --- | --- |
| 0–10 | Suite roja y seams | “Lee qué observa el consumidor, no cómo se implementa.” | Tests de vista, error, estado y telemetría localizados. |
| 10–30 | Vista de predicción | “Separa nivel de confianza del texto que lo explica.” | Umbrales y copy coherentes. |
| 30–55 | Errores | “El usuario necesita acción y request ID, no stack trace.” | Códigos estables y recuperación. |
| 55–85 | Controlador | “Emite loading antes de llamar al gateway; mide con monotonic clock.” | Transiciones y latencia. |
| 85–105 | Telemetría | “Cuenta, no captures el formulario.” | Snapshot sin features. |
| 105–115 | Adaptador Streamlit | “La app presenta; el gateway infiere.” | No aparece `joblib.load` en `app.py`. |
| 115–120 | Intercambio | “Prueba una entrada inválida en la app de otra pareja.” | Aceptación y debrief. |

## Pistas graduadas

1. **Confianza:** usa una política explícita y prueba los límites, no compares
   strings de forma dispersa.
2. **Errores:** asigna el código antes de construir el texto; el código sirve a
   la telemetría y el texto a la persona.
3. **Estados:** el callback de emisión permite observar `loading` sin acoplar el
   controlador a Streamlit.
4. **Gateway empaquetado:** construye `WineQualityRequest` y llama a
   `infer_wine_quality()` de S4; no copies el preprocesado.

## Criterios de aceptación

```bash
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
```

La app es aceptada si una persona puede distinguir idle/loading/success/error,
entender qué hacer ante un fallo y ver versión, confianza y latencia sin que la
interfaz exponga detalles internos o datos del formulario.
