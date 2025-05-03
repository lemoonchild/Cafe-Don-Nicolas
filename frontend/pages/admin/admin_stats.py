import streamlit as st
from api import fetch_restaurants, fetch_menu_items, fetch_orders_for_user


def admin_stats_page():
    st.header("Estadísticas de Ventas")
    st.write("Aquí puedes ver las estadísticas de ventas por sucursal y por producto.")
    

