# Semana 4 — Serialización y validación de modelos

Objetivo de la semana: convertir el artefacto que la semana 3 cargaba desde un
`.joblib` en un paquete explícito, inspeccionable y ejecutable. El paquete
separa el binario del modelo de un manifiesto JSON y comprueba la compatibilidad
antes de inferir.

La semana continúa el caso de calidad de vino. No se entrena un modelo nuevo ni
se expone todavía una API web: primero hacemos fiable el artefacto local que
después consumirá la interfaz de la semana 5 y la API de las semanas 7–10.

## Secuencia semanal

| Sesión | Foco | Resultado |
| --- | --- | --- |
| 1 | Inspección de artefactos y contrato de empaquetado | Las parejas distinguen binario, metadatos y contrato; completan un manifiesto y prueban qué cambios deben rechazar. |
| 2 | Taller de bundle serializado | Cada pareja implementa guardado/carga, validación de entradas y salidas, CLI y pruebas sin salida parcial sobre el starter. |

## Prácticas y entregable

| Recurso | Uso |
| --- | --- |
| [Lienzo de artefacto](exercises/01-model-packaging/01.01-artifact-contract/problem/01-artefacto-y-manifiesto-alumno.ipynb) | Práctica guiada de la clase 1; no implementa todavía el módulo completo. |
| [Starter del taller](exercises/01-model-packaging/01.02-serializable-inference-module/problem/starter/) | Proyecto incompleto que parte de los contratos y el preprocesado de la semana 3. |
| [Solución docente](solutions/01.02-serializable-inference-module/) | Referencia para el debrief, no se entrega al alumnado antes del cierre. |
| [Ejemplo ejecutable](examples/serializable-model/README.md) | Mapa de responsabilidades y comandos de aceptación. |

El entregable es un directorio de bundle con:

```text
models/wine_quality_bundle/
├── manifest.json       # contrato legible y validable
└── model.joblib        # estimador serializado
```

No se versiona el `.joblib`. Las pruebas crean clasificadores pequeños en
directorios temporales para que la clase sea reproducible sin credenciales ni
descargas.

## Relación con las semanas anteriores

- **Semana 1:** el modelo tiene que llevar evidencia y versión, no ser solo un
  objeto escondido en un notebook.
- **Semana 2:** el bundle vive en una estructura reproducible y sus dependencias
  se declaran con `uv`.
- **Semana 3:** se conserva `WineQualityRequest`, el orden de las once
  características y el comando local de inferencia; esta semana añade un
  manifiesto y una frontera de carga más estricta.
- **Semana 5:** la futura interfaz web consumirá el mismo bundle; no se duplica
  la lógica de carga ni de validación.

## Validación docente

Desde la raíz del repositorio:

```bash
uv run pytest
uv run ruff check modules/04-model-packaging/solutions
uv run ruff format --check modules/04-model-packaging/solutions
```

Para revisar el starter como lo recibe el alumnado:

```bash
cd modules/04-model-packaging/exercises/01-model-packaging/01.02-serializable-inference-module/problem/starter
uv sync
uv run pytest
```

Ese último conjunto de pruebas empieza rojo porque los puntos de extensión del
taller contienen `TODO`; debe quedar verde tras la implementación de la pareja.
