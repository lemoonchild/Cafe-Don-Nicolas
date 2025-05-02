import streamlit as st
from api import get_user_by_email

def login_page():
    st.title("🔒 Don Nicolás – Login")
    email = st.text_input("Correo")
    pwd   = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        user = get_user_by_email(email)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Usuario no encontrado")