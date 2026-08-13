# Guion docente — Clase 1: diseñar una experiencia operable

**Resultado:** cada pareja sale con una matriz de estados que conecta contratos,
riesgos, mensajes y acciones. No implementa todavía la app.

## Preparación

- Abrir el notebook [guiado](../sessions/01-ux-estados-confianza/notebooks/01-ux-modelo-guiada.ipynb).
- Tener a mano el `manifest_example.json` de S4 y recordar las versiones del
  contrato de S3.
- Compartir solo el notebook del alumnado y la práctica 01; la solución se
  mantiene cerrada.
- Si se usa la app de S5, tener un screenshot de un resultado válido y otro de
  un error. Si S5 aún no está disponible, el gateway demo cubre la sesión.

## Secuencia de 120 minutos

| Minutos | Acción docente | Actividad del alumnado | Evidencia |
| ---: | --- | --- | --- |
| 0–15 | Recuperar el riesgo de S1: una salida no es una decisión. | Marcan palabras prohibidas para la confianza. | “No es garantía”, “requiere revisión”. |
| 15–30 | Mostrar `manifest.json`, `model_version` y `preprocessing_version`. | Deciden qué metadatos son útiles para la persona y cuáles son internos. | Tabla de trazabilidad. |
| 30–45 | Dibujar la máquina de estados. | Añaden idle, loading, success y error. | Transiciones y acción de recuperación. |
| 45–60 | Comparar confianza 0.42/0.74/0.93. | Escriben copy de tres niveles. | Mensajes sin sobreafirmación. |
| 60–75 | Ejecutar el gateway demo. | Predicen el estado final y la telemetría. | Hoja de predicciones. |
| 75–95 | Provocar error de contrato y backend. | Redactan mensajes sin traceback. | Código, mensaje, acción y request ID. |
| 95–110 | Medir una latencia artificial. | Deciden cómo distinguir resultado válido y servicio lento. | Regla de latencia. |
| 110–120 | Debrief. | Entregan la matriz y dos invariantes. | Prerequisito para el taller. |

## Invariantes que debe conservar la solución

- El modelo y el preprocesado siguen siendo responsabilidad del gateway de S4.
- `confidence` se muestra como señal, nunca como garantía.
- Un error de contrato se puede corregir desde la UI sin leer una excepción
  técnica.
- La telemetría contiene agregados y versiones, no los valores del formulario.
