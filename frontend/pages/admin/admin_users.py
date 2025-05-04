import streamlit as st
import math
import datetime

from apiCalls.admin.apiAdminUsers import (
    fetch_users,
    fetch_user_by_id,
    create_user,
    update_user,
    delete_user,
    create_many_users,
    update_many_users_by_ids,
    delete_many_users_by_ids
)

def admin_users_page():
    st.header("Gestión de Usuarios")
    tabs = st.tabs(["📄 Ver", "🔍 Filtrar", "➕ Crear", "✏️ Actualizar", "🗑️ Eliminar"])

    # ─── 📄 Ver todas ─────────────────────────────────────────────────────────
    with tabs[0]:
        st.subheader("Todos los usuarios")
        users = fetch_users(limit=100)  # traemos un tope de 100
        per_page = 10
        total = len(users)
        total_pages = math.ceil(total / per_page)
        if "user_page" not in st.session_state:
            st.session_state.user_page = 0
        page = st.session_state.user_page
        start, end = page * per_page, (page + 1) * per_page
        slice_users = users[start:end]

        if total == 0:
            st.info("No hay usuarios registrados.")
        else:
            for u in slice_users:
                st.markdown(f"**ID:** {u['_id']}")
                st.markdown(f"- **Nombre:** {u.get('name','—')}")
                st.markdown(f"- **Email:** {u.get('email','—')}")
                st.markdown(f"- **Rol:** {u.get('role','—')}")
                if u.get("location"):
                    coords = u["location"]["coordinates"]
                    st.markdown(f"- **Ubicación:** {coords[1]:.4f}, {coords[0]:.4f}")
                st.markdown("---")

            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                if st.button("← Anterior", key="prev_user", disabled=page == 0):
                    st.session_state.user_page -= 1
                    st.rerun()
            with col3:
                if st.button("Siguiente →", key="next_user", disabled=page >= total_pages - 1):
                    st.session_state.user_page += 1
                    st.rerun()
            col2.markdown(f"Página {page+1} de {total_pages}")

    # ─── 🔍 Filtrar ────────────────────────────────────────────────────────────
    with tabs[1]:
        st.subheader("Filtrar Usuarios")
        # Inputs de filtro
        search        = st.text_input("Texto de búsqueda", key="filter_search_user")
        role          = st.selectbox("Rol", ["", "cliente", "admin"], key="filter_role_user")
        email         = st.text_input("Email exacto", key="filter_email_user")
        has_loc       = st.checkbox("Tiene ubicación", key="filter_hasloc_user")
        near          = st.text_input("Cercanos a (lat,lng)", key="filter_near_user")
        max_distance  = st.number_input("Distancia máxima (m)", value=5000, key="filter_maxdist_user")
        sort          = st.selectbox("Ordenar por", ["name", "email"], key="filter_sort_user")
        order         = st.selectbox("Dirección", ["asc", "desc"], key="filter_order_user")
        limit         = st.number_input("Límite", 1, 100, 20, key="filter_limit_user")
        skip          = st.number_input("Saltar", 0, 1000, 0, key="filter_skip_user")
        fields        = st.text_input("Campos a mostrar (csv)", key="filter_fields_user")

        if st.button("Aplicar filtro", key="btn_filter_user"):
            
            if search and near:
                st.error("No puedes combinar búsqueda de texto con geolocalización. Elige **solo** una opción.")
                st.stop()
            
            params = {}
            if search:       params["search"]      = search
            if role:         params["role"]        = role
            if email:        params["email"]       = email
            if has_loc:      params["hasLocation"] = True
            if near:         params["near"]        = near
            if max_distance: params["maxDistance"] = int(max_distance)
            if sort:         params["sort"]        = sort
            if order:        params["order"]       = order
            if limit:        params["limit"]       = int(limit)
            if skip:         params["skip"]        = int(skip)
            if fields:
                # siempre queremos _id para formatear
                required = ["_id"]
                wanted = [f.strip() for f in fields.split(",") if f.strip()]
                for r in required:
                    if r not in wanted:
                        wanted.append(r)
                params["fields"] = ",".join(wanted)

            try:
                users = fetch_users(**params)
                if not users:
                    st.info("No se encontraron usuarios con esos filtros.")
                else:
                    for u in users:
                        st.markdown(f"**ID:** {u['_id']}")
                        if "name" in u:
                            st.markdown(f"- **Nombre:** {u['name']}")
                        if "email" in u:
                            st.markdown(f"- **Email:** {u['email']}")
                        if "role" in u:
                            st.markdown(f"- **Rol:** {u['role']}")
                        if "location" in u:
                            coords = u["location"]["coordinates"]
                            st.markdown(f"- **Ubicación:** {coords[1]:.4f}, {coords[0]:.4f}")
                        st.markdown("---")
            except Exception as e:
                st.error(f"Error al obtener usuarios: {e}")

            

    # ─── ➕ Crear ──────────────────────────────────────────────────────────────
    with tabs[2]:
            st.subheader("➕ Crear Usuario(s)")

            # Número de filas dinámico
            if "num_users" not in st.session_state:
                st.session_state.num_users = 1

            c1, c2 = st.columns(2)
            with c1:
                if st.button("➕ Añadir otro usuario"):
                    st.session_state.num_users += 1
            with c2:
                if st.session_state.num_users > 1 and st.button("➖ Quitar último usuario"):
                    st.session_state.num_users -= 1

            # Recolectar datos de cada usuario
            user_rows = []
            for i in range(st.session_state.num_users):
                st.markdown(f"**Usuario #{i+1}**")
                name  = st.text_input("Nombre",       key=f"create_name_{i}")
                email = st.text_input("Email",        key=f"create_email_{i}")
                role  = st.selectbox("Rol", ["cliente", "admin"], key=f"create_role_{i}")
                lat   = st.text_input("Latitud (opt.)",  key=f"create_lat_{i}")
                lng   = st.text_input("Longitud (opt.)", key=f"create_lng_{i}")
                st.markdown("---")
                user_rows.append((name, email, role, lat, lng))

            # Botón de envío
            if st.button(f"Crear {len(user_rows)} usuario(s)", key="btn_create_users"):
                payloads = []
                for idx, (name, email, role, lat, lng) in enumerate(user_rows, start=1):
                    if not name or not email:
                        st.error(f"Falta Nombre o Email en la fila #{idx}.")
                        break

                    item = {
                        "name":  name,
                        "email": email,
                        "role":  role
                    }

                    # Si incluyeron lat/lng
                    if lat and lng:
                        try:
                            ll_lat = float(lat)
                            ll_lng = float(lng)
                            item["location"] = {
                                "type": "Point",
                                "coordinates": [ll_lng, ll_lat]
                            }
                        except ValueError:
                            st.warning(f"Lat/Lng inválidos en fila #{idx}, omitiendo ubicación.")

                    payloads.append(item)
                else:
                    try:
                        if len(payloads) == 1:
                            # Crear un solo usuario
                            new = create_user(payloads[0])
                            st.success(f"Usuario creado: {new['_id']}")
                        else:
                            # Crear múltiples
                            result = create_many_users(payloads)
                            st.success(f"Se crearon {len(result)} usuarios correctamente.")
                            # Resetear el formulario
                            st.session_state.num_users = 1
                    except Exception as e:
                        st.error(f"Error al crear usuario(s): {e}")

    # ─── ✏️ Actualizar ─────────────────────────────────────────────────────────
    with tabs[3]:
        st.subheader("✏️ Actualizar Usuario(s)")
        mode = st.radio("Modo", ["Individual", "Por IDs"], key="upd_mode_user")

        if mode == "Individual":
            u_id    = st.text_input("ID de usuario", key="upd_id_user")
            if u_id:
                try:
                    u_obj = fetch_user_by_id(u_id)
                except Exception:
                    st.error("Usuario no encontrado.")
                    u_obj = None
            else:
                u_obj = None

            if u_obj:
                u_name     = st.text_input("Nombre", value=u_obj.get("name",""), key="upd_name_user")
                u_email    = st.text_input("Email",  value=u_obj.get("email",""), key="upd_email_user")
                u_role     = st.selectbox("Rol", ["cliente","admin"], index=["cliente","admin"].index(u_obj.get("role","cliente")), key="upd_role_user")
                if st.button("Actualizar usuario", key="btn_update_user"):
                    payload = {"name": u_name, "email": u_email, "role": u_role}
                    try:
                        updated = update_user(u_id, payload)
                        st.success(f"Usuario actualizado: {updated['_id']}")
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

        else:
            ids_str = st.text_input("IDs separados por coma", key="upd_many_ids_user")
            new_role = st.selectbox("Nuevo rol", ["","cliente","admin"], key="upd_many_role_user")
            if st.button("Actualizar por IDs", key="btn_update_many_user"):
                ids = [i.strip() for i in ids_str.split(",") if i.strip()]
                if not ids or not new_role:
                    st.error("Debes indicar al menos un ID y un rol.")
                else:
                    try:
                        resp = update_many_users_by_ids(ids, {"role": new_role})
                        count = resp.get("result",{}).get("modifiedCount",0)
                        st.success(f"Se actualizaron {count} usuario(s).")
                    except Exception as e:
                        st.error(f"Error al actualización masiva: {e}")

    # ─── 🗑️ Eliminar ──────────────────────────────────────────────────────────
    with tabs[4]:
        st.subheader("🗑️ Eliminar Usuario(s)")
        modo_del = st.radio("Modo", ["Individual", "Por IDs"], key="del_mode_user")

        if modo_del == "Individual":
            d_id = st.text_input("ID de usuario", key="del_id_user")
            if st.button("Eliminar usuario", key="btn_delete_user"):
                if not d_id:
                    st.error("Debes ingresar un ID.")
                else:
                    try:
                        msg = delete_user(d_id)
                        st.success(msg)
                    except Exception as e:
                        st.error(f"Error al eliminar: {e}")
        else:
            d_ids_str = st.text_input("IDs separados por coma", key="del_many_ids_user")
            if st.button("Eliminar usuarios", key="btn_delete_many_user"):
                ids = [i.strip() for i in d_ids_str.split(",") if i.strip()]
                if not ids:
                    st.error("Debes ingresar al menos un ID.")
                else:
                    try:
                        resp = delete_many_users_by_ids(ids)
                        deleted = resp.get("result", {}).get("deletedCount", 0)
                        st.success(f"Se eliminaron {deleted} usuario(s).")
                    except Exception as e:
                        st.error(f"Error al eliminar masivamente: {e}")