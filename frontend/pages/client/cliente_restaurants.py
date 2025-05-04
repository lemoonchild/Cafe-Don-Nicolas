import streamlit as st
import requests
import os
from api import fetch_restaurants 
from api import fetch_menu_items  

from apiCalls.client.apiClientRestaurants import fetch_restaurant_by_id

from dotenv import load_dotenv

load_dotenv() 

API_BASE_URL = os.getenv("API_BASE_URL")
        
def cliente_restaurants_page():
    st.header("🍴 Restaurantes Disponibles")

    if st.session_state.get("current_page") == "ver_menu":

        rest_id = st.session_state.selected_restaurant_id
    
        st.markdown("---")
        # Botón para volver
        if st.button("Volver a restaurantes"):
            st.session_state.current_page = None
            del st.session_state.selected_restaurant_id
            st.rerun()

        rest_data = fetch_restaurant_by_id(rest_id)
        rest_name = rest_data.get("name", "Desconocido") if rest_data else "Desconocido"
        st.header(f"🍽️ Menú del Restaurante: {rest_name}")

        st.markdown("---")
        productos = fetch_menu_items(restaurant_id=rest_id)

        if productos:
            for p in productos:
                if p.get("image_url"):
                    st.image(f"http://localhost:3000{p['image_url']}", width=150)
                st.markdown(f"**{p['name']}**")
                st.markdown(f"_{p.get('description', 'Sin descripción')}_")
                st.markdown(f"**Precio:** Q{p.get('price', 0):.2f}")
                st.markdown(f"**Categoría:** {p.get('category', 'Sin categoría')}")
                estado = "Disponible" if p.get("available", False) else "No disponible"
                st.markdown(f"**Estado:** {estado}")

                st.markdown("---")
        else:
            st.info("Este restaurante aún no tiene productos.")

        return
    
    
    st.write("Administra los restaurantes disponibles en el sistema. Puedes crear nuevos registros, editarlos o eliminarlos según sea necesario.")
    tabs = st.tabs(["📄 Ver", "🔍 Filtrar", "🛒 Carrito"])

    # === VER RESTAURANTES ===
    with tabs[0]:
        st.subheader("📄 Ver Restaurantes")

        if st.session_state.get("refresh_restaurants"):
            del st.session_state["refresh_restaurants"]
            st.rerun()

        restos = fetch_restaurants()

        if restos:
            for r in restos:
                with st.expander(r["name"]):
                    st.markdown(f"**Dirección:** {r.get('address', 'Sin dirección')}")
                    
                    coords = r.get("location", {}).get("coordinates", [None, None])
                    st.markdown(f"**Ubicación (lat, lng):** {coords[1]}, {coords[0]}")
                    
                    horario = r.get("schedule", {})
                    st.markdown(f"**Horario:** {horario.get('open', '??')} - {horario.get('close', '??')}")

                    if r.get("image_url"):
                        st.image(f"http://localhost:3000{r['image_url']}", width=200)

                    if st.button("Ver menú", key=f"ver_menu_{r['_id']}"):
                        st.session_state.selected_restaurant_id = r["_id"]
                        st.session_state.current_page = "ver_menu"
                        st.rerun()
        else:
            st.info("No hay restaurantes registrados.")

    # === VER POR FILTROS ===
    with tabs[1]:
        st.subheader("🔍 Filtrar Restaurantes")

        # === Controles de filtrado ===
        search = st.text_input("Buscar por nombre o palabra clave:")
        has_image = st.checkbox("Solo con imagen")

        # Activar filtro por horario
        use_open_at = st.checkbox("Filtrar por hora de apertura")
        if use_open_at:
            open_at = st.time_input("Restaurantes abiertos a las:", key="open_at_input")
        else:
            open_at = None

        # Activar filtro por ubicación (geoNear)
        use_near = st.checkbox("Filtrar por ubicación (geoNear)")
        if use_near:
            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input("Latitud", format="%.6f", key="lat_input")
            with col2:
                lng = st.number_input("Longitud", format="%.6f", key="lng_input")
            distance = st.slider("Distancia máxima (metros)", 1000, 20000, 5000, key="distance_input")
        else:
            lat, lng, distance = None, None, None

        ids_raw = st.text_area("Filtrar por IDs (separados por coma)", help="Ej: 641b..., 642a...")

        col3, col4 = st.columns(2)
        with col3:
            sort_field = st.selectbox("Ordenar por", options=["name", "address", "schedule.open", "schedule.close"], index=0)
        with col4:
            sort_order = st.radio("Orden", options=["asc", "desc"], horizontal=True)

        limit = st.slider("Límite de resultados", min_value=1, max_value=100, value=10)
        skip = st.number_input("Saltar registros", min_value=0, value=0, step=1)

        # === Botón para aplicar filtros ===
        if st.button("Aplicar filtros"):
            params = {}

            if search:
                params["search"] = search
            if has_image:
                params["hasImage"] = "true"
            if use_open_at and open_at:
                params["openAt"] = open_at.strftime("%H:%M")
            if use_near and lat is not None and lng is not None:
                params["near"] = f"{lat},{lng}"
                params["maxDistance"] = distance
            if ids_raw:
                ids = [i.strip() for i in ids_raw.split(",") if i.strip()]
                params["ids"] = ",".join(ids)
            if sort_field:
                params["sort"] = sort_field
                params["order"] = sort_order
            if limit:
                params["limit"] = limit
            if skip:
                params["skip"] = skip

            # Consulta a la API
            response = requests.get(f"{API_BASE_URL}restaurants", params=params)
            if response.status_code == 200:
                data = response.json()
                if data:
                    st.success(f"{len(data)} restaurante(s) encontrados.")
                    for r in data:
                        with st.expander(r["name"]):
                            st.markdown(f"**Dirección:** {r.get('address')}")
                            coords = r.get("location", {}).get("coordinates", [None, None])
                            st.markdown(f"**Ubicación:** {coords[1]}, {coords[0]}")
                            horario = r.get("schedule", {})
                            st.markdown(f"**Horario:** {horario.get('open')} - {horario.get('close')}")
                            if r.get("description"):
                                st.markdown(f"**Descripción:** {r['description']}")
                            if r.get("image_url"):
                                st.image(f"http://localhost:3000{r['image_url']}", width=200)
                else:
                    st.warning("No se encontraron restaurantes con los filtros aplicados.")
            else:
                st.error("Error en la solicitud: " + response.text)
