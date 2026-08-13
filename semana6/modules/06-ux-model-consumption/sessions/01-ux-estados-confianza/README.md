# Clase 1 — UX para IA: estados, errores, latencia y confianza

**Duración:** 1 hora de teoría participativa + 1 hora de demo guiada

## Resultado de aprendizaje

La pareja puede transformar un resultado de S4 en una experiencia que comunica
estado, incertidumbre, latencia, versiones y recuperación ante errores. Puede
justificar cada mensaje con un contrato o riesgo previo, sin presentar la
confianza del clasificador como una garantía.

## Puente desde S1, S3 y S4

1. **S1:** recuperar el riesgo de interpretar una salida didáctica como una
   decisión real y la obligación de no registrar datos sensibles.
2. **S3:** localizar qué parte de la entrada valida el contrato y qué metadatos
   de salida ya existen (`quality_band`, `confidence`, versiones).
3. **S4:** abrir el `manifest.json` y decidir qué identidad del bundle debe ver la
   persona consumidora y cuál no debe resolverse en la capa visual.

La interfaz no arregla un artefacto incompatible: muestra el fallo y orienta a
corregirlo. Tampoco vuelve clínico el caso de vino; es una práctica educativa.

## Secuencia de la sesión

### 1. Concepto y microdecisiones — 60 min

| Minutos | Concepto | Actividad de parejas | Evidencia |
| ---: | --- | --- | --- |
| 0–10 | Resultado válido frente a experiencia válida | Comparan una respuesta correcta, una confianza baja y un error de entrada. | Diferencian “el modelo respondió” de “la UI permite actuar”. |
| 10–25 | Máquina de estados | Diseñan `idle → loading → success/error` y una acción para cada estado. | Matriz con estado, mensaje, acción y métrica. |
| 25–40 | Confianza e incertidumbre | Clasifican 0.42, 0.74 y 0.93; redactan copy que no prometa certeza. | Regla de umbrales y aviso de revisión. |
| 40–50 | Latencia y espera | Deciden qué ocurre si la predicción supera 300 ms. | Indicador técnico separado del resultado. |
| 50–60 | Errores y trazabilidad | Mapean contrato inválido, bundle ausente y backend caído. | Código de error, recuperación y `request_id`. |

### 2. Demo guiada — 60 min

El docente ejecuta
[`01-ux-modelo-guiada.ipynb`](notebooks/01-ux-modelo-guiada.ipynb), que usa un
gateway determinista y recorre éxito, confianza baja, fallo de contrato y
latencia alta. La demo enseña el controlador; no se copia la app completa.

Después, las parejas completan
[`01-ux-y-estados-alumno.ipynb`](../../exercises/01-ui-contract/problem/01-ux-y-estados-alumno.ipynb)
o el [lienzo en README](../../exercises/01-ui-contract/problem/README.md).

## Cierre

Cada pareja entrega:

- una matriz de estados;
- tres mensajes de error accionables;
- una regla de confianza con contraejemplo;
- dos criterios para comprobar que la telemetría no contiene valores de
  entrada.

Estas decisiones son el contrato de diseño que guiará la clase 2.
