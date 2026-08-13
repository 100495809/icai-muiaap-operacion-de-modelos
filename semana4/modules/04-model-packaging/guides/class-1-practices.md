# Guion docente — Clase 1: del `.joblib` al contrato del artefacto

**Resultado:** al finalizar, cada pareja puede explicar qué información debe
acompañar a un modelo serializado, ha elegido un formato para cada pieza y ha
escrito las comprobaciones que deben impedir una inferencia incompatible.

La sesión parte del módulo local de la semana 3. No se pide todavía escribir el
módulo completo: la práctica guiada es inspeccionar, diseñar y romper un
artefacto pequeño antes de implementarlo en la clase 2.

## Preparación docente

- Abrir el [notebook guiado](../sessions/01-serializacion-validacion/notebooks/01-serializacion-validacion-guiada.ipynb).
- Tener disponible, si se desea, el artefacto de la semana 3 en
  `models/wine_quality_classifier.joblib`. La demo también puede funcionar con
  el clasificador pequeño que crea el notebook.
- Compartir únicamente el notebook, el [lienzo del alumnado](../exercises/01-model-packaging/01.01-artifact-contract/problem/01-artefacto-y-manifiesto-alumno.ipynb)
  y la muestra de datos de ../semana3/assets/03-wine-quality/.
- Mantener cerrada la carpeta `solutions/` hasta el debrief.

## Secuencia de 120 minutos

| Minutos | Concepto breve | Actividad de las parejas | Evidencia de salida |
| --- | --- | --- | --- |
| 0–10 | Recuperar la frontera de la semana 3: contrato → vector → modelo → salida. | Dibujan qué parte del flujo conoce un `.joblib` y qué parte no. | Identifican que el binario no basta para explicar el orden de columnas. |
| 10–25 | Inspeccionar una serialización como estructura de datos. | Abren el payload legado y enumeran sus claves, tipos y campos ausentes. | Lista de riesgos: versión, preprocesado, etiquetas y orden de características. |
| 25–40 | Elegir formatos con criterio: binario para el estimador y JSON para metadatos. | Clasifican qué guardarían en `model.joblib`, `manifest.json` o en el código. | Tabla de decisiones del lienzo. |
| 40–58 | Manifiesto como contrato verificable. | Completan `schema_version`, `model_version`, `preprocessing_version`, `feature_names`, `output_labels` y `estimator_type`. | Manifiesto propuesto y tres invariantes. |
| 58–78 | Guardar y cargar de forma reproducible. | Siguen el notebook: crear un clasificador pequeño, escribir el bundle y leer el manifiesto antes del binario. | El bundle contiene exactamente `manifest.json` y `model.joblib`. |
| 78–98 | Validación de compatibilidad. | Alteran el orden de `feature_names`, la versión de preprocesado y una etiqueta. Predicen qué error debe aparecer. | Matriz cambio → comprobación → mensaje. |
| 98–112 | Validación de salida. | Sustituyen el estimador por uno que devuelve una etiqueta desconocida o una confianza inválida. | Criterio de rechazo antes de escribir resultados. |
| 112–120 | Debrief y puente al taller. | Cada pareja explica una decisión y un caso de fallo. | Lienzo entregado; orden de implementación para la clase 2. |

## Preguntas de facilitación

- ¿Qué error puede producir una predicción con once números pero con el orden de
  columnas equivocado?
- ¿Por qué `model_version` no sustituye a `preprocessing_version`?
- ¿Qué puede leer una persona sin cargar el binario?
- ¿Qué significa “cargar solo artefactos de confianza” aunque exista un
  `manifest.json`?

## Cierre

La pareja debe salir con esta regla: **un modelo serializado es ejecutable solo
cuando el código valida el contrato que lo acompaña**. La clase 2 convertirá el
lienzo en funciones, un CLI y pruebas.
