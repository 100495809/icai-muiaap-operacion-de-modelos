import streamlit as st
st.title("Contador con callback")
# Callback es una funcion que llama a otra funcion cuando ocurre un evento, en este caso cuando se hace click en el boton
if "count" not in st.session_state:
    st.session_state.count = 0
def increment():
    st.session_state.count += 1
st.button("Sumar", on_click=increment)
st.metric("Cuenta", st.session_state.count)

# st.text_input("Name", key="name")

# def set_name():
#     st.session_state.name = st.session_state.name_input
