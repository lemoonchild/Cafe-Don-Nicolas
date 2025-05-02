import streamlit as st
from api import fetch_restaurants, create_review

def cliente_reviews_page():
    st.header("✍️ Dejar Reseña")
    restos = fetch_restaurants()
    sel = st.selectbox("Restaurante", [r["name"] for r in restos])
    rating  = st.slider("Calificación", 1, 5, 3)
    comment = st.text_area("Comentario")
    if st.button("Enviar Reseña"):
        r = next(filter(lambda x: x["name"]==sel, restos))
        create_review({
            "user_id": st.session_state.user["_id"],
            "restaurant_id": r["_id"],
            "rating": rating,
            "comment": comment
        })
        st.success("Reseña enviada")
