import streamlit as st
from api import fetch_restaurants, fetch_menu_items, fetch_orders_for_user
# o bien llamas a /api/orders/total-sales, etc.

def admin_stats_page():
    st.header("📊 Estadísticas")
    st.write("- Total de ventas, promedio por orden, top productos, top restaurants…")
    # usa requests a tus endpoints de agregación
