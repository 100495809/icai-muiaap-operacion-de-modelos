# Guion de diapositivas — Sesión 01

1. **Título y resultado de aprendizaje:** de un notebook a una evidencia
   operable.
2. **Caso heredado:** clasificación cardiovascular con `data/raw/heart.csv`;
   uso sólo didáctico, nunca clínico.
3. **Prototipo frente a operación:** usuarios, fallo, cambios de datos, coste,
   privacidad y responsabilidad.
4. **Ciclo de un modelo clásico:** datos → candidatos → gate de validación →
   test reservado → Registry/alias → despliegue → monitorización.
5. **Ciclo de una aplicación con agente:** entrada → ruta/herramientas → LLM →
   respuesta → traza → evaluación.
6. **MLflow como evidencia:** experimento, run, input/digest, métrica,
   parámetro, artefacto, modelo/firma, versión/alias, traza y evaluación.
7. **Riesgos iniciales del caso:** uso clínico indebido, sesgo/representatividad,
   secreto en logs, respuesta no fundamentada y coste/latencia.
8. **Selección sin contaminar test:** gate de recall, ranking y decisión
   auditable; qué hacer si ningún candidato pasa.
9. **Registrar no es desplegar:** versión gobernada y alias `Champion` frente a
   proceso de serving.
10. **API local gratuita:** cargar el pickle, contrato HTTP, health, 200/400,
    telemetría y apagado; por qué localhost no es producción.
11. **Puente a la práctica:** ficha inicial, evidencia esperada en Experiments
    y Catalog Explorer, y límites de Free Edition.
