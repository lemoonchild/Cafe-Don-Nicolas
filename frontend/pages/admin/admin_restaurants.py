import streamlit as st
from api import fetch_restaurants
# (Puedes agregar aquí formularios de POST/PUT/DELETE usando requests)

def admin_restaurants_page():
    st.header("⚙️ CRUD Restaurantes")
    restos = fetch_restaurants()
    for r in restos:
        with st.expander(r["name"]):
            st.write(r)
            # aquí botones para editar/eliminar
    st.write("---")
    st.subheader("Crear Nuevo Restaurante")
    # st.text_input, st.button -> POST /api/restaurants
