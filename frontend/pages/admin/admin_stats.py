import streamlit as st
import streamlit.components.v1 as components
from apiCalls.admin.apiAdminStats import (
    get_restaurants_stats, get_users_stats, get_menu_items_stats,
    total_sales, average_order_value, count_orders_by_status,
    orders_with_restaurant, unwind_order_items, get_reviews_stats,
    average_rating_for_restaurant
)

from apiCalls.admin.apiAdminRestaurants import fetch_restaurants


import pandas as pd
import math

def admin_stats_page():
    st.header("📊 Estadísticas Generales")
    resource_tabs = st.tabs([
        "🏠 Restaurantes",
        "👥 Usuarios",
        "🍽 Menu Items",
        "🛒 Orders",
        "🌟 Reviews",
        "🖼 MongoCharts",
    ])

    # ─── Restaurantes ─────────────────────────────────────────────────────────
    with resource_tabs[0]:
        st.subheader("📈 Restaurantes")
        stats = get_restaurants_stats()

        # Métricas disponibles
        st.metric("Total Restaurantes", stats["total"])
        st.metric("Con Imagen",        stats["withImage"])
        st.metric("Abiertos Ahora",    stats["openNow"])

        st.text("Cantidad de Restaurantes Abiertos por su hora de apertura:")
        # Gráfico de barras: número de restaurantes por hora de apertura
        st.bar_chart(stats["countByOpenHour"])

    # ─── Usuarios ────────────────────────────────────────────────────────────
    with resource_tabs[1]:
        st.subheader("📈 Usuarios")

        stats = get_users_stats()
        st.metric("Total Usuarios", stats["total"])
        st.metric("Clientes",      stats["roleCounts"]["cliente"])
        st.metric("Admins",        stats["roleCounts"]["admin"])

    # ─── Menu Items ─────────────────────────────────────────────────────────
    with resource_tabs[2]:
        st.subheader("📈 Estadísticas de Menu Items")
        stats = get_menu_items_stats()

        # Métricas principales
        st.metric("Disponibles",          stats["availableCount"])
        st.metric("Precio promedio (USD)", f"{stats['avgPrice']:.2f}")

        # Precio promedio por categoría
        st.markdown("**Precio promedio por categoría**")
        df_avg_cat = pd.DataFrame(stats["avgPriceByCategory"])\
                    .rename(columns={"_id":"Categoría","avgPrice":"Precio"})
        st.bar_chart(df_avg_cat.set_index("Categoría")["Precio"])

        # Conteo por categoría
        st.markdown("**Conteo por categoría**")
        df_count_cat = pd.DataFrame(stats["countByCategory"])\
                        .rename(columns={"_id":"Categoría","count":"Conteo"})
        st.bar_chart(df_count_cat.set_index("Categoría")["Conteo"])

        # Top 10 ingredientes
        st.markdown("**Top 10 ingredientes**")
        df_ing = pd.DataFrame(stats["topIngredients"])\
                .rename(columns={"_id":"Ingrediente","count":"Veces"})
        st.bar_chart(df_ing.set_index("Ingrediente")["Veces"])

        # Productos por rango de precio
        st.markdown("**Productos por rango de precio**")
        st.markdown(
        """
        Te devuelve un documento por cada “límite” de la lista `boundaries`, donde:

        - `0`:   ítems con 0 ≤ precio < 20  
        - `20`:  ítems con 20 ≤ precio < 40  
        - `40`:  ítems con 40 ≤ precio < 60  
        - … así sucesivamente hasta `100`  
        - **Más de 100**: ítems con precio ≥ 100  
        """
        )
        df_bucket = pd.DataFrame(stats["priceBuckets"])\
                    .rename(columns={"_id":"Rango","count":"Conteo"})
        st.bar_chart(df_bucket.set_index("Rango")["Conteo"])

        # Ítems por restaurante
        st.markdown("**Ítems por restaurante**")
        df_rest = pd.DataFrame(stats["byRestaurant"])\
                    .rename(columns={"name":"Restaurante","count":"Items"})
        st.bar_chart(df_rest.set_index("Restaurante")["Items"])

    # ─── Orders ──────────────────────────────────────────────────────────────
    with resource_tabs[3]:
        st.subheader("📈 Orders")

        # — Métricas globales
        total   = total_sales()
        avg_val = average_order_value()
        by_sta  = count_orders_by_status()
        st.metric("Total Ventas (USD)",   f"${total:.2f}")
        st.metric("Valor Promedio (USD)", f"${avg_val:.2f}")

        # — Órdenes por estado
        st.markdown("**Órdenes por estado**")

        # by_sta puede ser:
        # 1) una lista de dicts [ {'_id':'pendiente','count':123}, ... ]
        # 2) un dict { 'pendiente':123, 'entregado':456, ... }

        if isinstance(by_sta, dict):
            # Caso (2): ya está mapeado status->count
            df_status = pd.DataFrame.from_dict(
                by_sta, orient="index", columns=["Conteo"]
            )
            df_status.index.name = "Estado"
        else:
            # Caso (1): lista de documentos con _id y count
            df_status = (
                pd.DataFrame.from_records(by_sta)
                .rename(columns={"_id":"Estado","count":"Conteo"})
                .set_index("Estado")
            )

        df_status = df_status.sort_values("Conteo", ascending=False)
        st.bar_chart(df_status["Conteo"])

        # — Control de límite
        limit = st.number_input(
            "Máximo de registros a traer",
            min_value=10, max_value=1000, value=50, step=10
        )

        # — Órdenes + Restaurante
        st.markdown("**Órdenes con datos de sucursal**")
        raw_wr = orders_with_restaurant(limit=limit)
        df_wr  = pd.DataFrame(raw_wr)
        # Desanidamos
        df_wr["Sucursal"]  = df_wr["restaurantInfo"].apply(lambda x: x["name"])
        df_wr["Dirección"] = df_wr["restaurantInfo"].apply(lambda x: x["address"])
        df_wr = df_wr[["date","status","total","Sucursal","Dirección"]]

        # Paginación fija a 10 filas/página
        per_page = 10
        total_pages = math.ceil(len(df_wr) / per_page)
        if "wr_page" not in st.session_state:
            st.session_state.wr_page = 0
        page = st.session_state.wr_page

        start, end = page * per_page, (page + 1) * per_page
        st.dataframe(df_wr.iloc[start:end], use_container_width=True)

        col1, col2, col3 = st.columns([1,2,1])
        with col1:
            if st.button("← Anterior", key="wr_prev", disabled=page == 0):
                st.session_state.wr_page -= 1
                st.rerun()
        with col3:
            if st.button("Siguiente →", key="wr_next", disabled=page >= total_pages - 1):
                st.session_state.wr_page += 1
                st.rerun()
        col2.markdown(f"Página {page+1} de {total_pages}")

        # — Detalle de items desenrollados
        st.markdown("**Detalle de items de órdenes**")
        raw_it = unwind_order_items(limit=limit)
        df_it  = pd.DataFrame(raw_it)
        df_it["Cliente"]   = df_it["userInfo"].apply(lambda u: u["name"])
        df_it["Sucursal"]  = df_it["restaurantInfo"].apply(lambda r: r["name"])
        df_it["Item"]      = df_it["items"].apply(lambda it: it["name"])
        df_it["Cantidad"]  = df_it["items"].apply(lambda it: it["quantity"])
        df_it["Precio U."] = df_it["items"].apply(lambda it: it["unit_price"])
        df_it = df_it[["date","status","Cliente","Sucursal","Item","Cantidad","Precio U."]]

        # Misma paginación de 10 filas
        total_pages_it = math.ceil(len(df_it) / per_page)
        if "it_page" not in st.session_state:
            st.session_state.it_page = 0
        page_it = st.session_state.it_page
        start_it, end_it = page_it * per_page, (page_it + 1) * per_page

        st.dataframe(df_it.iloc[start_it:end_it], use_container_width=True)

        col1, col2, col3 = st.columns([1,2,1])
        with col1:
            if st.button("← Anterior Items", key="it_prev", disabled=page_it == 0):
                st.session_state.it_page -= 1
                st.rerun()
        with col3:
            if st.button("Siguiente Items →", key="it_next", disabled=page_it >= total_pages_it - 1):
                st.session_state.it_page += 1
                st.rerun()
        col2.markdown(f"Página {page_it+1} de {total_pages_it}")

    # # ─── Reviews ─────────────────────────────────────────────────────────────
    with resource_tabs[4]:
        st.subheader("📈 Reviews")

        # 1) Primeramente, elige un restaurante para ver su rating:
        restos = fetch_restaurants()
        # Creamos opciones “Nombre (ID)” para que el usuario vea ambas cosas
        options = [f"{r['name']} ({r['_id']})" for r in restos]
        sel = st.selectbox("Selecciona un Restaurante", options)

        # Extraemos el _id de la opción seleccionada
        sel_id = sel.split("(")[-1].rstrip(")")

        avg = average_rating_for_restaurant(sel_id)
        if avg is None:
            st.info("Este restaurante aún no tiene reviews.")
        else:
            st.metric(f"⭐ Rating promedio de {sel.split(' (')[0]}", f"{avg:.2f}/5")

        st.markdown("---")
        # 2) Métrico global de total de reviews + gráfico
        stats = get_reviews_stats()

        st.metric("Total Reseñas", stats["total"])
        st.markdown("**Reseñas por Restaurante**")
        df_rev = (
            pd.DataFrame(stats["countByRestaurant"])
              .rename(columns={"restaurantName": "Restaurante", "count": "Conteo"})
              .set_index("Restaurante")
              .sort_values("Conteo", ascending=False)
        )
        st.bar_chart(df_rev["Conteo"])
    
        # ─── MongoCharts ──────────────────────────────────────────────────────────
    with resource_tabs[5]:
        st.subheader("🖼 MongoDB Charts Embebidos")

        # Chart 1
        components.html(
            """
            <iframe 
              style="background: #21313C;border: none;border-radius: 2px;
                     box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" 
              width="640" height="480"
              src="https://charts.mongodb.com/charts-project-0-vrznjzi/embed/charts?id=21a0a0e5-390f-4d30-a4b3-cf5a195b5ffa&maxDataAge=3600&theme=dark&autoRefresh=true">
            </iframe>
            """,
            height=500
        )

        # Chart 2
        components.html(
            """
            <iframe 
              style="background: #21313C;border: none;border-radius: 2px;
                     box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" 
              width="640" height="480"
              src="https://charts.mongodb.com/charts-project-0-vrznjzi/embed/charts?id=a70fe192-2de3-41f5-aa02-1012e3217d86&maxDataAge=3600&theme=dark&autoRefresh=true">
            </iframe>
            """,
            height=500
        )

        # Chart 3
        components.html(
            """
            <iframe 
              style="background: #21313C;border: none;border-radius: 2px;
                     box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2);" 
              width="640" height="480"
              src="https://charts.mongodb.com/charts-project-0-vrznjzi/embed/charts?id=935f8a69-d8ea-41c3-99c6-283369872e94&maxDataAge=3600&theme=dark&autoRefresh=true">
            </iframe>
            """,
            height=500
        )


