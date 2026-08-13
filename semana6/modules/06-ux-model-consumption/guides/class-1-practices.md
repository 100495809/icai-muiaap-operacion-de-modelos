# Guion docente — Clase 1: de la app básica al estado explícito

**Resultado:** cada pareja inspecciona su app de S5 y sale con un diseño
implementable de sesión, caché y transiciones. No reescribe todavía el
formulario.

## Preparación

- Pedir que cada pareja traiga la app de S5 funcionando.
- Tener disponible la solución de S5 como snapshot común si alguna pareja no
  terminó su app.
- Abrir el [notebook guiado](../sessions/01-ux-estados-confianza/notebooks/01-ux-modelo-guiada.ipynb).
- Recordar que S4 sigue siendo la frontera de inferencia y que S6 no copia su
  preprocesado.

## Secuencia de 120 minutos

| Minutos | Acción docente | Actividad | Evidencia |
| ---: | --- | --- | --- |
| 0–15 | Ejecutar una app de S5 | Señalan líneas de formulario, gateway y resultado. | Mapa de S5. |
| 15–30 | Provocar reruns | Predicen qué se pierde y qué se recalcula. | Tabla variable → ciclo de vida. |
| 30–45 | Introducir `session_state` | Diseñan claves mínimas. | `last_state`, `telemetry`. |
| 45–60 | Introducir `cache_resource` | Deciden qué recurso debe cachearse. | Regla de caché. |
| 60–75 | Máquina de estados | Definen eventos y salidas. | Diagrama de transición. |
| 75–90 | Ejecutar demo avanzada | Comparan éxito, error, reintento y limpieza. | Predicción frente a resultado. |
| 90–105 | Confianza y latencia | Redactan copy y umbrales como política de UX. | Mensajes revisados. |
| 105–120 | Preparar taller | Relacionan cada requisito con una función/test. | Orden de implementación. |

## Invariantes

- El formulario de S5 no se duplica ni se rediseña sin motivo.
- El bundle se carga como recurso, no en cada interacción.
- Limpiar la pantalla no borra la telemetría de sesión.
- La confianza no se presenta como certeza.
- Un fallo visible tiene una recuperación y un `request_id`.
