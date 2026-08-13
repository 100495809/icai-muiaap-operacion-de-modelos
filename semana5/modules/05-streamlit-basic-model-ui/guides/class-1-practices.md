# Guion docente — Clase 1: Streamlit básico para servir un modelo

**Resultado:** cada pareja puede explicar el rerun de Streamlit, diseñar un
formulario compatible con S4 y predecir qué ocurre cuando la persona pulsa el
botón.

## Preparación

- Abrir el [notebook guiado](../sessions/01-streamlit-basics/notebooks/01-streamlit-basics-guiada.ipynb).
- Tener a mano el `manifest.json` de S4 y las once features de S3.
- Compartir el [contrato del formulario](../exercises/01-ui-form-contract/problem/README.md).
- No introducir todavía `st.session_state`, `st.cache_resource` ni callbacks
  complejos; forman parte de S6.

## Secuencia de 120 minutos

| Minutos | Concepto | Actividad de las parejas | Evidencia |
| ---: | --- | --- | --- |
| 0–15 | Qué resuelve Streamlit | Comparan CLI de S4 con una pantalla web. | Identifican entrada, acción y salida. |
| 15–30 | Modelo de ejecución | Predicen qué líneas se ejecutan al pulsar un widget. | Distinguen rerun de estado persistente. |
| 30–45 | Widgets y tipos | Relacionan `number_input`, `text`, `button` y el contrato Pydantic. | Tabla widget → tipo → rango. |
| 45–60 | Formularios | Diseñan el momento exacto en que se envía la petición. | No se infiere en cada cambio de campo. |
| 60–75 | Demo de gateway | Ejecutan una predicción determinista. | Payload con categoría, confianza y versiones. |
| 75–95 | Presentación mínima | Deciden qué información mostrar y qué dejar para S6. | Boceto de pantalla. |
| 95–110 | Error básico | Simulan bundle ausente o entrada inválida. | Mensaje comprensible y acción siguiente. |
| 110–120 | Cierre | Preparan el orden del taller. | Contrato de formulario entregado. |

## Mensajes que conviene repetir

- Streamlit vuelve a ejecutar el script; S5 todavía no intenta ocultar ese
  hecho con una máquina de estados.
- El formulario evita enviar una petición por cada cambio de widget.
- La app presenta el resultado de S4; no vuelve a entrenar ni preprocesar.
- La confianza se muestra como dato del modelo, sin prometer certeza.
