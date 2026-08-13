# Guion docente — Clase 2: taller de bundle serializado

**Resultado:** cada pareja entrega un bundle de modelo que puede guardarse,
cargarse y consumirse desde un CLI; las entradas y salidas se validan y una
fila inválida no deja un CSV parcial.

El starter ya contiene los contratos y el preprocesado acordados en la semana
3. El trabajo nuevo está concentrado en `artifact.py` y `predict_file.py`.

## Antes de empezar

- Distribuir solo
  `exercises/01-model-packaging/01.02-serializable-inference-module/problem/starter/`.
- Pedir que cada pareja cree una copia propia y trabaje con `.tmp/` local.
- Explicar que los tests generan un `DummyClassifier`; no hace falta descargar
  un dataset ni recibir un modelo grande para comprobar la interfaz.
- Si se quiere ejecutar sobre el caso completo, colocar el artefacto de la
  semana 3 y usar después el comando de migración de la solución docente.

## Secuencia de 120 minutos

| Minutos | Hito | Trabajo de las parejas | Comprobación docente |
| --- | --- | --- | --- |
| 0–10 | Leer el starter y ejecutar la suite roja. | Identifican qué funciones son nuevas y qué piezas vienen de la semana 3. | Nadie vuelve a implementar el orden de características. |
| 10–28 | Definir `ArtifactManifest`. | Implementan campos estrictos, versiones, características y etiquetas de salida. | Un manifiesto extra o incompatible falla antes de cargar el modelo. |
| 28–48 | Implementar `save_model_bundle()`. | Escriben `manifest.json` y `model.joblib`; comprueban el estimador y el formato. | El directorio es inspeccionable y no depende del notebook. |
| 48–68 | Implementar `load_model_bundle()`. | Leen y validan el manifiesto antes de deserializar el objeto. | Se rechazan archivos ausentes, metadatos inválidos y estimadores incompatibles. |
| 68–86 | Validar la respuesta. | Completan `infer_wine_quality()` y hacen cumplir etiqueta, confianza y versiones. | Una salida desconocida no alcanza el CSV. |
| 86–105 | Completar el CLI. | Leen todas las filas, validan, infieren y escriben al final de forma atómica. | Una segunda fila inválida no deja salida parcial. |
| 105–115 | Extensión autónoma. | Añaden un caso de manifest corrupto o un campo de entrada fuera de rango. | El error explica qué debe corregirse. |
| 115–120 | Intercambio y debrief. | Otra pareja ejecuta el comando y revisa el bundle. | `pytest`, Ruff y el comando CLI pasan. |

## Pistas graduadas

1. **Manifiesto:** fija primero las invariantes que escribiste en el lienzo; no
   las infieras desde el estimador ya cargado.
2. **Carga:** un `joblib.load()` exitoso no demuestra que el artefacto sea
   compatible con este preprocesado.
3. **Salida:** valida la predicción con el mismo enfoque que usaste para la
   entrada; una etiqueta arbitraria no es una respuesta válida.
4. **CLI:** guarda las predicciones en memoria y abre el fichero de salida solo
   después de validar todas las filas.

## Comando de aceptación

Desde la copia del starter:

```bash
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
uv run python -m model_packaging.predict_file \
  --bundle models/wine_quality_bundle \
  --input ../semana3/assets/03-wine-quality/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

La ruta relativa del CSV puede sustituirse por una ruta absoluta en el aula. El
debrief compara responsabilidades y decisiones con
`solutions/01.02-serializable-inference-module/`, no entrega una solución antes
de que el grupo haya hecho pasar sus pruebas.
