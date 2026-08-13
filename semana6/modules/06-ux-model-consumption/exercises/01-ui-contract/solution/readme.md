# Solución orientativa — Contrato UX de inferencia

Una solución válida conserva cuatro estados y no convierte la confianza en una
decisión:

| Estado | Mensaje | Acción |
| --- | --- | --- |
| `idle` | “Introduce una muestra para ejecutar la inferencia didáctica.” | Completar el formulario. |
| `loading` | “Validando la muestra y ejecutando el modelo…” | Esperar; deshabilitar el botón. |
| `success` con confianza baja | “Resultado orientativo: requiere revisión.” | Revisar la entrada y no usarla como garantía. |
| `success` con confianza media/alta | “Resultado orientativo; la confianza describe la salida del modelo.” | Consultar versiones y contexto antes de usarlo. |
| `error` de entrada | “Revisa los campos marcados.” | Corregir el contrato. |
| `error` de bundle/backend | “No se pudo ejecutar el modelo.” | Reintentar o avisar al responsable técnico. |

Los umbrales de referencia del taller son `< 0.60` para confianza baja,
`0.60–<0.85` para media y `≥ 0.85` para alta. Son una política de UX, no una
validación clínica ni una métrica de calidad del modelo.

La latencia por encima de 300 ms conserva el estado `success` si la salida es
válida y se comunica con `latency_status=above_target`; no se mezcla con los
errores de contrato, bundle o backend.

La telemetría mínima contiene `requests_total`, éxitos, errores por código,
latencias y versiones. No contiene las once características, el CSV completo,
identificadores personales ni texto libre.
