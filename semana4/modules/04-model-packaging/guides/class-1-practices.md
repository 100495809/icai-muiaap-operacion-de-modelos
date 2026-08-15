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
| 0–10 | Recuperar la frontera de la semana 3: contrato → vector → modelo → salida. | Formulan qué necesitarían inspeccionar para saber qué contiene un `.joblib`; no lo dibujan ni lo suponen. | Identifican que el contenido del binario debe comprobarse con evidencia. |
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

## Guion por diapositiva — Clase 1 (21 diapositivas)

Usa el [notebook docente](../sessions/01-serializacion-validacion/notebooks/01-serializacion-validacion-guiada.ipynb)
como única fuente para las demostraciones. El alumnado trabaja en el
[notebook de práctica](../exercises/01-model-packaging/01.01-artifact-contract/problem/01-artefacto-y-manifiesto-alumno.ipynb).
No abras `solutions/` ni muestres `artifact.py` durante la sesión.

| Slide | Tiempo | Contenido que se proyecta | Notebook / acción | Nota de facilitación |
| --- | --- | --- | --- | --- |
| 1 | 0–2 | **Semana 4 — Del modelo al bundle verificable.** Subtítulo: “Serialización, manifiesto y validación”. | Ninguno. | Presenta el objetivo como una continuación de la frontera de inferencia de la semana 3. |
| 2 | 2–5 | `model.joblib` → `wine_quality_bundle/` con `manifest.json` y `model.joblib`; a la derecha: orden de features, versiones y etiquetas permitidas. | Ninguno. | Explica que el bundle no mejora la métrica: hace explícitas las condiciones de uso. |
| 3 | 5–8 | `CSV → contrato → vector → modelo → predicción`. “Esta semana validamos el artefacto antes de cargarlo”. | Ninguno. | Recupera que semana 3 protegía la entrada y la salida. |
| 4 | 8–10 | “Un `.joblib` puede contener información útil, pero no ofrece por sí solo un contrato explícito, legible y versionado”. | Ninguno. | No afirmes que un binario no pueda conservar nombres o clases; el problema es depender de inspeccionarlo para descubrir el contrato. |
| 5 | 10–14 | Árbol del payload legado: `estimator`, `feature_names`, `model_version`. | Docente: notebook guiado, sección **1. Ver qué recibimos de la semana 3**, celda que crea `legacy_payload` e imprime claves, tamaño y campos ausentes. | Pide que observen la salida. No uses una definición teórica en lugar de la evidencia. |
| 6 | 14–16 | Campos todavía implícitos: `schema_version`, `preprocessing_version`, `output_labels`, `estimator_type`. | Ninguno. | Formula: “¿qué fallo evitaría cada campo?”. |
| 7 | 16–28 | **Práctica 1 — Asignar cada dato a un formato.** Tabla: dato / `model.joblib` / `manifest.json` / código. | Alumnado: notebook de práctica, tabla inicial de decisión. | Pide una justificación por fila, no solo marcar una columna. |
| 8 | 28–32 | Puesta en común: binario ejecuta; manifiesto describe; código valida. | Ninguno. | Fija que `feature_names` debe ser visible y comprobable, aunque el estimador pueda retenerlos internamente. |
| 9 | 32–35 | “El manifiesto no sustituye el contrato de entrada; lo complementa.” Contrato de entrada frente a contrato del artefacto. | Ninguno. | Distingue validación de una petición y validación de un bundle. |
| 10 | 35–40 | Las seis claves del manifiesto y la pregunta que responde cada una. | Ninguno. | Presenta `output_labels` como contrato del consumidor, no como una inferencia que se toma del estimador una vez cargado. |
| 11 | 40–55 | **Práctica 2 — Construye un manifiesto mínimo.** Completar `manifest_draft` y mostrarlo como JSON. | Alumnado: notebook de práctica, celda `manifest_draft`. Sustituyen los `TODO`, corrigen `output_labels` y ejecutan `json.dumps`. | No implementan Pydantic ni `ArtifactManifest`: trabajan con un diccionario y toman decisiones justificadas. |
| 12 | 55–58 | Tres invariantes mínimas: orden de `feature_names`, versión de preprocesado y etiquetas permitidas. | Ninguno. | Contrasta sus JSON con estas reglas. Una invariante debe ser comprobable y detener la carga si falla. |
| 13 | 58–62 | Secuencia de carga: leer manifiesto → validar compatibilidad → comprobar archivos → cargar binario → inferir. | Ninguno. | Repite: `joblib.load()` exitoso no prueba compatibilidad. |
| 14 | 62–68 | **Demo — Crear un bundle pequeño.** `DummyClassifier → create_manifest() → save_model_bundle()`. | Docente: notebook guiado, sección **2. Escribir un manifiesto mínimo**, celda que crea `manifest`, llama a `save_model_bundle()` y carga el bundle. | El clasificador pequeño elimina dependencias de descargas y permite centrarse en el formato. |
| 15 | 68–78 | Árbol del bundle y fragmento del `manifest.json`: versiones, features, etiquetas y tipo de estimador. | Mantén proyectada la salida de la misma celda docente. | Muestra solo JSON y árbol; no abras `model.joblib` ni el código de solución. |
| 16 | 78–90 | **Práctica 3 — Anticipar fallos.** Cambios: invertir `density` y `alcohol`; cambiar preprocesado; devolver `unknown`; recibir `ph=99`. | Alumnado: notebook de práctica, sección de entradas inválidas e invariantes. | Pide cuatro predicciones: comprobación, etapa de fallo, mensaje útil y si se genera CSV. |
| 17 | 90–96 | **Demo — El orden incompatible se rechaza.** `feature_names` alterado → validación → error → no inferencia. | Docente: notebook guiado, celda que invierte `feature_names` y valida `manifest_reordered.json`. | Relaciona el error con la primera invariante. El notebook demuestra este caso, no todos los casos de la slide 16. |
| 18 | 96–103 | Tres fronteras: contrato de entrada, contrato del artefacto y contrato de salida. | Docente: notebook guiado, celda que infiere una muestra válida y rechaza `ph=99`. | Señala que la salida `unknown` se implementará y probará en el taller; no afirmes que esta celda ya la demuestra. |
| 19 | 103–112 | **Práctica 4 — Matriz de fallos.** Tabla: cambio / frontera / mensaje útil / ¿se escribe CSV? | Alumnado: completa la matriz en el notebook de práctica o en el lienzo. | Recoge especialmente la decisión: una segunda fila inválida impide publicar una salida parcial. |
| 20 | 112–116 | “Mañana convertimos el contrato en código”: `ArtifactManifest`, guardar, cargar, validar salida y CLI. | Ninguno. | Sitúa el trabajo nuevo en `artifact.py` y `predict_file.py`; se reutilizan contratos y preprocesado de semana 3. |
| 21 | 116–120 | Ticket de salida: una invariante y un fallo que debe impedir escribir un CSV. | Alumnado entrega el enlace/captura de su notebook. | Cierra: “un modelo serializado es ejecutable solo cuando el código valida el contrato que lo acompaña”. |

### Revisión antes de clase

1. Ejecuta de principio a fin el notebook docente. Debe crear sus artefactos
   solo en `.tmp/semana_04_notebook/`.
2. Abre el notebook de práctica y verifica que la celda `manifest_draft` muestra
   los `TODO` y las etiquetas provisionales `low`, `medium`, `high`; esa es la
   evidencia que el alumnado debe corregir en la slide 11.
3. No muestres los valores de la solución antes de la puesta en común de la
   slide 12.
