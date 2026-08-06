# Semana 3 — Inferencia y contratos

Objetivo de la semana: separar entrenamiento, modelo e inferencia en un módulo
local reutilizable. Se recibe un modelo ya entrenado y se construye una frontera
de inferencia con contratos explícitos y `uv`.

El caso consiste en clasificar la calidad de una muestra de vino tinto a partir
de once mediciones físico-químicas. No recomienda productos ni sustituye una
evaluación sensorial: es un caso docente para practicar inferencia reproducible.

## Secuencia semanal

| Sesión | Foco | Resultado |
| --- | --- | --- |
| 1 | Inferencia, preprocesado y contratos | Teoría y práctica guiada intercaladas; [diapositivas](sessions/01-inferencia-contratos/slides/Semana_03_Clase_1_Inferencia_y_Contratos.pptx). |
| 2 | Taller learning by doing | Construir y probar un script/módulo local reutilizable con `uv`; [diapositivas](sessions/02-modulo-inferencia-local/slides/Semana_03_Clase_2_Taller_Modulo_de_Inferencia.pptx). |

## Material entregado

| Recurso | Uso |
| --- | --- |
| [Datos de inferencia](../../assets/03-wine-quality/inference_samples.csv) | Cinco muestras de Kaggle sin su etiqueta de calidad. |
| `models/wine_quality_classifier.joblib` | Artefacto preentrenado que distribuye el profesorado y que Git ignora. |
| `scripts/train_instructor_wine_model.py` | Utilidad de reproducción para el profesorado, fuera del taller. |

Las filas proceden del dataset [Red Wine Quality (UCI) de Kaggle](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009), que contiene 1.599 muestras y 11 variables de entrada. La atribución está recogida con la muestra de datos.

## Ejecución

El ejemplo vive en `src/model_inference/`. Una vez que el profesorado ha
colocado el artefacto en `models/wine_quality_classifier.joblib`, ejecutad:

```bash
uv sync
uv run python -m model_inference.predict_file \
  --input assets/03-wine-quality/inference_samples.csv \
  --output .tmp/wine_predictions.csv
uv run pytest
```

El resultado es un CSV con `sample_id`, categoría predicha, confianza y las
versiones de modelo y preprocesado.
