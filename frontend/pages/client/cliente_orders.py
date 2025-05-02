import streamlit as st
from api import fetch_orders_for_user

def cliente_orders_page():
    st.header("🧾 Mi Historial de Pedidos")
    orders = fetch_orders_for_user(st.session_state.user["_id"])
    if not orders:
        st.info("No tienes pedidos aún.")
    for o in orders:
        st.write(f"- {o['date']} · Q{o['total']} · {o['status']}")
