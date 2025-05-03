import streamlit as st
import requests
import os
from api import fetch_restaurants 
from dotenv import load_dotenv

load_dotenv() 

API_BASE_URL = os.getenv("API_BASE_URL")

def admin_restaurants_page():
    st.header("Gestión de Restaurantes")
    st.write("Administra los restaurantes disponibles en el sistema. Puedes crear nuevos registros, editarlos o eliminarlos según sea necesario.")

    tabs = st.tabs(["📄 Ver", "🔍 Filtrar", "➕ Crear", "✏️ Actualizar", "🗑️ Eliminar", "🖼️ Subir Imagen"])

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

    # Controlar el número de formularios activos
    if "num_forms" not in st.session_state:
        st.session_state.num_forms = 1

    # === CREAR RESTAURANTES ===
    with tabs[2]:
        st.subheader("➕ Crear Restaurante(s)")

        if st.session_state.get("success_restaurante"):
            st.success("¡Restaurantes creados correctamente!")
            del st.session_state["success_restaurante"]

        st.write("Puedes crear uno o varios restaurantes llenando cada formulario. Haz clic en 'Agregar otro' para más.")

        if "num_forms" not in st.session_state:
            st.session_state.num_forms = 1

        restaurantes = []

        # Crear formularios según la cantidad actual
        for i in range(st.session_state.num_forms):
            with st.expander(f"📝 Restaurante #{i + 1}", expanded=True):
                name = st.text_input("Nombre", key=f"name_{i}")
                address = st.text_input("Dirección", key=f"address_{i}")

                col1, col2 = st.columns(2)
                with col1:
                    lat = st.number_input("Latitud", format="%.6f", key=f"lat_{i}")
                with col2:
                    lng = st.number_input("Longitud", format="%.6f", key=f"lng_{i}")

                open_hour = st.text_input("Hora de apertura (HH:mm)", key=f"open_{i}")
                close_hour = st.text_input("Hora de cierre (HH:mm)", key=f"close_{i}")

                # Botón para eliminar este formulario (si hay más de uno)
                if st.session_state.num_forms > 1:
                    if st.button(f"🗑️ Eliminar este restaurante", key=f"delete_{i}"):
                        # Eliminar todos los campos relacionados en st.session_state
                        for field in ["name", "address", "lat", "lng", "open", "close"]:
                            st.session_state.pop(f"{field}_{i}", None)
                        st.session_state.num_forms -= 1
                        st.rerun()

                # Guardar temporalmente el restaurante
                restaurantes.append({
                    "name": name,
                    "address": address,
                    "location": {"type": "Point", "coordinates": [lng, lat]},
                    "schedule": {"open": open_hour, "close": close_hour},
                })

        # Botón para agregar más formularios
        if st.button("➕ Agregar otro restaurante"):
            st.session_state.num_forms += 1
            st.rerun()

        # Botón para enviar todos
        if st.button("Crear restaurante(s)"):
            errores = []
            validos = []

            for idx, r in enumerate(restaurantes):
                nombre = r["name"].strip()
                direccion = r["address"].strip()
                lng, lat = r["location"]["coordinates"]

                if not nombre or not direccion:
                    continue  # ignorar si están vacíos

                if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                    errores.append(f"Restaurante #{idx + 1} tiene coordenadas inválidas: lat={lat}, lng={lng}")
                else:
                    validos.append(r)

            if errores:
                st.error("Se encontraron errores en las coordenadas:")
                for err in errores:
                    st.markdown(f"Ha ocurrido un error: {err}")
            elif not validos:
                st.warning("No se ingresaron restaurantes válidos.")
            else:
                url = f"{API_BASE_URL}restaurants/create-many" if len(validos) > 1 else f"{API_BASE_URL}restaurants"
                body = {"items": validos} if len(validos) > 1 else validos[0]
                res = requests.post(url, json=body)
                if res.status_code in [200, 201]:
                    st.session_state.success_restaurante = True
                    st.session_state.num_forms = 1
                    st.rerun()

                else:
                    st.error(f"Ha ocurrido un error: {res.text}")

    with tabs[3]:
        st.subheader("✏️ Actualizar Restaurante(s)")

        if st.session_state.get("success_update"):
            st.success(st.session_state.success_update)
            del st.session_state["success_update"]

        metodo = st.radio("Selecciona el método de actualización:", ["Por ID", "Por múltiples IDs"], horizontal=True)

        # === === === MODO: POR ID === === ===
        if metodo == "Por ID":
            st.markdown("### Actualizar restaurante por ID")

            rest_id = st.text_input("ID del restaurante a actualizar")

            if rest_id and st.button("🔍 Buscar restaurante"):
                res = requests.get(f"{API_BASE_URL}restaurants/{rest_id}")
                if res.status_code == 200:
                    st.session_state.rest_data = res.json()
                    st.session_state.rest_id = rest_id
                    st.rerun()
                else:
                    st.error("No se encontró el restaurante con ese ID.")

            if st.session_state.get("rest_data") and st.session_state.get("rest_id") == rest_id:
                data = st.session_state.rest_data

                nuevo_nombre = st.text_input("Nombre", value=data.get("name", ""), key="update_name")
                nueva_direccion = st.text_input("Dirección", value=data.get("address", ""), key="update_address")

                coords = data.get("location", {}).get("coordinates", [0.0, 0.0])
                lat = st.number_input("Latitud", value=coords[1], format="%.6f", key="update_lat")
                lng = st.number_input("Longitud", value=coords[0], format="%.6f", key="update_lng")

                horario = data.get("schedule", {})
                hora_apertura = st.text_input("Hora de apertura (HH:mm)", value=horario.get("open", ""), key="update_open")
                hora_cierre = st.text_input("Hora de cierre (HH:mm)", value=horario.get("close", ""), key="update_close")

                if st.button("✏️ Actualizar restaurante"):
                    update_payload = {
                        "name": nuevo_nombre,
                        "address": nueva_direccion,
                        "location": {
                            "type": "Point",
                            "coordinates": [lng, lat]
                        },
                        "schedule": {
                            "open": hora_apertura,
                            "close": hora_cierre
                        }
                    }

                    res = requests.put(f"{API_BASE_URL}restaurants/{rest_id}", json=update_payload)
                    if res.status_code == 200:
                        st.session_state.success_update = "Restaurante actualizado correctamente."
                        del st.session_state["rest_data"]
                        del st.session_state["rest_id"]
                        st.rerun()
                    else:
                        st.error(f"Error al actualizar: {res.text}")

        # === === === MODO: POR MÚLTIPLES IDS === === ===
        elif metodo == "Por múltiples IDs":
            st.markdown("### Actualizar múltiples restaurantes por IDs")

            ids_raw = st.text_area("IDs de restaurantes (separados por coma)")
            nuevo_nombre = st.text_input("Nuevo nombre")
            nueva_direccion = st.text_input("Nueva dirección")
            col1, col2 = st.columns(2)
            with col1:
                nueva_lat = st.number_input("Nueva latitud", format="%.6f", key="multi_lat")
            with col2:
                nueva_lng = st.number_input("Nueva longitud", format="%.6f", key="multi_lng")
            nueva_hora_apertura = st.text_input("Nueva hora de apertura (HH:mm)", key="multi_open")
            nueva_hora_cierre = st.text_input("Nueva hora de cierre (HH:mm)", key="multi_close")

            update = {"$set": {}}
            if nuevo_nombre: update["$set"]["name"] = nuevo_nombre
            if nueva_direccion: update["$set"]["address"] = nueva_direccion
            if nueva_lat != 0.0 or nueva_lng != 0.0:
                update["$set"]["location"] = {"type": "Point", "coordinates": [nueva_lng, nueva_lat]}
            if nueva_hora_apertura or nueva_hora_cierre:
                update["$set"]["schedule"] = {}
                if nueva_hora_apertura:
                    update["$set"]["schedule"]["open"] = nueva_hora_apertura
                if nueva_hora_cierre:
                    update["$set"]["schedule"]["close"] = nueva_hora_cierre

            if st.button("Actualizar por múltiples IDs"):
                ids = [i.strip() for i in ids_raw.split(",") if i.strip()]
                if not ids or not update["$set"]:
                    st.warning("Debes ingresar al menos un ID y un campo para actualizar.")
                else:
                    res = requests.post(f"{API_BASE_URL}restaurants/update-many-by-ids", json={
                        "ids": ids,
                        "update": update
                    })
                    if res.status_code == 200:
                        st.session_state.success_update = "Restaurante actualizado correctamente."
                        st.rerun()
                    else:
                        st.error(f"Error: {res.text}")

    # === ELIMINAR ===
    with tabs[4]:
        st.subheader("🗑️ Eliminar Restaurante(s)")

        if st.session_state.get("success_delete"):
            st.success(st.session_state.success_delete)
            del st.session_state["success_delete"]

        modo = st.radio("Selecciona el método de eliminación:", ["Por ID", "Por múltiples IDs"], horizontal=True)

        # === ELIMINAR POR ID ===
        if modo == "Por ID":
            delete_id = st.text_input("ID del restaurante a eliminar")

            if delete_id and st.button("🔍 Buscar restaurante para eliminar"):
                res = requests.get(f"{API_BASE_URL}restaurants/{delete_id}")
                if res.status_code == 200:
                    st.session_state.found_restaurant = res.json()
                    st.session_state.pending_delete_id = delete_id
                    st.rerun()
                else:
                    st.error("Restaurante no encontrado con ese ID.")

            # Mostrar si hay uno encontrado
            if st.session_state.get("found_restaurant"):
                r = st.session_state.found_restaurant
                with st.expander("Restaurante encontrado"):
                    st.markdown(f"**Nombre:** {r.get('name')}")
                    st.markdown(f"**Dirección:** {r.get('address')}")
                    coords = r.get("location", {}).get("coordinates", [None, None])
                    st.markdown(f"**Coordenadas:** {coords[1]}, {coords[0]}")
                    horario = r.get("schedule", {})
                    st.markdown(f"**Horario:** {horario.get('open')} - {horario.get('close')}")
                    if r.get("image_url"):
                        st.image(f"http://localhost:3000{r['image_url']}", width=200)

                if st.button("🗑️ Confirmar eliminación"):
                    delete_id = st.session_state.get("pending_delete_id")
                    delete_res = requests.delete(f"{API_BASE_URL}restaurants/{delete_id}")
                    if delete_res.status_code == 200:
                        st.session_state.success_delete = "Restaurante eliminado correctamente."
                        # limpiar
                        del st.session_state["found_restaurant"]
                        del st.session_state["pending_delete_id"]
                        st.rerun()
                    else:
                        st.error(f"Error al eliminar: {delete_res.text}")

        # === ELIMINAR POR MÚLTIPLES IDS ===
        elif modo == "Por múltiples IDs":
            ids_raw = st.text_area("IDs de restaurantes a eliminar (separados por coma)")
            ids = [i.strip() for i in ids_raw.split(",") if i.strip()]

            if st.button("🗑️ Eliminar restaurantes seleccionados"):
                if not ids:
                    st.warning("Debes ingresar al menos un ID.")
                else:
                    res = requests.post(f"{API_BASE_URL}restaurants/delete-many-by-ids", json={"ids": ids})
                    if res.status_code == 200:
                        deleted = res.json().get("result", {}).get("deletedCount", len(ids))
                        st.session_state.success_delete = f"Se eliminaron {deleted} restaurante(s)."
                        st.rerun()
                    else:
                        st.error(f"Error: {res.text}")

    # === SUBIR IMAGEN ===
    with tabs[5]:
        st.subheader("🖼️ Subir Imagen a Restaurante")
        upload_id = st.text_input("ID del restaurante")
        image_file = st.file_uploader("Selecciona imagen", type=["png", "jpg", "jpeg"])

        # Mostrar mensaje si viene de un rerun exitoso
        if st.session_state.get("success_upload"):
            st.success(st.session_state.success_upload)
            del st.session_state["success_upload"]

        if st.button("Subir Imagen"):
            if not upload_id:
                st.warning("Debes ingresar el ID del restaurante.")
            elif not image_file:
                st.warning("Debes seleccionar una imagen.")
            else:
                files = {"image": (image_file.name, image_file, image_file.type)}
                res = requests.post(f"{API_BASE_URL}restaurants/upload-image/{upload_id}", files=files)

                if res.status_code == 200:
                    result = res.json()
                    # Guardar image_id en session_state para mostrar después del rerun
                    if "restaurant" in result and result["restaurant"].get("image_id"):
                        st.session_state.uploaded_image_url = f"{API_BASE_URL}images/{result['restaurant']['image_id']}"
                    st.session_state.success_upload = "Imagen subida correctamente."
                    st.session_state.refresh_restaurants = True
                    st.rerun()
                else:
                    st.error(f"Error: {res.text}")

        # Mostrar imagen subida después del rerun
        if st.session_state.get("uploaded_image_url"):
            st.image(st.session_state.uploaded_image_url, caption="Vista previa de la imagen subida", width=300)
            del st.session_state["uploaded_image_url"]

