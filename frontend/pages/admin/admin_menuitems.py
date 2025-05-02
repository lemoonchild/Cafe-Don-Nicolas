import streamlit as st
from api import fetch_restaurants, fetch_menu_items
# similar a admin_restaurants

def admin_menuitems_page():
    st.header("⚙️ CRUD Productos")
    restos = fetch_restaurants()
    sel = st.selectbox("Sucursal", [r["name"] for r in restos])
    if st.button("Ver Productos"):
        r = next(r for r in restos if r["name"]==sel)
        items = fetch_menu_items(r["_id"])
        st.write(items)
    # aquí agregas formularios para crear/editar/eliminar menu‐items
