# frontend/pages/admin/admin_reviews.py

import datetime
import math
import streamlit as st

from apiCalls.admin.apiAdminReviews import (
    fetch_reviews, fetch_review_by_id, fetch_reviews_with_filters,
    create_review, update_review, delete_review,
    create_many_reviews, update_many_reviews,
    update_many_reviews_by_ids, delete_many_reviews,
    delete_many_reviews_by_ids
)

from apiCalls.admin.apiAdminUsers import fetch_user_by_id
from apiCalls.admin.apiAdminRestaurants import fetch_restaurant_by_id

def admin_reviews_page():
    st.header("🔧 Gestión de Reviews")
    tabs = st.tabs(["📄 Ver", "🔍 Filtrar", "➕ Crear", "✏️ Actualizar", "🗑️ Eliminar"])

    # ─── 📄 Ver todas ─────────────────────────────────────────────────────────
    with tabs[0]:
        st.subheader("Todas las reseñas")
        st.markdown("---")

        reviews = fetch_reviews()
        per_page = 10
        total = len(reviews)
        total_pages = math.ceil(total / per_page)
        if "rev_page" not in st.session_state:
            st.session_state.rev_page = 0
        page = st.session_state.rev_page
        start, end = page * per_page, (page + 1) * per_page
        slice_reviews = reviews[start:end]

        if total == 0:
            st.info("No hay reseñas registradas.")
        else:
            for rev in slice_reviews:
                # Obtener nombres
                user = fetch_user_by_id(rev["user_id"])
                rest = fetch_restaurant_by_id(rev["restaurant_id"])
                user_name = user["name"] if user and "name" in user else "[Usuario Borrado]"
                rest_name = rest["name"] if rest and "name" in rest else "[Restaurante Borrado]"

                # Parsear fecha
                dt = datetime.datetime.fromisoformat(rev["date"].replace("Z", ""))
                fecha_str = dt.strftime("%d/%m/%Y %H:%M")

                st.markdown(f"**ID:** {rev['_id']}")
                st.markdown(f"- **Usuario:** {user_name} ({rev['user_id']})")
                st.markdown(f"- **Restaurante:** {rest_name} ({rev['restaurant_id']})")
                if rev.get("order_id"):
                    st.markdown(f"- **Orden relacionada:** {rev['order_id']}")
                st.markdown(f"- **Rating:** {rev['rating']}/5")
                st.markdown(f"- **Fecha:** {fecha_str}")
                st.markdown(f"- **Comentario:** {rev.get('comment','')}")
                st.markdown("---")

            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("← Anterior", key="prev_rev", disabled=page == 0):
                    st.session_state.rev_page -= 1
                    st.rerun()
            with col3:
                if st.button("Siguiente →", key="next_rev", disabled=page >= total_pages - 1):
                    st.session_state.rev_page += 1
                    st.rerun()
            col2.markdown(f"Página {page+1} de {total_pages}")

    # ─── 🔍 Filtrar ────────────────────────────────────────────────────────────
    with tabs[1]:
        st.subheader("Filtrar Reseñas")

        # +––– Inputs de filtro –––––––––––––––––––––––––––––––––––––––––––––––+
        rid       = st.text_input("Restaurant ID",       key="filter_rid")
        uid       = st.text_input("User ID",             key="filter_uid")
        oid       = st.text_input("Order ID",            key="filter_oid")
        search    = st.text_input("Texto en comentario", key="filter_search")
        rating    = st.selectbox("Rating exacto", [""]+list(range(1,6)), key="filter_rating")
        rmin      = st.number_input("Rating Mínimo", 1,5,1, key="filter_rating_min")
        rmax      = st.number_input("Rating Máximo", 1,5,5, key="filter_rating_max")
        limit     = st.number_input("Límite", 1,100,10, key="filter_limit")
        skip      = st.number_input("Saltar", 0,1000,0,   key="filter_skip")
        sort      = st.selectbox("Ordenar por",   ["date","rating"], key="filter_sort")
        order     = st.selectbox("Dirección",     ["asc","desc"],    key="filter_order")
        fields    = st.text_input("Campos a mostrar (csv)", key="filter_fields")
        # +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+

        if st.button("Aplicar filtro", key="apply_filter"):
            # Construye llamada
            kwargs = {}
            if rid:    kwargs["restaurant_id"] = rid
            if uid:    kwargs["user_id"]       = uid
            if oid:    kwargs["order_id"]      = oid
            if rating: kwargs["rating"]        = int(rating)
            if rmin:   kwargs["ratingMin"]     = rmin
            if rmax:   kwargs["ratingMax"]     = rmax
            if search: kwargs["search"]        = search
            if sort:   kwargs["sort"]          = sort
            if order:  kwargs["order"]         = order
            if limit:  kwargs["limit"]         = limit
            if skip:   kwargs["skip"]          = skip
            if fields: kwargs["fields"]        = fields

            raw_fields = None
            if fields:
                # esta es la lista *exacta* que el usuario quiere ver
                raw_fields = [f.strip() for f in fields.split(",") if f.strip()]

                # pero para preguntarle al API tengo que incluir además los obligatorios:
                required = ["_id", "user_id", "restaurant_id", "date"]
                projection = set(raw_fields + required)
                kwargs["fields"] = ",".join(projection)

                reviews = fetch_reviews_with_filters(**kwargs)

            # Muestra los resultados bonitos
            if not reviews:
                st.info("No se encontraron reseñas con esos filtros.")
            else:
                for rev in reviews:
                    # Siempre querrás reemplazar estos IDs por nombres

                    st.markdown(f"**ID:** {rev['_id']}")


                    user = fetch_user_by_id(rev["user_id"])["name"]
                    rest = fetch_restaurant_by_id(rev["restaurant_id"])["name"]
                    dt = datetime.datetime.fromisoformat(rev["date"].replace("Z",""))
                    fecha = dt.strftime("%d/%m/%Y %H:%M")

                    # si no hay raw_fields, muestro TODO (con tu formato habitual)
                    if raw_fields is None:
                        st.markdown(f"- **Usuario:** {user} ({rev['user_id']})  ")
                        st.markdown(f"- **Restaurante:** {rest} ({rev['restaurant_id']})  ")
                        if rev.get("order_id"):
                            st.markdown(f"- **Orden relacionada:** {rev['order_id']}  ")
                        st.markdown(f"- **Rating:** {rev['rating']}/5  ")
                        st.markdown(f"- **Fecha:** {fecha}  ")
                        st.markdown(f"- **Comentario:** {rev.get('comment','')}  ")
                        st.markdown("---")
                    else:
                        # si el usuario pidió campos, los pinto uno por uno
                        for field in raw_fields:
                            if field == "user_id":
                                st.markdown(f"- **Usuario:** {user} ({rev['user_id']})  ")
                            elif field == "restaurant_id":
                                st.markdown(f"- **Restaurante:** {rest} ({rev['restaurant_id']})  ")
                            elif field == "order_id" and rev.get("order_id"):
                                st.markdown(f"- **Orden relacionada:** {rev['order_id']}  ")
                            elif field == "rating":
                                st.markdown(f"- **Rating:** {rev['rating']}/5  ")
                            elif field == "comment":
                                st.markdown(f"- **Comentario:** {rev.get('comment','')}  ")
                            elif field == "date":
                                st.markdown(f"- **Fecha:** {fecha}  ")
                            else:
                                # cualquier otro campo genérico
                                val = rev.get(field)
                                st.markdown(f"- **{field.replace('_',' ').capitalize()}:** {val}  ")
                        st.markdown("---")

    # ─── ➕ Crear ──────────────────────────────────────────────────────────────
    with tabs[2]:
        st.subheader("➕ Crear Múltiples Reseñas")

        # — User ID único para todas las reseñas
        c_user = st.text_input("User ID", key="create_user")
        if not c_user:
            st.warning("Debes indicar un User ID antes de añadir reseñas.")
        else:
            # — Controlamos en session_state cuántas filas mostramos
            if "num_reviews" not in st.session_state:
                st.session_state.num_reviews = 1

            cols = st.columns([1,1,1,1,1])
            with cols[0]:
                if st.button("➕ Añadir otra reseña"):
                    st.session_state.num_reviews += 1
            with cols[1]:
                if st.session_state.num_reviews > 1:
                    if st.button("➖ Quitar última reseña"):
                        st.session_state.num_reviews -= 1

            # — Recolectamos los datos de cada reseña
            review_rows = []
            for i in range(st.session_state.num_reviews):
                st.markdown(f"**Reseña #{i+1}**")
                r1 = st.text_input("Restaurant ID", key=f"create_rest_{i}")
                r2 = st.text_input("Order ID (opcional)", key=f"create_order_{i}")
                r3 = st.slider("Rating", 1, 5, 3, key=f"create_rating_{i}")
                r4 = st.text_area("Comentario", key=f"create_comment_{i}")
                st.markdown("---")
                review_rows.append((r1, r2, r3, r4))

            # — Botón de envío para todas
            if st.button(f"Crear {len(review_rows)} reseñas", key="btn_create_many"):
                # Validamos
                payloads = []
                for idx, (rest_id, ord_id, rating, comment) in enumerate(review_rows, start=1):
                    if not rest_id:
                        st.error(f"Falta Restaurant ID en la fila #{idx}")
                        break
                    payload = {
                        "user_id":       c_user,
                        "restaurant_id": rest_id,
                        "rating":        rating,
                        "comment":       comment,
                        "date": datetime.datetime.utcnow()
                                        .isoformat(timespec="milliseconds") + "Z"
                    }
                    if ord_id:
                        payload["order_id"] = ord_id
                    payloads.append(payload)
                else:
                    # Si todas las filas ok, enviamos en bloque
                    try:
                        result = create_many_reviews(payloads)
                        st.success(f"Se crearon {len(result['result'])} reseñas correctamente.")
                        # opcional: resetear el formulario
                        st.session_state.num_reviews = 1
                    except Exception as e:
                        st.error(f"Error al crear reseñas: {e}")

    # ─── ✏️ Actualizar ─────────────────────────────────────────────────────────
    with tabs[3]:
        st.subheader("✏️ Actualizar Reseña(s)")

        modo_upd = st.radio("Selecciona modo", ["Individual", "Por IDs"], key="upd_mode")

        if modo_upd == "Individual":
            u_id      = st.text_input("ID de la reseña a actualizar", key="upd_id")
            u_rating  = st.slider("Nuevo Rating", 1, 5, 3, key="upd_rating")
            u_comment = st.text_area("Nuevo Comentario", key="upd_comment")
            if st.button("Actualizar reseña", key="btn_update_single"):
                if not u_id:
                    st.error("Debes ingresar el ID de la reseña.")
                else:
                    try:
                        updated = update_review(u_id, {
                            "rating":  u_rating,
                            "comment": u_comment
                        })
                        st.success(f"Reseña actualizada: {updated['_id']}")
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

        else:  # modo "Por IDs"
            u_ids      = st.text_input(
                "IDs de reseñas (separados por coma)", key="upd_many_ids"
            )
            u_rating2  = st.slider("Rating (opcional)", 1, 5, 3, key="upd_many_rating")
            u_comment2 = st.text_area("Comentario (opcional)", key="upd_many_comment")
            if st.button("Actualizar múltiples reseñas", key="btn_update_many"):
                # parsear lista de IDs
                ids_list = [i.strip() for i in u_ids.split(",") if i.strip()]
                # armar objeto de actualización
                update_payload = {}
                # sólo agregamos campos que efectivamente cambian
                if u_rating2 is not None:
                    update_payload["rating"] = u_rating2
                if u_comment2:
                    update_payload["comment"] = u_comment2

                if not ids_list:
                    st.error("Debes ingresar al menos un ID válido.")
                elif not update_payload:
                    st.error("Debes especificar Rating o Comentario para actualizar.")
                else:
                    try:
                        res = update_many_reviews_by_ids(ids_list, update_payload)
                        # el API devuelve { message, result }, donde result.modifiedCount es el número
                        count = res.get("result", {}).get("modifiedCount", 0)
                        st.success(f"Se actualizaron {count} reseña(s).")
                    except Exception as e:
                        st.error(f"Error al actualizar múltiples: {e}")

    # ─── 🗑️ Eliminar ──────────────────────────────────────────────────────────
    with tabs[4]:
        st.subheader("🗑️ Eliminar Reseña(s)")

        modo_del = st.radio(
            "Selecciona modo",
            ["Individual", "Por IDs"],
            horizontal=True,
            key="del_mode",
        )

        if modo_del == "Individual":
            d_id = st.text_input("ID de la reseña a eliminar", key="del_id_single")
            if st.button("Eliminar reseña", key="btn_delete_single"):
                if not d_id:
                    st.error("Debes ingresar el ID de la reseña.")
                else:
                    try:
                        resp = delete_review(d_id)
                        st.success(resp.get("message", "Reseña eliminada."))
                    except Exception as e:
                        st.error(f"Error al eliminar reseña: {e}")

        else:  # modo "Por IDs"
            d_ids = st.text_input(
                "IDs de reseñas a eliminar (separados por coma)",
                key="del_many_ids"
            )
            if st.button("Eliminar reseñas", key="btn_delete_many"):
                # Parseamos la lista de IDs
                ids_list = [i.strip() for i in d_ids.split(",") if i.strip()]
                if not ids_list:
                    st.error("Introduce al menos un ID válido.")
                else:
                    try:
                        result = delete_many_reviews_by_ids(ids_list)
                        # El API devuelve { message, result: { deletedCount } }
                        deleted = result.get("result", {}).get("deletedCount", 0)
                        st.success(f"Se eliminaron {deleted} reseña(s).")
                    except Exception as e:
                        st.error(f"Error al eliminar múltiples reseñas: {e}")
