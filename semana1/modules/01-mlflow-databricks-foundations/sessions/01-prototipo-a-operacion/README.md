# Sesión 01 — Del prototipo a la operación

**Duración:** 2 horas de teoría guiada

## Resultado de aprendizaje

El alumnado puede identificar qué falta a un notebook para operar un sistema de
IA con responsabilidad: una decisión explícita, evidencia reproducible,
propietario, límites de datos, riesgos y criterios de paso. Distingue además el
ciclo de un modelo clásico del ciclo de una aplicación con agente o LLM.

## Secuencia

### Concepto breve (35 min)

Presenta el contraste prototipo/producción y las unidades de evidencia de
MLflow: experimentos, *runs*, artefactos, trazas y evaluaciones.

### Construcción en directo (35 min)

Revisa el caso histórico de `data/raw/heart.csv` incluido en `semana1/` y uno
de los notebooks anteriores. Identifica rutas frágiles, configuración codificada, una falta de
registro de riesgos y el peligro de interpretar una predicción como consejo
clínico.

### Extensión independiente (35 min)

En parejas, completa el borrador de
[`s01_project_record.yaml`](../../examples/s01_project_record.yaml) con una
decisión, dos límites del dato y tres riesgos con propietario y mitigación.

### Debrief (15 min)

Cada pareja comparte un riesgo que MLflow puede hacer visible y otro que exige
una decisión humana o de gobernanza.
