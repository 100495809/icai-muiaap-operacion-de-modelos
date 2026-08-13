# Práctica 01 — Diseñar el contrato UX de la inferencia

**Modalidad:** parejas · **Duración:** 45–60 minutos

## Objetivo

Diseñar antes de programar la experiencia que consumirá el bundle de S4. La
pareja debe convertir los riesgos de S1 y los contratos de S3/S4 en estados,
mensajes y criterios observables.

## Material de partida

- [Notebook del alumnado](01-ux-y-estados-alumno.ipynb).
- [Manifiesto de ejemplo de S4](../../../../../../semana4/assets/04-model-packaging/manifest_example.json).
- La salida de S3/S4: `quality_band`, `confidence`, `model_version` y
  `preprocessing_version`.

## Entrega

Completad el notebook o una tabla equivalente con:

| Caso | Estado | Qué ve la persona | Acción | Evidencia técnica |
| --- | --- | --- | --- | --- |
| Pantalla inicial | `idle` | Formulario y alcance didáctico | Completar campos | Ninguna petición enviada |
| Petición en curso | `loading` | Progreso y control deshabilitado | Esperar o cancelar | Inicio de latencia |
| Resultado con confianza baja | `success` | Resultado orientativo y aviso de revisión | Revisar, no concluir | Confianza y versiones |
| Campo inválido | `error` | Qué corregir | Modificar entrada | Código estable y `request_id` |
| Bundle no disponible | `error` | Servicio no disponible | Avisar al responsable | Error sin traceback |
| Respuesta lenta | `success` | Resultado + señal técnica de latencia | Revisar operación | Latencia agregada |

Una respuesta lenta no se convierte automáticamente en un error: si la salida
cumple el contrato, conserva `success` y añade la señal
`latency_status=above_target`. Los errores (`invalid_input`,
`artifact_unavailable`, `timeout` y `prediction_error`) tienen un código y una
recuperación distintos.

Además, entregad:

1. umbrales justificados para confianza baja/media/alta;
2. tres frases que la interfaz no debe mostrar, por ejemplo “garantizado”;
3. tres criterios de aceptación verificables;
4. un ejemplo de dato que nunca debe entrar en la telemetría.

## Pistas

- No confundas `confidence` con probabilidad de que una decisión humana sea
  correcta.
- `model_version` y `preprocessing_version` ayudan a investigar un resultado,
  pero no son instrucciones para la persona usuaria.
- El mensaje de error debe decir qué hacer después; el detalle técnico queda
  en logs controlados, no en la pantalla.
- Diseña la transición `loading → error` aunque la excepción ocurra antes de
  llamar al modelo.

## Comprobación

La tabla debe permitir que otra pareja implemente la clase 2 sin inventar
estados, textos ni umbrales. La solución orientativa está en
[`solution/readme.md`](../solution/readme.md).
