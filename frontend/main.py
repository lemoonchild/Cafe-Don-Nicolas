import streamlit as st
from pages.login import login_page
from pages.cliente_restaurants import cliente_restaurants_page
from pages.cliente_orders import cliente_orders_page
from pages.cliente_reviews import cliente_reviews_page
from pages.admin_restaurants import admin_restaurants_page
from pages.admin_menuitems import admin_menuitems_page
from pages.admin_orders import admin_orders_page
from pages.admin_stats import admin_stats_page

st.set_page_config(page_title="Don Nicolás App", layout="wide")

if "user" not in st.session_state:
    login_page()
else:
    user = st.session_state.user
    st.sidebar.write(f"👤 {user['name']} ({user['role']})")
    if user["role"] == "cliente":
        choice = st.sidebar.radio("Cliente", ["Restaurantes","Mis Pedidos","Dejar Reseña"])
        if choice == "Restaurantes":    cliente_restaurants_page()
        if choice == "Mis Pedidos":     cliente_orders_page()
        if choice == "Dejar Reseña":    cliente_reviews_page()
    else:
        choice = st.sidebar.radio("Administrador", ["Gestionar Restaurantes","Gestionar Productos","Ver Órdenes","Estadísticas"])
        if choice == "Gestionar Restaurantes":  admin_restaurants_page()
        if choice == "Gestionar Productos":     admin_menuitems_page()
        if choice == "Ver Órdenes":             admin_orders_page()
        if choice == "Estadísticas":            admin_stats_page()

    if st.sidebar.button("Cerrar sesión"):
        del st.session_state.user
        st.experimental_rerun()
