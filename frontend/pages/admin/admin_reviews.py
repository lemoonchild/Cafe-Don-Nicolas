import streamlit as st

def admin_reviews_page():
    st.header("Gestión de Reviews")
    st.write("Administra las reseñas dejadas por los usuarios. Puedes crear nuevas reseñas, editarlas o eliminarlas según sea necesario.")
    st.subheader("Reseñas registradas:")
    # Aquí iría la lógica para mostrar las reseñas registradas, posiblemente usando un fetch a la API