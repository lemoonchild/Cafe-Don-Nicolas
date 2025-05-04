import streamlit as st
import requests
import os
from api import fetch_menu_items 
from dotenv import load_dotenv
from datetime import datetime, time

from apiCalls.admin.apiAdminOrders import (
    fetch_orders,
    fetch_restaurant_name_by_id,
    fetch_user_name_by_id,
    create_order,
    create_many_orders,
    fetch_menu_item_by_id
)

load_dotenv() 

API_BASE_URL = os.getenv("API_BASE_URL")

def admin_orders_page():
    st.header("Gestión de Ordenes")
    st.write("Administra las ordenes realizadas por los usuarios. Puedes crear nuevas ordenes, editarlas o eliminarlas según sea necesario.")

    tabs = st.tabs(["📄 Ver", "🔍 Filtrar", "➕ Crear", "✏️ Actualizar", "🗑️ Eliminar"])

    with tabs[0]:
        st.subheader("📄 Ver Órdenes")

        if "order_page" not in st.session_state:
            st.session_state.order_page = 0

        ORDERS_PER_PAGE = 10
        skip = st.session_state.order_page * ORDERS_PER_PAGE

        try:
            orders = fetch_orders(limit=ORDERS_PER_PAGE, skip=skip)
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
        st.subheader("🔍 Filtrar Órdenes")

        ORDER_STATUSES = ["pendiente", "preparando", "entregado", "cancelado"]

        # Inputs
        user_id = st.text_input("ID del usuario")
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

    with tabs[2]:
        st.subheader("➕ Crear Órdenes")

        if "num_order_forms" not in st.session_state:
            st.session_state.num_order_forms = 1

        if st.session_state.get("success_create_order"):
            st.success(st.session_state.success_create_order)
            del st.session_state["success_create_order"]

        orders = []

        for i in range(st.session_state.num_order_forms):
            if f"num_items_{i}" not in st.session_state:
                st.session_state[f"num_items_{i}"] = 1

            with st.expander(f"📝 Orden #{i+1}", expanded=True):
                user_id = st.text_input("ID del Usuario", key=f"user_{i}")
                restaurant_id = st.text_input("ID del Restaurante", key=f"rest_{i}")
                status = st.selectbox("Estado", ["pendiente", "preparando", "entregado", "cancelado"], key=f"status_{i}")
                date = st.date_input("Fecha", key=f"date_{i}")
                order_time = st.time_input("Hora", key=f"time_{i}")

                items = []
                for j in range(st.session_state[f"num_items_{i}"]):
                    st.markdown(f"**🧾 Producto #{j+1}**")
                    product_id = st.text_input("ID del producto", key=f"prod_id_{i}_{j}")

                    # === FETCH automágico si el ID cambia ===
                    last_id_key = f"last_id_{i}_{j}"
                    current_id = product_id.strip()

                    if current_id and st.session_state.get(last_id_key) != current_id:
                        fetched = fetch_menu_item_by_id(current_id)
                        if fetched:
                            st.session_state[f"prod_name_{i}_{j}"] = fetched.get("name", "")
                            st.session_state[f"prod_price_{i}_{j}"] = fetched.get("price", 0.0)
                        st.session_state[last_id_key] = current_id

                    name = st.text_input("Nombre del producto", key=f"prod_name_{i}_{j}")
                    unit_price = st.number_input(
                        "Precio unitario (Q)", min_value=0.0, step=0.5,
                        format="%.2f", key=f"prod_price_{i}_{j}"
                    )
                    quantity = st.number_input("Cantidad", min_value=1, step=1, key=f"prod_qty_{i}_{j}")

                    items.append({
                        "product_id": product_id,
                        "name": name,
                        "quantity": quantity,
                        "unit_price": unit_price,
                    })

                # Botón para agregar ítems
                if st.button("➕ Agregar otro ítem", key=f"add_item_btn_{i}"):
                    st.session_state[f"num_items_{i}"] += 1
                    st.rerun()

                # Botón para eliminar ítem si hay más de 1
                if st.session_state[f"num_items_{i}"] > 1:
                    if st.button("🗑️ Eliminar último ítem", key=f"remove_item_btn_{i}"):
                        st.session_state[f"num_items_{i}"] -= 1
                        st.rerun()

                total = sum(item["quantity"] * item["unit_price"] for item in items)

                # Combinar fecha y hora en ISO format
                order_datetime = datetime.combine(date, order_time)
                iso_date = order_datetime.isoformat() + "Z"

                orders.append({
                    "user_id": user_id.strip(),
                    "restaurant_id": restaurant_id.strip(),
                    "status": status,
                    "date": iso_date,
                    "items": items,
                    "total": total
                })

                # Botón para eliminar esta orden si hay más de 1
                if st.session_state.num_order_forms > 1:
                    if st.button("🗑️ Eliminar esta orden", key=f"delete_order_btn_{i}"):
                        for prefix in ["user", "rest", "status", "date", "time", f"num_items_{i}"]:
                            st.session_state.pop(f"{prefix}_{i}", None)
                        st.session_state.num_order_forms -= 1
                        st.rerun()

        # Botón para agregar otra orden
        if st.button("➕ Agregar otra orden"):
            st.session_state.num_order_forms += 1
            st.rerun()

        # Botón para crear las órdenes (colocado debajo)
        if st.button("Crear orden(es)"):
            valid_orders = [o for o in orders if o["user_id"] and o["restaurant_id"] and o["items"]]
            try:
                if len(valid_orders) == 1:
                    create_order(valid_orders[0])
                    st.session_state.success_create_order = "Orden creada exitosamente."
                else:
                    create_many_orders(valid_orders)
                    st.session_state.success_create_order = f"Se crearon {len(valid_orders)} órdenes."
                st.session_state.num_order_forms = 1
                st.rerun()
            except Exception as e:
                st.error(f"Error al crear órdenes: {e}")

    with tabs[3]:
        st.subheader("✏️ Actualizar Órdenes")

        update_mode = st.radio("Selecciona el método de actualización:", ["Por ID", "Por múltiples IDs"], horizontal=True)

        if update_mode == "Por ID":
            order_id = st.text_input("ID de la orden")

            if order_id and st.button("🔍 Buscar orden"):
                res = requests.get(f"{API_BASE_URL}orders/{order_id}")
                if res.status_code == 200:
                    st.session_state["edit_order_data"] = res.json()
                    st.session_state["edit_order_id"] = order_id
                    st.session_state["edit_order_items"] = res.json().get("items", [])
                else:
                    st.error("No se encontró una orden con ese ID.")

            if "edit_order_data" in st.session_state:
                order_data = st.session_state["edit_order_data"]
                order_id = st.session_state["edit_order_id"]
                items = st.session_state["edit_order_items"]

                user_id = st.text_input("ID del usuario", value=order_data.get("user_id", ""))
                restaurant_id = st.text_input("ID del restaurante", value=order_data.get("restaurant_id", ""))
                status = st.selectbox("Estado", ["pendiente", "preparando", "entregado", "cancelado"],
                    index=["pendiente", "preparando", "entregado", "cancelado"].index(order_data.get("status", "pendiente")))

                parsed_date = datetime.fromisoformat(order_data.get("date", "").replace("Z", ""))
                date = st.date_input("Fecha", value=parsed_date.date())
                order_time = st.time_input("Hora", value=parsed_date.time())

                st.markdown("### ✏️ Editar productos")
                for idx, item in enumerate(items):
                    st.markdown(f"**🧾 Producto #{idx+1}**")
                    product_id_key = f"item_pid_{idx}"
                    item["product_id"] = st.text_input("ID del producto", value=item.get("product_id", ""), key=product_id_key)

                    # Lógica para autocompletar si no se ha hecho ya
                    fetch_flag_key = f"fetched_edit_prod_{idx}"
                    if item["product_id"] and not st.session_state.get(fetch_flag_key):
                        fetched = fetch_menu_item_by_id(item["product_id"])
                        if fetched:
                            st.session_state[f"item_name_{idx}"] = fetched.get("name", "")
                            st.session_state[f"item_price_{idx}"] = fetched.get("price", 0.0)
                            st.session_state[fetch_flag_key] = True

                    item["name"] = st.text_input("Nombre", value=st.session_state.get(f"item_name_{idx}", item.get("name", "")), key=f"item_name_{idx}")
                    item["quantity"] = st.number_input("Cantidad", min_value=1, step=1, value=item.get("quantity", 1), key=f"item_qty_{idx}")
                    item["unit_price"] = st.number_input(
                        "Precio unitario (Q)", min_value=0.0, step=0.5, format="%.2f",
                        value=float(st.session_state.get(f"item_price_{idx}", item.get("unit_price", 0.0))),
                        key=f"item_price_{idx}"
                    )

                    # Botón individual para eliminar producto
                    if len(items) > 1:
                        if st.button(f"🗑️ Eliminar Producto #{idx+1}", key=f"delete_item_{idx}"):
                            st.session_state["edit_order_items"].pop(idx)
                            st.rerun()
                    st.markdown("---")

                # Agregar ítems
                if st.button("➕ Agregar ítem", key="edit_add_item"):
                    items.append({"product_id": "", "name": "", "quantity": 1, "unit_price": 0.0})
                    st.rerun()

                if st.button("Actualizar orden"):
                    updated_data = {
                        "user_id": user_id,
                        "restaurant_id": restaurant_id,
                        "status": status,
                        "date": datetime.combine(date, order_time).isoformat() + "Z",
                        "items": items,
                        "total": sum(i["quantity"] * i["unit_price"] for i in items)
                    }
                    res = requests.put(f"{API_BASE_URL}orders/{order_id}", json=updated_data)
                    if res.status_code == 200:
                        st.success("Orden actualizada correctamente.")
                        del st.session_state["edit_order_data"]
                        del st.session_state["edit_order_id"]
                        del st.session_state["edit_order_items"]
                    else:
                        st.error(f"Error al actualizar: {res.text}")

        else:
            st.markdown("### Actualizar varias órdenes")
            ids_raw = st.text_area("IDs de órdenes (separados por coma)")
            ids = [i.strip() for i in ids_raw.split(",") if i.strip()]

            status = st.selectbox("Nuevo estado (opcional)", ["", "pendiente", "preparando", "entregado", "cancelado"])
            user_id = st.text_input("Nuevo ID de usuario (opcional)")
            restaurant_id = st.text_input("Nuevo ID de restaurante (opcional)")
            date = st.date_input("Nueva fecha (opcional)")
            time_val = st.time_input("Nueva hora (opcional)")

            if st.button("Actualizar órdenes seleccionadas"):
                update_fields = {}
                if status: update_fields["status"] = status
                if user_id: update_fields["user_id"] = user_id
                if restaurant_id: update_fields["restaurant_id"] = restaurant_id
                if date and time_val:
                    update_fields["date"] = datetime.combine(date, time_val).isoformat() + "Z"

                if not ids or not update_fields:
                    st.warning("Debes ingresar al menos un ID y un campo a actualizar.")
                else:
                    res = requests.post(f"{API_BASE_URL}orders/update-many-by-ids", json={"ids": ids, "update": update_fields})
                    if res.status_code == 200:
                        msg = res.json().get("message", "Órdenes actualizadas correctamente.")
                        st.success(msg)
                    else:
                        st.error(f"Error al actualizar órdenes: {res.text}")

    with tabs[4]:
        st.subheader("🗑️ Eliminar Órdenes")

        delete_mode = st.radio("Selecciona el método de eliminación:", ["Por ID", "Por múltiples IDs"], horizontal=True)

        if delete_mode == "Por ID":
            order_id = st.text_input("ID de la orden a eliminar")
            if st.button("Eliminar orden", key="delete_single_order"):
                if order_id:
                    res = requests.delete(f"{API_BASE_URL}orders/{order_id}")
                    if res.status_code == 200:
                        st.success("Orden eliminada correctamente.")
                    else:
                        st.error(f"Error al eliminar orden: {res.text}")
                else:
                    st.warning("Debes ingresar un ID válido.")

        else:
            st.markdown("### Eliminar múltiples órdenes")
            ids_raw = st.text_area("IDs de órdenes a eliminar (separados por coma)")
            ids = [i.strip() for i in ids_raw.split(",") if i.strip()]

            if st.button("Eliminar órdenes seleccionadas", key="delete_many_orders"):
                if ids:
                    res = requests.post(f"{API_BASE_URL}orders/delete-many-by-ids", json={"ids": ids})
                    if res.status_code == 200:
                        msg = res.json().get("message", "Órdenes eliminadas correctamente.")
                        st.success(msg)
                    else:
                        st.error(f"Error al eliminar órdenes: {res.text}")
                else:
                    st.warning("Debes ingresar al menos un ID para eliminar.")
