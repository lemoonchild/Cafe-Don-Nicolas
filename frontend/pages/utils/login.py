import streamlit as st
import os
from api import get_user_by_email


def login_page():

    st.image("pages/assets/logo.png", width=300)

    st.title("¡Bienvenido a Café Don Nicolás!")
    st.subheader("Iniciar sesión")
    st.write("Por favor, ingresa tu correo y contraseña para acceder a tu cuenta.")
    email = st.text_input("Ingresa tu correo electrónico:")
    pwd   = st.text_input("Ingresa tu contraseña:", type="password")
    if st.button("Entrar"):
        user = get_user_by_email(email)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Usuario no encontrado")