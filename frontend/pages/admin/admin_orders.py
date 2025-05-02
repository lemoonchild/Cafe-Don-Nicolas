import streamlit as st
from api import fetch_restaurants, fetch_orders_for_user

def admin_orders_page():
    st.header("📦 Órdenes por Sucursal")
    restos = fetch_restaurants()
    sel = st.selectbox("Sucursal", [r["name"] for r in restos])
    if st.button("Ver Órdenes"):
        r = next(r for r in restos if r["name"]==sel)
        orders = fetch_orders_for_user(None)  # tu API admite ?restaurant_id
        orders = [o for o in orders if o["restaurant_id"]==r["_id"]]
        for o in orders:
            st.write(f"- {o['date']} · Q{o['total']} · {o['status']}")
