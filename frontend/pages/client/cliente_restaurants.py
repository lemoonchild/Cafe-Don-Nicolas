import streamlit as st
from api import fetch_restaurants, fetch_menu_items, create_order

def cliente_restaurants_page():
    st.header("📍 Restaurantes Cercanos")
    restos = fetch_restaurants()  # podrías pasar near, maxDistance…
    for r in restos:
        with st.expander(r["name"]):
            st.write(f"📍 {r['address']}")
            if st.button("Ver Menú", key=r["_id"]):
                st.session_state.sel_restaurant = r
                st.experimental_rerun()

    if "sel_restaurant" in st.session_state:
        r = st.session_state.sel_restaurant
        st.subheader(f"Menú de {r['name']}")
        items = fetch_menu_items(r["_id"])
        cart = st.session_state.get("cart", {})
        cols = st.columns((3,1,1))
        for it in items:
            cols[0].write(it["name"])
            cols[1].write(f"Q{it['price']}")
            qty = cols[2].number_input("Cant.", 0, 10, key=it["_id"])
            if qty > 0:
                cart[it["_id"]] = {"item": it, "qty": qty}
        if st.button("Agregar al carrito"):
            st.session_state.cart = cart
            st.success("Carrito actualizado")
        if cart and st.button("Realizar Pedido"):
            payload = {
                "user_id": st.session_state.user["_id"],
                "restaurant_id": r["_id"],
                "items": [
                    {
                        "product_id": v["item"]["_id"],
                        "name": v["item"]["name"],
                        "quantity": v["qty"],
                        "unit_price": v["item"]["price"]
                    } for v in cart.values()
                ],
                "total": sum(v["qty"]*v["item"]["price"] for v in cart.values())
            }
            create_order(payload)
            st.success("Pedido creado")
            st.session_state.pop("cart", None)
