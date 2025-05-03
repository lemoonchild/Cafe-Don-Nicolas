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
                # Parsear fecha
                dt = datetime.datetime.fromisoformat(rev["date"].replace("Z",""))
                fecha_str = dt.strftime("%d/%m/%Y %H:%M")

                st.markdown(f"**ID:** {rev['_id']}")
                st.markdown(f"- **Usuario:** {user['name']} ({rev['user_id']})")  
                st.markdown(f"- **Restaurante:** {rest['name']} ({rev['restaurant_id']})")  
                if rev.get("order_id"):
                    st.markdown(f"- **Orden relacionada:** {rev['order_id']}")
                st.markdown(f"- **Rating:** {rev['rating']}/5")
                st.markdown(f"- **Fecha:** {fecha_str}")
                st.markdown(f"- **Comentario:** {rev.get('comment','')}")
                st.markdown("---")

            col1, col2, col3 = st.columns([1,2,1])
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
                        st.markdown(f"- **Usuario:** {user} ({rev["user_id"]})  ")
                        st.markdown(f"- **Restaurante:** {rest} ({rev["restaurant_id"]})  ")
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
                                st.markdown(f"- **Usuario:** {user} ({rev["user_id"]})  ")
                            elif field == "restaurant_id":
                                st.markdown(f"- **Restaurante:** {rest} ({rev["restaurant_id"]})  ")
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
