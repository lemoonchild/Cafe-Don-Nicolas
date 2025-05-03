import streamlit as st
import requests
import os
from dotenv import load_dotenv

from apiCalls.admin.apiAdminMenuItems import (
    fetch_menu_items,
    fetch_restaurant_name_by_id,
    create_menu_item,
    create_many_menu_items,
)

load_dotenv() 

API_BASE_URL = os.getenv("API_BASE_URL")

def admin_menuitems_page():
    st.header("Gestión de Platos y Bebidas")
    st.write("Administra los platos y bebidas disponibles en el sistema. Puedes crear nuevos registros, editarlos o eliminarlos según sea necesario.")

    tabs = st.tabs(["📄 Ver", "🔍 Filtrar", "➕ Crear", "✏️ Actualizar", "🗑️ Eliminar", "🖼️ Subir Imagen"])

    # === VER MENU ITEMS ===
    with tabs[0]:
        st.subheader("📄 Ver Platos y Bebidas")

        items_per_page = 10

        # Estado inicial
        if "menu_page" not in st.session_state:
            st.session_state.menu_page = 0

        # Cargar total de productos (solo IDs o count para no traer todo)
        total_items = 0
        try:
            count_res = requests.get(f"{API_BASE_URL}menu-items", params={"fields": "_id"})
            if count_res.status_code == 200:
                total_items = len(count_res.json())
        except:
            st.warning("No se pudo calcular el total de productos.")

        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        page = st.session_state.menu_page
        skip = page * items_per_page

        try:
            menu_items = fetch_menu_items(limit=items_per_page, skip=skip)
            if menu_items:
                for item in menu_items:
                    with st.expander(item["name"]):
                        st.markdown(f"**Descripción:** {item.get('description', 'Sin descripción')}")
                        st.markdown(f"**Precio:** Q{item.get('price', 0):.2f}")
                        st.markdown(f"**Categoría:** {item.get('category', 'No especificada')}")
                        st.markdown(f"**Disponible:** {'Sí' if item.get('available') else 'No'}")
                        st.markdown(f"**Ingredientes:** {', '.join(item.get('ingredients', [])) or 'Ninguno'}")

                        restaurant_id = str(item.get("restaurant_id", ""))
                        restaurant_name = fetch_restaurant_name_by_id(restaurant_id) if restaurant_id else "Desconocido"
                        st.markdown(f"**Restaurante:** {restaurant_name} ({restaurant_id})")

                        if item.get("image_url"):
                            st.image(f"http://localhost:3000{item['image_url']}", width=200)

                # Navegación de páginas
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    if st.button("← Anterior", key="prev_menu", disabled=page == 0):
                        st.session_state.menu_page -= 1
                        st.rerun()
                with col3:
                    if st.button("Siguiente →", key="next_menu", disabled=page >= total_pages - 1):
                        st.session_state.menu_page += 1
                        st.rerun()
                with col2:
                    st.markdown(f"<div style='text-align: center;'>Página {page+1} de {total_pages}</div>", unsafe_allow_html=True)
            else:
                st.info("No hay productos registrados.")
        except Exception as e:
            st.error(f"Error al obtener los productos del menú: {e}")

    # === FILTRAR MENU ITEMS ===

    CATEGORIAS = [
        "bebida caliente",
        "bebida fría",
        "postre",
        "snack",
        "desayuno"
    ]

    with tabs[1]:
        st.subheader("🔍 Filtrar Platos y Bebidas")

        # Entradas de filtro
        search = st.text_input("Buscar por palabra clave (nombre, descripción, ingredientes):")
        restaurant_id = st.text_input("ID del restaurante")
        category = st.selectbox("Categoría", ["Cualquiera"] + CATEGORIAS)
        available = st.selectbox("Disponibilidad", ["Cualquiera", "Disponible", "No disponible"])

        # Filtros opcionales activables
        use_price_filter = st.checkbox("Filtrar por precio")
        col1, col2 = st.columns(2)
        with col1:
            price_min = st.number_input("Precio mínimo", min_value=0.0, step=1.0, format="%.2f", disabled=not use_price_filter)
        with col2:
            price_max = st.number_input("Precio máximo", min_value=0.0, step=1.0, format="%.2f", disabled=not use_price_filter)

        ingredients = st.text_input("Ingredientes (separados por coma)")

        sort_field = st.selectbox("Ordenar por", ["name", "price", "category"])
        order = st.radio("Orden", ["asc", "desc"], horizontal=True)

        use_limit = st.checkbox("Aplicar límite de resultados", value=True)
        limit = st.slider("Límite de resultados", min_value=1, max_value=1000, value=10, disabled=not use_limit)
        skip = st.number_input("Saltar registros", min_value=0, step=1)

        if st.button("Aplicar filtros"):
            params = {}

            if search: params["search"] = search
            if restaurant_id: params["restaurant_id"] = restaurant_id
            if category != "Cualquiera": params["category"] = category
            if available != "Cualquiera":
                params["available"] = "true" if available == "Disponible" else "false"
            if use_price_filter:
                if price_min > 0: params["priceMin"] = price_min
                if price_max > 0: params["priceMax"] = price_max
            if ingredients: params["ingredient"] = ingredients
            params["sort"] = sort_field
            params["order"] = order
            if use_limit:
                params["limit"] = limit
                params["skip"] = skip

            response = requests.get(f"{API_BASE_URL}menu-items", params=params)
            if response.status_code == 200:
                items = response.json()
                if items:
                    st.success(f"{len(items)} producto(s) encontrados.")
                    for item in items:
                        with st.expander(item["name"]):
                            st.markdown(f"**Descripción:** {item.get('description', 'Sin descripción')}")
                            st.markdown(f"**Precio:** Q{item.get('price', 0):.2f}")
                            st.markdown(f"**Categoría:** {item.get('category', 'No especificada')}")
                            st.markdown(f"**Disponible:** {'Sí' if item.get('available') else 'No'}")
                            st.markdown(f"**Ingredientes:** {', '.join(item.get('ingredients', [])) or 'Ninguno'}")

                            rid = str(item.get("restaurant_id", ""))
                            rname = fetch_restaurant_name_by_id(rid) if rid else "Desconocido"
                            st.markdown(f"**Restaurante:** {rname} ({rid})")

                            if item.get("image_url"):
                                st.image(f"http://localhost:3000{item['image_url']}", width=200)
                else:
                    st.info("No se encontraron productos con los filtros aplicados.")
            else:
                st.error("Error al consultar productos: " + response.text)


    with tabs[2]:
        st.subheader("➕ Crear Plato o Bebida")

        if st.session_state.get("success_restaurante"):
            st.success("¡Producto creado correctamente!")
            del st.session_state["success_restaurante"]
        
        if "num_menu_forms" not in st.session_state:
            st.session_state.num_menu_forms = 1

        items = []

        for i in range(st.session_state.num_menu_forms):
            with st.expander(f"📝 Producto #{i+1}", expanded=True):
                name = st.text_input("Nombre", key=f"name_{i}")
                description = st.text_area("Descripción", key=f"desc_{i}")
                price = st.number_input("Precio (Q)", min_value=0.0, format="%.2f", key=f"price_{i}")
                ingredients = st.text_input("Ingredientes (separados por coma)", key=f"ing_{i}")
                category = st.selectbox("Categoría", ["bebida caliente", "bebida fría", "postre", "snack", "desayuno"], key=f"cat_{i}")
                available = st.checkbox("Disponible", value=True, key=f"avail_{i}")
                restaurant_id = st.text_input("ID del restaurante", key=f"rest_{i}")

                # Botón para eliminar este formulario
                if st.session_state.num_menu_forms > 1:
                    if st.button(f"🗑️ Eliminar este producto", key=f"delete_menu_{i}"):
                        # Eliminar campos asociados del session_state
                        for key_prefix in ["name", "desc", "price", "ing", "cat", "avail", "rest"]:
                            st.session_state.pop(f"{key_prefix}_{i}", None)
                        st.session_state.num_menu_forms -= 1
                        st.rerun()

                # Guardar temporalmente
                items.append({
                    "name": name.strip(),
                    "description": description.strip(),
                    "price": price,
                    "ingredients": [ing.strip() for ing in ingredients.split(",") if ing.strip()],
                    "category": category,
                    "available": available,
                    "restaurant_id": restaurant_id.strip()
                })

        # Botón para agregar más
        if st.button("➕ Agregar otro producto"):
            st.session_state.num_menu_forms += 1
            st.rerun()

        # Botón para enviar todos
        if st.button("Crear producto(s)"):
            valid_items = [item for item in items if item["name"] and item["price"] > 0 and item["restaurant_id"]]
            if not valid_items:
                st.warning("Debes completar al menos un producto válido (nombre, precio y restaurante).")
            elif len(valid_items) == 1:
                try:
                    res = create_menu_item(valid_items[0])
                    st.session_state.success_restaurante = True
                    st.session_state.num_menu_forms = 1
                    st.rerun()

                except Exception as e:
                    st.error(f"Error al crear producto: {e}")
            else:
                try:
                    res = create_many_menu_items(valid_items)
                    st.session_state.success_restaurante = True
                    st.session_state.num_menu_forms = 1
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al crear productos: {e}")

    with tabs[3]:
        st.subheader("✏️ Actualizar Producto(s)")

        if "success_update_menu" in st.session_state:
            st.success(st.session_state.success_update_menu)
            del st.session_state["success_update_menu"]

        metodo = st.radio("Selecciona el método de actualización:", ["Por ID", "Por múltiples IDs"], horizontal=True)

        if metodo == "Por ID":
            st.markdown("### Actualizar por ID")
            prod_id = st.text_input("ID del producto a actualizar")

            if prod_id and st.button("🔍 Buscar producto"):
                res = requests.get(f"{API_BASE_URL}menu-items/{prod_id}")
                if res.status_code == 200:
                    st.session_state.menu_item_data = res.json()
                    st.session_state.prod_id = prod_id
                    st.rerun()
                else:
                    st.error("Producto no encontrado.")

            if st.session_state.get("menu_item_data") and st.session_state.get("prod_id") == prod_id:
                data = st.session_state.menu_item_data

                nuevo_nombre = st.text_input("Nombre", value=data.get("name", ""), key="edit_name")
                nueva_desc = st.text_area("Descripción", value=data.get("description", ""), key="edit_desc")
                nuevo_precio = st.number_input(
                    "Precio",
                    value=float(data.get("price", 0.0)),
                    format="%.2f",
                    key="edit_price"
                )
                ingredientes = st.text_input("Ingredientes (separados por coma)", value=", ".join(data.get("ingredients", [])), key="edit_ing")
                categoria = st.selectbox("Categoría", ["bebida caliente", "bebida fría", "postre", "snack", "desayuno"], index=0, key="edit_cat")
                disponible = st.checkbox("Disponible", value=data.get("available", True), key="edit_avail")

                if st.button("✏️ Actualizar producto"):
                    update_payload = {
                        "name": nuevo_nombre.strip(),
                        "description": nueva_desc.strip(),
                        "price": nuevo_precio,
                        "ingredients": [i.strip() for i in ingredientes.split(",") if i.strip()],
                        "category": categoria,
                        "available": disponible
                    }
                    res = requests.put(f"{API_BASE_URL}menu-items/{prod_id}", json=update_payload)
                    if res.status_code == 200:
                        st.session_state.success_update_menu = "Producto actualizado correctamente."
                        del st.session_state["menu_item_data"]
                        del st.session_state["prod_id"]
                        st.rerun()
                    else:
                        st.error(f"Error al actualizar: {res.text}")

        elif metodo == "Por múltiples IDs":
            st.markdown("### Actualizar múltiples productos por IDs")
            ids_raw = st.text_area("IDs de productos (separados por coma)")
            ids = [i.strip() for i in ids_raw.split(",") if i.strip()]

            nombre = st.text_input("Nuevo nombre (opcional)")
            desc = st.text_area("Nueva descripción (opcional)")
            precio = st.number_input("Nuevo precio (opcional)", min_value=0.0, format="%.2f")
            ing_multi = st.text_input("Nuevos ingredientes (opcional)")
            cat_multi = st.selectbox("Nueva categoría (opcional)", ["", "bebida caliente", "bebida fría", "postre", "snack", "desayuno"])
            disp_multi = st.selectbox("Disponibilidad (opcional)", ["", "Disponible", "No disponible"])

            update = {"$set": {}}
            if nombre: update["$set"]["name"] = nombre
            if desc: update["$set"]["description"] = desc
            if precio > 0: update["$set"]["price"] = precio
            if ing_multi: update["$set"]["ingredients"] = [i.strip() for i in ing_multi.split(",") if i.strip()]
            if cat_multi: update["$set"]["category"] = cat_multi
            if disp_multi: update["$set"]["available"] = (disp_multi == "Disponible")

            if st.button("Actualizar productos"):
                if not ids or not update["$set"]:
                    st.warning("Debes ingresar al menos un ID y un campo a actualizar.")
                else:
                    res = requests.post(f"{API_BASE_URL}menu-items/update-many-by-ids", json={"ids": ids, "update": update})
                    if res.status_code == 200:
                        st.session_state.success_update_menu = "Productos actualizados correctamente."
                        st.rerun()
                    else:
                        st.error(f"Error: {res.text}")

        # === MANEJO DE INGREDIENTES ===
        st.divider()
        st.subheader("🥄 Manejo de Ingredientes (por ID)")

        st.markdown("Utiliza esta sección para **agregar**, **agregar si no existe** o **eliminar** un ingrediente de un producto del menú, utilizando su ID.")

        ing_menu_id = st.text_input("ID del producto", key="ing_menu_id")
        ing_value = st.text_input("Ingrediente a procesar", key="ing_value")
        ing_op = st.radio("Operación a realizar", ["Agregar", "Agregar (único)", "Eliminar"], horizontal=True)

        if st.button("Procesar ingrediente"):
            if not ing_menu_id or not ing_value:
                st.warning("Debes proporcionar tanto el ID del producto como el ingrediente.")
            else:
                endpoint = None
                if ing_op == "Agregar":
                    endpoint = f"{API_BASE_URL}menu-items/add-ingredient/{ing_menu_id}"
                elif ing_op == "Agregar (único)":
                    endpoint = f"{API_BASE_URL}menu-items/add-ingredient-unique/{ing_menu_id}"
                elif ing_op == "Eliminar":
                    endpoint = f"{API_BASE_URL}menu-items/remove-ingredient/{ing_menu_id}"

                payload = {"ingredient": ing_value}
                res = requests.patch(endpoint, json=payload)

                if res.status_code == 200:
                    msg = res.json().get("message", "Operación realizada correctamente.")
                    st.success(f"{msg}")
                else:
                    st.error(f"Error: {res.text}")

    # === ELIMINAR MENU ITEMS ===
    with tabs[4]:
        st.subheader("🗑️ Eliminar Producto(s) del Menú")

        if st.session_state.get("success_delete_menu"):
            st.success(st.session_state.success_delete_menu)
            del st.session_state["success_delete_menu"]

        modo = st.radio("Selecciona el método de eliminación:", ["Por ID", "Por múltiples IDs"], horizontal=True)

        # === ELIMINAR POR ID ===
        if modo == "Por ID":
            del_id = st.text_input("ID del producto a eliminar")

            if del_id and st.button("🔍 Buscar producto para eliminar"):
                res = requests.get(f"{API_BASE_URL}menu-items/{del_id}")
                if res.status_code == 200:
                    st.session_state.menu_item_to_delete = res.json()
                    st.session_state.pending_menu_delete_id = del_id
                    st.rerun()
                else:
                    st.error("No se encontró el producto con ese ID.")

            if st.session_state.get("menu_item_to_delete") and st.session_state.get("pending_menu_delete_id") == del_id:
                prod = st.session_state.menu_item_to_delete
                with st.expander("Producto encontrado"):
                    st.markdown(f"**Nombre:** {prod.get('name')}")
                    st.markdown(f"**Descripción:** {prod.get('description')}")
                    st.markdown(f"**Precio:** Q{prod.get('price', 0):.2f}")
                    st.markdown(f"**Categoría:** {prod.get('category')}")
                    st.markdown(f"**Ingredientes:** {', '.join(prod.get('ingredients', []))}")
                    if prod.get("image_url"):
                        st.image(f"http://localhost:3000{prod['image_url']}", width=200)

                if st.button("🗑️ Confirmar eliminación"):
                    delete_id = st.session_state.get("pending_menu_delete_id")
                    del_res = requests.delete(f"{API_BASE_URL}menu-items/{delete_id}")
                    if del_res.status_code == 200:
                        st.session_state.success_delete_menu = "Producto eliminado correctamente."
                        del st.session_state["menu_item_to_delete"]
                        del st.session_state["pending_menu_delete_id"]
                        st.rerun()
                    else:
                        st.error(f"Error al eliminar: {del_res.text}")

        # === ELIMINAR POR MÚLTIPLES IDS ===
        elif modo == "Por múltiples IDs":
            ids_raw = st.text_area("IDs de productos a eliminar (separados por coma)")
            ids = [i.strip() for i in ids_raw.split(",") if i.strip()]

            if st.button("🗑️ Eliminar productos seleccionados"):
                if not ids:
                    st.warning("Debes ingresar al menos un ID.")
                else:
                    res = requests.post(f"{API_BASE_URL}menu-items/delete-many-by-ids", json={"ids": ids})
                    if res.status_code == 200:
                        deleted = res.json().get("result", {}).get("deletedCount", len(ids))
                        st.session_state.success_delete_menu = f"Se eliminaron {deleted} producto(s)."
                        st.rerun()
                    else:
                        st.error(f"Error: {res.text}")

    # === SUBIR IMAGEN A MENU ITEM ===
    with tabs[5]:
        st.subheader("🖼️ Subir Imagen a Producto del Menú")

        upload_id = st.text_input("ID del producto del menú")
        image_file = st.file_uploader("Selecciona imagen", type=["png", "jpg", "jpeg"])

        if st.session_state.get("success_upload_menu"):
            st.success(st.session_state.success_upload_menu)
            del st.session_state["success_upload_menu"]

        if st.button("Subir Imagen a Producto"):
            if not upload_id:
                st.warning("Debes ingresar el ID del producto.")
            elif not image_file:
                st.warning("Debes seleccionar una imagen.")
            else:
                files = {"image": (image_file.name, image_file, image_file.type)}
                res = requests.post(f"{API_BASE_URL}menu-items/upload-image/{upload_id}", files=files)

                if res.status_code == 200:
                    result = res.json()
                    if "item" in result and result["item"].get("image_id"):
                        st.session_state.uploaded_menu_image_url = f"{API_BASE_URL}images/{result['item']['image_id']}"
                    st.session_state.success_upload_menu = "Imagen subida correctamente."
                    st.session_state.refresh_menu_items = True
                    st.rerun()
                else:
                    st.error(f"Error: {res.text}")

        if st.session_state.get("uploaded_menu_image_url"):
            st.image(st.session_state.uploaded_menu_image_url, caption="Vista previa de la imagen subida", width=300)
            del st.session_state["uploaded_menu_image_url"]
