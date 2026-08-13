# Starter — Interfaz de consumo robusta

Este es el único proyecto de código que recibe el alumnado. Los TODO están en
`presentation.py`, `controller.py` y `app.py`; el gateway demo, los contratos
de UX y las pruebas base están preparados para que el taller se concentre en
estados, mensajes y observabilidad.

Implementa los TODO siguiendo el orden de la
[práctica](../../README.md). Las pruebas describen el comportamiento público; no
comprueban detalles internos.

El `DemoGateway` devuelve una predicción determinista y no representa un modelo
clínico ni una garantía de calidad. El modo real reutiliza el bundle validado de
S4 mediante `PackagedBundleGateway`.
