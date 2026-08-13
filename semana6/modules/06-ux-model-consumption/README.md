# Semana 6 — UX para consumo de modelos

Objetivo de la unidad: convertir una inferencia correcta en una experiencia de
consumo comprensible y operable. La interfaz debe hacer visible cuándo está
trabajando, qué resultado recibió, qué incertidumbre acompaña a la predicción,
cuánto tardó y qué puede hacer la persona ante un fallo.

## Principio de diseño

La interfaz no es otra capa de inferencia. El flujo conserva las fronteras de
S3 y S4:

```text
formulario -> request values -> gateway -> PredictionPayload -> vista UX
                                      \-> model_version/preprocessing_version
```

El gateway en modo empaquetado usa `load_model_bundle()` e
`infer_wine_quality()` de la solución de la semana 4. La app no accede al
estimador ni reconstruye el vector de once características. En S7, el mismo
contrato `InferenceGateway` puede implementarse con un cliente HTTP.

## Secuencia semanal

| Sesión | Foco | Resultado |
| --- | --- | --- |
| 1 | UX para IA, errores, latencia, estados y confianza | La pareja entrega una matriz de estados y reglas de comunicación que respetan el contrato y los riesgos del caso. |
| 2 | Taller de interfaz robusta | La pareja implementa un controlador probado y una demo Streamlit que consume un gateway local sin duplicar la inferencia. |

## Material

| Recurso | Uso |
| --- | --- |
| [Sesión 1](sessions/01-ux-estados-confianza/README.md) | Conceptos, demo de estados y notebook docente. |
| [Sesión 2](sessions/02-interfaz-robusta/README.md) | Taller de implementación y debrief. |
| [Práctica 01](exercises/01-ui-contract/problem/README.md) | Diseño de estados y mensajes antes de programar. |
| [Práctica 02](exercises/02-robust-streamlit/README.md) | Starter con TODOs, pruebas y app Streamlit. |
| [Solución docente](solutions/02-robust-streamlit/) | Referencia separada para el debrief. |
| [Ejemplo ejecutable](examples/robust-ui/README.md) | Mapa de componentes y criterios de aceptación. |

## Contratos de UX que se evalúan

- `loading`: la persona sabe que la petición está en curso y no duplica el
  envío accidentalmente;
- `success`: se muestra la categoría, la confianza como señal orientativa, la
  latencia y las versiones del bundle;
- `error`: se muestra un mensaje accionable, un identificador de petición y una
  recuperación posible, sin stack trace ni payload;
- confianza baja: la UI recomienda revisión y nunca dice “seguro”, “garantizado”
  o “diagnóstico”;
- latencia alta: se comunica como señal técnica y se registra como agregado;
- telemetría: solo cuenta peticiones, éxitos, errores, códigos y latencias.

## Relación con el roadmap

S6 prepara la separación entre presentación e inferencia. No introduce HTTP ni
autenticación: esas decisiones pertenecen a S7–S10. El objetivo es que en S7 se
pueda reemplazar el gateway local por un cliente REST sin cambiar la política de
estados ni la forma en que la interfaz comunica errores.
