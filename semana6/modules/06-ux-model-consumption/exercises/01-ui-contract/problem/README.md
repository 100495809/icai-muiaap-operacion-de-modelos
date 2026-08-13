# Práctica 01 — Analizar y diseñar el estado de la app de S5

**Modalidad:** parejas · **Duración:** 45–60 minutos

## Objetivo

Partir de la app básica de S5 y decidir qué debe persistir entre reruns, qué
evento provoca cada transición y qué debe ver la persona mientras se sirve una
predicción.

No rediseñéis el formulario de S5. El trabajo es especificar su evolución.

## Material

- [Notebook del alumnado](01-estado-streamlit-alumno.ipynb).
- Vuestra app de S5 o la [solución base de S5](../../../../../../semana5/modules/05-streamlit-basic-model-ui/solutions/02-first-streamlit/README.md).
- Contrato de salida y manifiesto de [S4](../../../../../../semana4/assets/04-model-packaging/manifest_example.json).

## Entrega

### 1. Estado de sesión

Completad una tabla:

| Clave | Tipo | Se conserva entre reruns | Se puede limpiar | Por qué |
| --- | --- | --- | --- | --- |
| `last_state` | TODO | TODO | TODO | TODO |
| `telemetry` | TODO | TODO | TODO | TODO |
| valores completos del formulario | TODO | TODO | TODO | TODO |

### 2. Máquina de estados

| Estado | Evento de entrada | Qué se muestra | Acción permitida | Evidencia |
| --- | --- | --- | --- | --- |
| `idle` | Inicio/limpiar | TODO | TODO | TODO |
| `loading` | Enviar formulario | TODO | TODO | TODO |
| `success` | Payload válido | TODO | TODO | TODO |
| `error` | Excepción controlada | TODO | TODO | TODO |

Una respuesta con salida válida pero latencia superior a 300 ms permanece en
`success` y añade una señal técnica de lentitud.

### 3. Caché y UX

Justificad:

- qué función se protege con `st.cache_resource`;
- qué dato no debe cachearse como recurso;
- qué mensaje se muestra con confianza baja;
- qué recuperación se ofrece para bundle ausente, timeout y error de entrada.

## Criterios de aceptación

- el diseño parte explícitamente de una limitación de S5;
- no introduce una segunda definición del contrato de S4;
- las transiciones tienen eventos y acciones observables;
- distingue estado de sesión, recurso cacheado y datos de una petición;
- otra pareja puede implementar el taller sin inventar estados.
