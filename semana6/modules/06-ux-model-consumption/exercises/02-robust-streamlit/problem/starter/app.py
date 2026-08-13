"""Starter de la app Streamlit de la semana 6."""

from __future__ import annotations

from typing import Any

from model_ui.contracts import UiState
from model_ui.controller import PredictionController
from model_ui.gateway import InferenceGateway
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
    """TODO: usa el bundle de MODEL_UI_BUNDLE o el DemoGateway."""

    raise NotImplementedError("TODO: conecta la app al gateway sin inferir aquí")


def collect_values(st: Any) -> tuple[bool, dict[str, float]]:
    """TODO: dibuja los once campos dentro de un formulario Streamlit."""

    raise NotImplementedError("TODO: crea el formulario y devuelve submitted, values")


def render_state(st: Any, state: UiState) -> None:
    """TODO: renderiza idle/loading/success/error sin mostrar excepciones."""

    raise NotImplementedError("TODO: presenta el estado y sus acciones")


def main() -> None:
    """Punto de entrada opcional; la lógica importante debe quedar testeable."""

    try:
        import streamlit as st
    except ModuleNotFoundError as error:
        raise SystemExit(
            "Instala Streamlit con `uv run --with streamlit streamlit run app.py`."
        ) from error

    st.set_page_config(page_title="Wine Quality · S6", page_icon="🍷")
    st.title("Inferencia de calidad de vino")
    if "telemetry" not in st.session_state:
        st.session_state["telemetry"] = Telemetry()
    if "gateway" not in st.session_state:
        st.session_state["gateway"] = build_gateway()
    if "last_state" not in st.session_state:
        st.session_state["last_state"] = UiState(phase="idle")

    submitted, values = collect_values(st)
    if submitted:
        controller = PredictionController(
            st.session_state["gateway"], telemetry=st.session_state["telemetry"]
        )
        st.session_state["last_state"] = controller.submit(values)
    render_state(st, st.session_state["last_state"])


if __name__ == "__main__":
    main()
