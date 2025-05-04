# === apiCalls/admin/apiAdminOrders.py ===
import requests

API_BASE = "http://localhost:3000/api"

def fetch_orders(user_id=None, limit=10, skip=0):
    params = {"limit": limit, "skip": skip}
    if user_id:
        params["user_id"] = user_id
    response = requests.get(f"{API_BASE}/orders", params=params)
    response.raise_for_status()
    return response.json()

def fetch_restaurant_name_by_id(restaurant_id):
    try:
        res = requests.get(f"{API_BASE}/restaurants/{restaurant_id}")
        if res.status_code == 200:
            return res.json().get("name", f"Restaurante {restaurant_id[:6]}...")
    except:
        pass
    return "Restaurante Don Nicolás eliminado/desconocido"

def fetch_user_name_by_id(user_id):
    try:
        res = requests.get(f"{API_BASE}/users/{user_id}")
        if res.status_code == 200:
            data = res.json()
            return data.get("user", {}).get("name", f"Usuario {user_id[:6]}...")
    except:
        pass
    return "Usuario eliminado/desconocido"

