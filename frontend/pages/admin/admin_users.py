import streamlit as st

def admin_users_page():
    st.header("Gestión de Usuarios")
    st.write("Administra los usuarios registrados en el sistema. Puedes crear nuevos registros, editarlos o eliminarlos según sea necesario.")
    st.subheader("Usuarios registrados:")
    # Aquí iría la lógica para mostrar los usuarios registrados, posiblemente usando un fetch a la API