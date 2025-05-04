import streamlit as st
import requests
import os
from api import fetch_menu_items 
from dotenv import load_dotenv
from datetime import datetime, time

from apiCalls.client.apiClientOrders import ( 
    fetch_orders,
    fetch_restaurant_name_by_id,
    fetch_user_name_by_id
)

load_dotenv() 

API_BASE_URL = os.getenv("API_BASE_URL")

def cliente_orders_page():
    st.header("Mis órdenes")
    st.write("Aquí puedes ver todas tus órdenes y filtrarlas por diferentes criterios.")

    tabs = st.tabs(["📄 Ver", "🔍 Filtrar"])

    with tabs[0]:
        st.subheader("📄 Ver mis órdenes")

        if "order_page" not in st.session_state:
            st.session_state.order_page = 0

        ORDERS_PER_PAGE = 10
        skip = st.session_state.order_page * ORDERS_PER_PAGE

        try:
            user_id = st.session_state.user["_id"]
            orders = fetch_orders(user_id=user_id, limit=ORDERS_PER_PAGE, skip=skip)

            if orders:
                for o in orders:
                    user_name = fetch_user_name_by_id(o.get("user_id", ""))
                    rest_name = fetch_restaurant_name_by_id(o.get("restaurant_id", ""))
                    with st.expander(f"Orden #{o['_id']} - Estado: {o.get('status', '??')}"):
                        st.markdown(f"**Usuario:** {user_name} ({o.get('user_id')})")
                        st.markdown(f"**Restaurante:** {rest_name} ({o.get('restaurant_id')})")
                        st.markdown(f"**Fecha:** {o.get('date', '')[:10]}")
                        st.markdown(f"**Total:** Q{o.get('total', 0):.2f}")
                        st.markdown("**Items:**")
                        for item in o.get("items", []):
                            st.markdown(f"- {item.get('name', '')} x{item.get('quantity')} (Q{item.get('unit_price'):.2f})")
            else:
                st.info("No hay órdenes registradas.")
        except Exception as e:
            st.error(f"Error al obtener órdenes: {e}")

        # Paginación
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Anterior", disabled=st.session_state.order_page == 0):
                st.session_state.order_page -= 1
                st.rerun()
        with col3:
            if len(orders) == ORDERS_PER_PAGE:
                if st.button("Siguiente →"):
                    st.session_state.order_page += 1
                    st.rerun()
        col2.markdown(f"<center>Página {st.session_state.order_page + 1}</center>", unsafe_allow_html=True)

    # === FILTRAR ÓRDENES ===
    with tabs[1]:
        st.subheader("🔍 Filtrar mis órdenes")

        ORDER_STATUSES = ["pendiente", "preparando", "entregado", "cancelado"]

        # Inputs
        user_id = st.session_state.user["_id"]
        st.text_input("ID del usuario", value=user_id, disabled=True)
        restaurant_id = st.text_input("ID del restaurante")
        status = st.selectbox("Estado de la orden", ["Cualquiera"] + ORDER_STATUSES)

        col1, col2 = st.columns(2)
        with col1:
            date_min = st.date_input("Fecha mínima", value=None)
        with col2:
            date_max = st.date_input("Fecha máxima", value=None)

        sort_field = st.selectbox("Ordenar por", ["date", "total", "status"])
        sort_order = st.radio("Orden", ["asc", "desc"], horizontal=True)

        use_limit = st.checkbox("Aplicar límite de resultados", value=True)
        limit = st.slider("Límite de resultados", 1, 1000, 10, disabled=not use_limit)
        skip = st.number_input("Saltar registros", min_value=0, step=1)

        # BOTÓN para aplicar filtros
        if st.button("Aplicar filtros"):
            params = {"sort": sort_field, "order": sort_order}
            if use_limit:
                params["limit"] = limit
                params["skip"] = skip
            if user_id:
                params["user_id"] = user_id
            if restaurant_id:
                params["restaurant_id"] = restaurant_id
            if status != "Cualquiera":
                params["status"] = status
            if date_min:
                start = datetime.combine(date_min, time.min)
                params["dateMin"] = start.isoformat() + "Z"  # → "2023-05-22T00:00:00Z"

            if date_max:
                end = datetime.combine(date_max, time.max)
                params["dateMax"] = end.isoformat() + "Z"  # → "2023-05-22T23:59:59.999999Z"

            response = requests.get(f"{API_BASE_URL}orders", params=params)
            if response.status_code == 200:
                orders = response.json()
                if orders:
                    st.success(f"Se encontraron {len(orders)} órdenes.")
                    for o in orders:
                        user_name = fetch_user_name_by_id(o.get("user_id", ""))
                        rest_name = fetch_restaurant_name_by_id(o.get("restaurant_id", ""))
                        with st.expander(f"Orden #{o['_id']} - Estado: {o.get('status', '??')}"):
                            st.markdown(f"**Usuario:** {user_name} ({o.get('user_id')})")
                            st.markdown(f"**Restaurante:** {rest_name} ({o.get('restaurant_id')})")
                            st.markdown(f"**Fecha:** {o.get('date', '')[:10]}")
                            st.markdown(f"**Total:** Q{o.get('total', 0):.2f}")
                            st.markdown("**Items:**")
                            for item in o.get("items", []):
                                st.markdown(f"- {item.get('name', '')} x{item.get('quantity')} (Q{item.get('unit_price'):.2f})")
                else:
                    st.info("No se encontraron órdenes con los filtros dados.")
            else:
                st.error("Error al consultar órdenes: " + response.text)
