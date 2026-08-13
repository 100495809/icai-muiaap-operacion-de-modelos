# Activo de clase — calidad de vino

La app de S5 reutiliza el contrato de las semanas 3 y 4. Las muestras se
consultan en:

`../../../semana3/assets/03-wine-quality/inference_samples.csv`

No se copia el CSV para evitar que las semanas evolucionen con datos distintos.
El formulario usa las once columnas del contrato y el gateway empaquetado
delega la validación y el preprocesado en S4.

Para la demo no es necesario versionar un `.joblib`: `DemoGateway` devuelve una
respuesta determinista. El bundle real se configura con `MODEL_UI_BUNDLE`.
