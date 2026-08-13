# Datos de apoyo — Semana 6

La interfaz reutiliza las once características y las cinco muestras de
`../../../semana3/assets/03-wine-quality/inference_samples.csv`. No se duplica el CSV
para mantener una única fuente de verdad entre las semanas 3, 4 y 6.

El formulario de demostración usa como valores iniciales la primera muestra del
caso. En modo real, el gateway delega la validación en el contrato Pydantic y
la inferencia del bundle de la semana 4.

La demo también ofrece un gateway determinista para que la clase pueda enseñar
estados de éxito, confianza baja y errores sin depender de un modelo binario ni
de una descarga externa.
