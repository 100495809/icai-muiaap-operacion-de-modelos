"""Solución de la primera interfaz Streamlit."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from model_ui.contracts import PredictionPayload
from model_ui.errors import ArtifactUnavailableError
from model_ui.gateway import (
    FEATURE_NAMES,
    DemoGateway,
    InferenceGateway,
    PackagedBundleGateway,
    UnavailableGateway,
)
from model_ui.presentation import confidence_caption, quality_label

FEATURE_FIELDS = (
    ("fixed_acidity", "Fixed acidity", 0.0, 20.0, 7.4),
    ("volatile_acidity", "Volatile acidity", 0.0, 2.0, 0.7),
    ("citric_acid", "Citric acid", 0.0, 2.0, 0.0),
    ("residual_sugar", "Residual sugar", 0.0, 20.0, 1.9),
    ("chlorides", "Chlorides", 0.0, 1.0, 0.076),
    ("free_sulfur_dioxide", "Free sulfur dioxide", 0.0, 100.0, 11.0),
    ("total_sulfur_dioxide", "Total sulfur dioxide", 0.0, 300.0, 34.0),
    ("density", "Density", 0.98, 1.01, 0.9978),
    ("ph", "pH", 2.5, 4.5, 3.51),
    ("sulphates", "Sulphates", 0.0, 3.0, 0.56),
    ("alcohol", "Alcohol", 5.0, 20.0, 9.4),
)

assert tuple(field[0] for field in FEATURE_FIELDS) == FEATURE_NAMES


def build_gateway() -> InferenceGateway:
    """Selecciona el bundle configurado o la demo determinista."""

    bundle_value = os.getenv("MODEL_UI_BUNDLE")
    if not bundle_value:
        return DemoGateway()
    try:
        return PackagedBundleGateway.from_bundle_path(Path(bundle_value))
    except Exception as error:  # noqa: BLE001 - se presenta como estado básico
        return UnavailableGateway(str(error))


def collect_values(st: Any) -> tuple[bool, dict[str, float]]:
    """Dibuja el formulario y devuelve si se ha enviado junto a sus valores."""

    values: dict[str, float] = {}
    with st.form("wine_quality_form"):
        st.caption("Introduce una muestra para ejecutar la inferencia.")
        columns = st.columns(2)
        for index, (name, label, minimum, maximum, default) in enumerate(
            FEATURE_FIELDS
        ):
            with columns[index % 2]:
                values[name] = st.number_input(
                    label,
                    min_value=minimum,
                    max_value=maximum,
                    value=default,
                    key=f"input_{name}",
                )
        submitted = st.form_submit_button("Ejecutar inferencia")
    return submitted, values


def render_prediction(st: Any, prediction: PredictionPayload) -> None:
    """Presenta el payload sin reimplementar la inferencia."""

    st.success(quality_label(prediction))
    columns = st.columns(2)
    columns[0].metric("Confianza", f"{prediction.confidence:.0%}")
    columns[1].metric("Modelo", prediction.model_version)
    st.info(confidence_caption(prediction))
    with st.expander("Trazabilidad"):
        st.write(
            {
                "model_version": prediction.model_version,
                "preprocessing_version": prediction.preprocessing_version,
            }
        )


def main() -> None:
    """Ejecuta la pantalla básica; S6 añadirá estado explícito."""

    try:
        import streamlit as st
    except ModuleNotFoundError as error:
        raise SystemExit(
            "Instala Streamlit con `uv run --with streamlit streamlit run app.py`."
        ) from error

    st.set_page_config(page_title="Wine Quality · S5", page_icon="🍷")
    st.title("Primera interfaz de inferencia")
    st.caption("S5: formulario, gateway y resultado; el estado avanzado llega en S6.")

    gateway = build_gateway()
    submitted, values = collect_values(st)
    if not submitted:
        st.info("Completa el formulario y pulsa “Ejecutar inferencia”.")
        return

    try:
        prediction = gateway.predict(values)
    except (ArtifactUnavailableError, ValueError) as error:
        st.error("No se pudo ejecutar la inferencia.")
        st.info("Revisa los datos o la configuración del bundle.")
        st.caption(f"Detalle para la demo: {error}")
        return

    render_prediction(st, prediction)


if __name__ == "__main__":
    main()
