# Guion docente — Clase 2: refactor avanzado de la interfaz de S5

**Resultado:** cada pareja entrega la app de S5 evolucionada con estado,
caché, máquina de estados y UX operable.

## Antes de empezar

- Distribuir el snapshot de S5 y el starter de S6.
- Aclarar que `collect_values()` ya está resuelto: no es el objetivo del
  taller.
- Mantener cerrada la solución hasta el debrief.
- Ejecutar primero los tests unitarios sin abrir todavía la app.

## Secuencia de 120 minutos

| Minutos | Hito | Pista | Comprobación |
| ---: | --- | --- | --- |
| 0–10 | Comparar diffs S5/S6 | “Busca lo nuevo, no rehagas lo existente.” | Identifican `session`, controller y políticas. |
| 10–25 | Estado de sesión | “`setdefault` protege la sesión.” | Inicialización idempotente y limpieza parcial. |
| 25–40 | Caché de recurso | “Cachea el gateway, no la petición.” | El bundle no se carga por cada rerun. |
| 40–60 | Presentación | “Una etiqueta técnica no es una decisión.” | Confianza/latencia pasan límites. |
| 60–85 | Controlador | “El callback observa `loading`.” | Secuencias `loading → success/error`. |
| 85–105 | App avanzada | “Conecta el formulario de S5 al estado.” | Resultado, retry y clear funcionan. |
| 105–115 | Revisión entre parejas | “Busca payloads en la telemetría.” | No se filtran features. |
| 115–120 | Debrief | “¿Qué cambiaría en S7?” | El gateway queda reemplazable por HTTP. |

## Evidencias obligatorias

- diff o nota que identifique qué se conserva de S5;
- captura de carga, éxito, error y reintento;
- prueba de que el resultado sobrevive a un rerun;
- prueba de que limpiar no borra telemetría;
- tests y lint verdes;
- explicación de qué se cachea y por qué.
