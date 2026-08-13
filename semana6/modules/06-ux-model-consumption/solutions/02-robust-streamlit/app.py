"""Adaptador Streamlit para el controlador de UX de la semana 6."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from model_ui.contracts import UiState
from model_ui.controller import PredictionController
from model_ui.gateway import (
    DemoGateway,
    InferenceGateway,
    PackagedBundleGateway,
    UnavailableGateway,
)
from model_ui.telemetry import Telemetry

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


def build_gateway() -> InferenceGateway:
    """Elige bundle real si está configurado y demo en otro caso."""

    bundle_value = os.getenv("MODEL_UI_BUNDLE")
    if not bundle_value:
        return DemoGateway()
    try:
        return PackagedBundleGateway.from_bundle_path(Path(bundle_value))
    except Exception as error:  # noqa: BLE001 - se traduce en la UI
        return UnavailableGateway(str(error))


def collect_values(st: Any) -> tuple[bool, dict[str, float]]:
    """Dibuja el formulario sin conocer la implementación del modelo."""

    values: dict[str, float] = {}
    with st.form("wine_quality_form"):
        st.caption("Caso didáctico: la salida es orientativa y no es una garantía.")
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


def render_state(st: Any, state: UiState) -> None:
    """Renderiza solo estados y view models, nunca excepciones internas."""

    if state.phase == "loading":
        st.info("Validando la muestra y ejecutando el modelo…")
        return
    if state.phase == "error" and state.error:
        st.error(state.error.title)
        st.write(state.error.message)
        st.info(state.error.recovery)
        st.caption(f"Request ID: {state.error.request_id}")
        return
    if state.phase != "success" or state.view is None:
        return

    view = state.view
    st.success(view.quality_label)
    metric_columns = st.columns(3)
    metric_columns[0].metric("Confianza", f"{view.confidence:.0%}")
    metric_columns[1].metric("Latencia", f"{view.latency_ms:.1f} ms")
    metric_columns[2].metric("Nivel", view.confidence_label)
    if view.confidence_level == "low":
        st.warning(view.confidence_message)
    else:
        st.info(view.confidence_message)
    if view.latency_status == "above_target":
        st.warning(view.latency_message)
    else:
        st.caption(view.latency_message)
    with st.expander("Trazabilidad del resultado"):
        st.write(
            {
                "model_version": view.model_version,
                "preprocessing_version": view.preprocessing_version,
                "request_id": state.request_id,
            }
        )


def main() -> None:
    """Construye la pantalla y conserva el controlador entre reruns."""

    try:
        import streamlit as st
    except ModuleNotFoundError as error:
        raise SystemExit(
            "Instala la app con `uv sync --extra app` para ejecutar Streamlit."
        ) from error

    st.set_page_config(page_title="Wine Quality · Operación de Modelos", page_icon="🍷")
    st.title("Inferencia de calidad de vino")
    st.write(
        "Demo de UX para IA: contrato, estado, confianza, latencia y trazabilidad."
    )

    if "telemetry" not in st.session_state:
        st.session_state["telemetry"] = Telemetry()
    if "gateway" not in st.session_state:
        st.session_state["gateway"] = build_gateway()
    if "last_state" not in st.session_state:
        st.session_state["last_state"] = UiState(phase="idle")

    gateway = st.session_state["gateway"]
    telemetry = st.session_state["telemetry"]
    controller = PredictionController(gateway, telemetry=telemetry)
    submitted, values = collect_values(st)
    if submitted:
        with st.spinner("Ejecutando inferencia…"):
            st.session_state["last_state"] = controller.submit(values)

    render_state(st, st.session_state["last_state"])
    st.divider()
    st.subheader("Telemetría de la sesión")
    st.json(telemetry.snapshot().__dict__)
    st.caption("Solo se muestran agregados; no se guardan los valores del formulario.")


if __name__ == "__main__":
    main()
