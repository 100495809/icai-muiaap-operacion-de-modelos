import streamlit as st

from model import predict


# Configuración básica de la página: título de la pestaña, icono y distribución.
st.set_page_config(
    page_title="Predictor de abandono de clientes",
    page_icon=":chart_with_downwards_trend:",
    layout="wide",
)

# La sidebar sirve para colocar información auxiliar y controles secundarios.
with st.sidebar:
    st.header(":bar_chart: Sobre esta demo")
    st.write(
        "Introduce los datos de un cliente y obtén una predicción "
        "explicable en unos segundos."
    )
    # st.warning(
    #     "Es una regla docente sintética. El score no es una probabilidad calibrada."
    # )
    # st.divider()
    simulate_error = st.checkbox("Simular un error de validación")

# El layout principal se divide en dos columnas: entrada y resultado
header_left, header_right = st.columns([3, 1])
with header_left:
    st.title("Predictor de abandono de clientes")
    st.caption("Herramienta de apoyo para identificar perfiles que podrían darse de baja.")
with header_right:
    st.metric("Tipo de modelo", "Sintético", help="Modelo creado para fines educativos.")

st.divider()

input_column, result_column = st.columns([1, 1.25], gap="large")

# st.form agrupa los campos y evita recalcular el modelo en cada cambio
with input_column:
    with st.container(border=True):
        st.subheader(":memo: Perfil del cliente")
        st.caption("Completa los datos de entrada para ejecutar la predicción.")

        with st.form("churn_form"):
            tenure = st.number_input(
                "Antigüedad (meses)",
                min_value=0,
                max_value=120,
                value=2,
                step=1,
            )
            spend = st.number_input(
                "Gasto mensual (€)",
                min_value=0.0,
                max_value=300.0,
                value=95.0,
                step=1.0,
            )
            calls = st.number_input(
                "Llamadas a soporte",
                min_value=0,
                max_value=20,
                value=4,
                step=1,
            )
            annual = st.checkbox("Tiene contrato anual")

            submitted = st.form_submit_button(
                ":mag: Calcular riesgo",
                type="primary",
                use_container_width=True,
            )

    st.caption("Las cuatro variables se envían al modelo únicamente al pulsar el botón.")

# Estas variables guardan el resultado de la inferencia de esta ejecución
result = None
error = False
if submitted:
    # Los nombres del diccionario deben coincidir con los argumentos de predict()
    values = {
        "tenure_months": tenure,
        "monthly_spend_eur": spend,
        "support_calls": calls,
        "has_annual_contract": annual,
    }
    if simulate_error:
        values["tenure_months"] = -1

    try:
        # Llamamos al modelo una sola vez, cuando el usuario envía el formulario
        result = predict(**values)
    except ValueError:
        # El modelo utiliza ValueError para avisar de datos fuera del contrato
        error = True

# El panel derecho muestra un estado inicial, un error o el resultado calculado
with result_column:
    with st.container(border=True):
        st.subheader(":dart: Resultado")

        if error:
            st.error(
                ":warning: No se pudo calcular el riesgo. "
                "Revisa los datos e inténtalo de nuevo."
            )
        elif result:
            st.caption("Predicción generada para el perfil introducido.")

            result_columns = st.columns(3)
            result_columns[0].metric(
                "Predicción",
                result["label"],
                delta="Atención" if result["will_churn"] else "Favorable",
                delta_color="inverse" if result["will_churn"] else "normal",
            )
            result_columns[1].metric("Score", f"{result['risk_score']:.2f}")
            result_columns[2].metric("Riesgo", f"{result['risk_score']:.0%}")

            # Los mensajes de estado ayudan a interpretar rápidamente el resultado
            if result["will_churn"]:
                st.warning(":warning: Se recomienda valorar una acción de retención.")
            else:
                st.success(":white_check_mark: El perfil presenta un riesgo bajo de abandono.")

            st.progress(
                result["risk_score"],
                text=f"Riesgo estimado: {result['risk_score']:.0%}",
            )
            st.divider()
            st.markdown("**Explicación del modelo**")
            st.write(result["explanation"])
        else:
            # Este mensaje se muestra antes de realizar la primera predicción
            st.info(":information_source: El resultado aparecerá aquí después de calcular el riesgo.")
            st.markdown(
                "La predicción combina antigüedad, gasto mensual, llamadas a soporte "
                "y tipo de contrato."
            )

# Expander permite ocultar información adicional y mantener la interfaz limpia
if result:
    with st.expander("¿Cómo se calcula la predicción?"):
        st.write(
            "La regla aumenta el riesgo cuando el cliente lleva pocos meses, "
            "gasta mucho, contacta varias veces con soporte o no tiene contrato anual."
        )
        st.write(
            "También reduce el riesgo cuando el cliente tiene una antigüedad alta "
            "o un contrato anual."
        )

st.divider()
st.caption("Ejemplo educativo de Streamlit · Modelo de churn sintético")
