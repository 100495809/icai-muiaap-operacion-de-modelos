# Clase 1 — Inferencia, preprocesado y contratos

Resultado de aprendizaje: diferenciar entrenamiento, artefacto e inferencia;
definir contratos de entrada y salida, y detectar transformaciones que deben ser
idénticas a las usadas al entrenar.

[Abrir diapositivas de la sesión](slides/Semana_03_Clase_1_Inferencia_y_Contratos.pptx)

El profesor entrega un clasificador de calidad de vino ya entrenado y cinco
muestras sin etiqueta. La primera hora es teoría participativa —cada concepto
incluye una microdecisión de las parejas—; la segunda es una demo local de 60
minutos. No se entrena el modelo ni se implementa una capa web.

## Primera hora — Teoría participativa

### 1. Entrenamiento e inferencia — 15 min

Explica esta cadena:

```text
datos de entrenamiento -> entrenamiento -> artefacto .joblib
fila nueva -> contrato -> preprocesado -> artefacto cargado -> predicción
```

Práctica breve: cada pareja marca qué piezas recibe ya hechas y qué piezas
deberá construir en el taller.

### 2. Contrato de entrada — 20 min

Abrir `assets/03-wine-quality/inference_samples.csv`. En parejas, anotad los
once campos, sus unidades y un rango razonable. Después proponed un campo extra
que el módulo deba rechazar.

Puesta en común: el contrato se expresa en `WineQualityRequest`; las filas con
campos desconocidos o valores no válidos no deben llegar al modelo.

### 3. Preprocesado reproducible — 20 min

Comparad la cabecera original de Kaggle con el contrato Python: el CSV original
usa `pH` y la muestra docente ya adaptada usa `ph`. Ordenad las once medidas
como vector de modelo. Conclusión: adaptar nombres y ordenar columnas son pasos
que deben quedar documentados antes de inferir.

### 4. Síntesis de contratos — 5 min

Cada pareja redacta tres criterios de aceptación para la demo: una fila válida,
una columna desconocida y la presencia de las dos versiones en la salida.

## Segunda hora — Demo local guiada

### 5. Inspeccionar el módulo y el artefacto — 10 min

Recorre el módulo de referencia:

1. `contracts.py`: valida una muestra.
2. `preprocess.py`: crea el vector en el orden entrenado.
3. `inference.py`: carga el artefacto y predice sobre el vector.
4. `predict_file.py`: lee filas, llama a preprocesado e inferencia y escribe
   resultados sin duplicar lógica.

### 6. Ejecutar una inferencia por fichero — 15 min

Ejecutad juntos el script sobre las cinco filas proporcionadas:

```bash
uv run python -m model_inference.predict_file \
  --input assets/03-wine-quality/inference_samples.csv \
  --output .tmp/wine_predictions.csv
```

Abrir el CSV de salida y localizar `model_version` y
`preprocessing_version`.

### 7. Seguir una fila de extremo a extremo — 15 min

Elegid `red-001` y seguidla en pantalla: CSV → `WineQualityRequest` →
`WineFeatures` → `infer_wine_quality()` → CSV de salida. El alumnado señala en
qué punto se aplica cada contrato.

### 8. Provocar y leer un fallo de contrato — 10 min

Añadid una columna inesperada a una copia temporal del CSV y ejecutad de nuevo
el comando. Comparad el error con los criterios de aceptación escritos en la
primera hora y comprobad que no se crea un archivo de salida parcial.

### 9. Debrief — 10 min

Pregunta final: ¿qué cambio podría devolver una predicción sin fallar y, aun
así, ser incorrecto? Respuesta esperada: cambiar unidades, nombres u orden de
características.
