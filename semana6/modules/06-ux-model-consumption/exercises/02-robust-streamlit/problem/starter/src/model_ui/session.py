"""Estado de sesión de Streamlit aislado para poder probarlo sin Streamlit."""

from __future__ import annotations

from collections.abc import MutableMapping

LAST_STATE_KEY = "last_state"
TELEMETRY_KEY = "telemetry"
LAST_VALUES_KEY = "last_values"


def initialize_session_state(
    session_state: MutableMapping[str, object],
) -> None:
    """TODO: crea solo las entradas de sesión que todavía no existan."""

    raise NotImplementedError("TODO: inicializa el estado persistente de S6")


def clear_last_state(session_state: MutableMapping[str, object]) -> None:
    """TODO: vuelve a idle sin perder la telemetría acumulada."""

    raise NotImplementedError("TODO: limpia el último resultado sin borrar telemetría")
