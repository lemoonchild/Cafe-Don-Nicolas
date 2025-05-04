import streamlit as st
import requests
import os
import datetime
from dotenv import load_dotenv

from api import fetch_restaurants, fetch_menu_items
from apiCalls.client.apiClientRestaurants import fetch_restaurant_by_id
from apiCalls.client.apiClientOrders import create_order

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000/api")



def cliente_restaurants_page():
    # ─── Inicializar estado ─────────────────────────────────────────────────
    if "current_page" not in st.session_state:
        st.session_state.current_page = None
    if "selected_restaurant_id" not in st.session_state:
        st.session_state.selected_restaurant_id = None
    if "cart" not in st.session_state:
        st.session_state.cart = []

    st.header("🍴 Restaurantes Disponibles")

    # ─── Página: Ver menú ───────────────────────────────────────────────────
    if st.session_state.current_page == "ver_menu":
        rid = st.session_state.selected_restaurant_id

        # Botones de navegación
        col1, col2 = st.columns(2)
        with col1:
            st.button("← Volver a Restaurantes", on_click=_reset_to_list)
        with col2:
            st.button("🛒 Ir al Carrito",       on_click=_go_to_cart)

        # Cabecera
        data = fetch_restaurant_by_id(rid)
        st.subheader(f"🍽️ Menú de {data.get('name','Desconocido')}")
        st.markdown("---")

        # Lista de platos
        platos = fetch_menu_items(restaurant_id=rid)
        if not platos:
            st.info("Este restaurante aún no tiene productos.")
        else:
            for p in platos:
                if p.get("image_url"):
                    st.image(f"http://localhost:3000{p['image_url']}", width=150)
                st.markdown(f"### {p['name']}")
                st.markdown(p.get("description","_Sin descripción_"))
                st.markdown(f"**Precio:** Q{p.get('price',0):.2f}")
                estado = "Disponible" if p.get("available") else "No disponible"
                st.markdown(f"**Estado:** {estado}")

                if p.get("available"):
                    # Formulario para añadir al carrito
                    with st.form(f"form_{p['_id']}"):
                        qty = st.number_input("Cantidad", min_value=1, step=1, key=f"qty_{p['_id']}")
                        if st.form_submit_button("Agregar al carrito"):
                            st.session_state.cart.append({
                                "product_id": p["_id"],
                                "name":       p["name"],
                                "quantity":   qty,
                                "unit_price": p["price"]
                            })
                            st.success(f"{p['name']} x{qty} agregado al carrito.")
                st.markdown("---")
        return

    # ─── Página: Carrito ─────────────────────────────────────────────────────
    if st.session_state.current_page == "carrito":
        st.subheader("🛒 Tu Carrito")
        cart = st.session_state.cart

        # Vacío
        if not cart:
            st.info("No has agregado ningún producto aún.")
        else:
            total = 0
            for idx, item in enumerate(cart):
                line_total = item["quantity"] * item["unit_price"]
                st.markdown(f"**{item['name']}** — {item['quantity']} × Q{item['unit_price']:.2f} = Q{line_total:.2f}")
                if st.button("❌ Eliminar", key=f"rm_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
                total += line_total

            st.markdown(f"### Total: Q{total:.2f}")
            user_id = st.session_state.user["_id"]



            if st.button("✅ Realizar Pedido"):
                payload = {
                    "user_id":       user_id,
                    "restaurant_id": st.session_state.selected_restaurant_id,
                    "date":          datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
                    "status":        "pendiente",
                    "total":         total,
                    "items":         cart
                }
                try:
                    create_order(payload)
                    st.success("Pedido creado correctamente.")
                    # reset
                    st.session_state.cart.clear()
                    _reset_to_list()
                except Exception as e:
                    st.error(f"Error al crear pedido: {e}")

        if st.button("← Volver a Restaurantes"):
            _reset_to_list()
        return

    # ─── Página default: Restaurantes + Filtros ───────────────────────────────
    tabs = st.tabs(["📄 Ver", "🔍 Filtrar"])
    # — Ver
    with tabs[0]:
        st.subheader("📄 Ver Restaurantes")
        restos = fetch_restaurants()
        if not restos:
            st.info("No hay restaurantes registrados.")
        else:
            for r in restos:
                with st.expander(r["name"]):
                    st.markdown(f"**Dirección:** {r.get('address','Sin dirección')}")
                    coords = r.get("location",{}).get("coordinates",[None,None])
                    st.markdown(f"**Ubicación:** {coords[1]}, {coords[0]}")
                    sched = r.get("schedule",{})
                    st.markdown(f"**Horario:** {sched.get('open','??')} - {sched.get('close','??')}")
                    if r.get("image_url"):
                        st.image(f"http://localhost:3000{r['image_url']}", width=200)
                    if st.button("Ver menú", key=f"ver_menu_{r['_id']}"):
                        st.session_state.selected_restaurant_id = r["_id"]
                        st.session_state.current_page = "ver_menu"
                        st.rerun()

    # — Filtrar
    with tabs[1]:
        st.subheader("🔍 Filtrar Restaurantes")
        search    = st.text_input("Buscar por nombre o palabra clave:")
        has_image = st.checkbox("Solo con imagen")
        use_open  = st.checkbox("Filtrar por hora de apertura")
        open_at   = st.time_input("Abiertos a las:", key="open_at_input") if use_open else None
        use_near  = st.checkbox("Filtrar por ubicación (geoNear)")
        if use_near:
            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input("Latitud",  format="%.6f", key="lat_input")
            with col2:
                lng = st.number_input("Longitud", format="%.6f", key="lng_input")
            distance = st.slider("Distancia máxima (m)", 1000, 20000, 5000, key="distance_input")
        else:
            lat = lng = distance = None

        ids_raw   = st.text_area("Filtrar por IDs (coma sep.)")
        col3, col4 = st.columns(2)
        with col3:
            sort_field = st.selectbox("Ordenar por", ["name","address","schedule.open","schedule.close"])
        with col4:
            sort_order = st.radio("Dirección", ["asc","desc"], horizontal=True)
        limit = st.slider("Límite", 1,100,10)
        skip  = st.number_input("Saltar", 0,0,step=1)

        if st.button("Aplicar filtros"):
            params = {}
            if search:      params["search"]      = search
            if has_image:   params["hasImage"]    = "true"
            if open_at:     params["openAt"]      = open_at.strftime("%H:%M")
            if use_near:    
                params["near"]        = f"{lat},{lng}"
                params["maxDistance"] = distance
            if ids_raw:
                lst = [i.strip() for i in ids_raw.split(",") if i.strip()]
                params["ids"] = ",".join(lst)
            params.update({"sort":sort_field,"order":sort_order,"limit":limit,"skip":skip})

            resp = requests.get(f"{API_BASE_URL}/restaurants", params=params)
            if resp.ok:
                data = resp.json()
                if data:
                    st.success(f"{len(data)} encontrado(s).")
                    for r in data:
                        with st.expander(r["name"]):
                            st.markdown(f"**Dirección:** {r.get('address')}")
                            coords = r.get("location",{}).get("coordinates",[None,None])
                            st.markdown(f"**Ubicación:** {coords[1]}, {coords[0]}")
                            sched = r.get("schedule",{})
                            st.markdown(f"**Horario:** {sched.get('open')} - {sched.get('close')}")
                            if r.get("description"):
                                st.markdown(r["description"])
                            if r.get("image_url"):
                                st.image(f"http://localhost:3000{r['image_url']}", width=200)
                else:
                    st.warning("No hay coincidencias.")
            else:
                st.error("Error en la API: " + resp.text)


def _reset_to_list():
    st.session_state.current_page = None
    st.session_state.selected_restaurant_id = None
    st.rerun()


def _go_to_cart():
    st.session_state.current_page = "carrito"
    st.rerun()
