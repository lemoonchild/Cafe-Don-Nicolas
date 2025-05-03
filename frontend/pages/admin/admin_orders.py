import streamlit as st
import requests
import os
from api import fetch_menu_items 
from dotenv import load_dotenv

load_dotenv() 

API_BASE_URL = os.getenv("API_BASE_URL")

def admin_orders_page():
    st.header("Gestión de Ordenes")
    st.write("Administra las ordenes realizadas por los usuarios. Puedes crear nuevas ordenes, editarlas o eliminarlas según sea necesario.")

    tabs = st.tabs(["📄 Ver", "🔍 Filtrar", "➕ Crear", "✏️ Actualizar", "🗑️ Eliminar", "🖼️ Subir Imagen"])
