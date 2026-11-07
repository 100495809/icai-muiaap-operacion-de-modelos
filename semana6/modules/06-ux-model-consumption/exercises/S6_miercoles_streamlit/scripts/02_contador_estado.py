import streamlit as st
st.title("Contador con estado")
# sesion state es una variable propia de streamlit que permite guardar el estado de la app entre interacciones
if "count" not in st.session_state:
    st.session_state.count = 0
if st.button("Sumar"):
    st.session_state.count += 1
st.metric("Cuenta", st.session_state.count)
