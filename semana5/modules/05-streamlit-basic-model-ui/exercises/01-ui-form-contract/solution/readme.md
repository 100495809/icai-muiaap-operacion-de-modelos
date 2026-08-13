# Solución orientativa — Contrato del formulario

Una solución válida usa `st.number_input` para las once medidas, conserva los
nombres del contrato y coloca todos los widgets dentro de un `st.form`.

El botón debe enviar una sola petición. Cambiar un número puede provocar un
rerun de Streamlit, pero no debe llamar al gateway hasta pulsar “Ejecutar
inferencia”.

El resultado mínimo contiene:

- categoría (`quality_band`);
- confianza como dato orientativo;
- `model_version`;
- `preprocessing_version`.

Limitaciones deliberadas de S5:

- el resultado no se conserva mediante `st.session_state`;
- la carga del gateway no está cacheada de forma explícita;
- no hay una máquina de estados ni telemetría detallada.

Esas limitaciones son el punto de partida de S6.
