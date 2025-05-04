import streamlit as st
import os
from pages.utils.login import login_page
from pages.client.cliente_restaurants import cliente_restaurants_page
from pages.client.cliente_orders import cliente_orders_page
from pages.client.cliente_reviews import cliente_reviews_page
from pages.admin.admin_restaurants import admin_restaurants_page
from pages.admin.admin_menuitems import admin_menuitems_page
from pages.admin.admin_orders import admin_orders_page
from pages.admin.admin_stats import admin_stats_page
from pages.admin.admin_reviews import admin_reviews_page
from pages.admin.admin_users import admin_users_page

st.set_page_config(page_title="Café Don Nicolás", layout="wide")

if "user" not in st.session_state:
    login_page()
else:
    user = st.session_state.user
    userid = user["_id"]

    st.sidebar.image("pages/assets/logo_sidebar.png", width=200)
    st.sidebar.write(f"¡Bienvenido {user['name']}!")
    if user["role"] == "cliente":
        choice = st.sidebar.radio("¿Listo para tu prómixo pedido/review?", ["Restaurantes","Mis Pedidos","Dejar o ver Reseña"])
        if choice == "Restaurantes":    cliente_restaurants_page()
        if choice == "Mis Pedidos":     cliente_orders_page()
        if choice == "Dejar o ver Reseña":    cliente_reviews_page()
    else:
        choice = st.sidebar.radio("¿Qué deseas administrar hoy?", ["Gestionar Restaurantes","Gestionar Productos","Gestionar Órdenes", "Gestionar Reviews", "Gestionar Usuarios", "Estadísticas"])
        if choice == "Gestionar Restaurantes":  admin_restaurants_page()
        if choice == "Gestionar Productos":     admin_menuitems_page()
        if choice == "Gestionar Órdenes":       admin_orders_page()
        if choice == "Gestionar Reviews":       admin_reviews_page()
        if choice == "Gestionar Usuarios":      admin_users_page()
        if choice == "Estadísticas":            admin_stats_page()

    if st.sidebar.button("Cerrar sesión"):
        del st.session_state.user
        st.experimental_rerun()
