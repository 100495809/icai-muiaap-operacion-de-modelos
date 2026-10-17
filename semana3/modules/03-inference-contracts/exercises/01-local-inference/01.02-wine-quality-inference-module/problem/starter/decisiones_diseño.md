## Decisiones de diseño

### 1. Mantener un orden fijo para las características

He decidido guardar los nombres de las características en `FEATURE_NAMES` como en la 3.1, y usar ese orden al construir el vector de entrada del modelo. Así se evita depender del orden en el que aparezcan las columnas del CSV y se evita que cada csv pueda generar un orden distinto de las características.

### 2. Validar todas las filas antes de crear el archivo de salida

Las predicciones se guardan primero en memoria y el archivo de salida solo se abre después de leer y generar una predicción para todas las filas del archivo de entrada. Por lo que si una fila es inválida, el programa no crea un CSV de salida con datos incompletos.