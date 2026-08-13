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

### Puesta a punto del entorno (20 min)

El assignment de la clase 1 no pide todavía analizar el notebook ni completar
una ficha de riesgos. Cada estudiante instala y verifica `uv`, Git y, si usa
Windows, Git Bash. Después crea una cuenta de Databricks Free Edition y
confirma que puede entrar en su workspace. Los problemas se documentan con el
comando ejecutado y el mensaje de error, sin compartir credenciales.

### Debrief (15 min)

Cada pareja comparte un riesgo que MLflow puede hacer visible y otro que exige
una decisión humana o de gobernanza. La clase 2 usará el entorno ya preparado
para construir la evidencia técnica.
