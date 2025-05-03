import requests

API_BASE = "http://localhost:3000/api"

def fetch_menu_items(restaurant_id: str = None, limit: int = 10, skip: int = 0):
    params = {"limit": limit, "skip": skip}
    if restaurant_id:
        params["restaurant_id"] = restaurant_id
    r = requests.get(f"{API_BASE}/menu-items", params=params)
    r.raise_for_status()
    return r.json()
    
def fetch_restaurant_name_by_id(restaurant_id):
    res = requests.get(f"{API_BASE}/restaurants/{restaurant_id}")
    if res.status_code == 200:
        return res.json().get("name", f"Restaurante {restaurant_id[:6]}...")
    return "Restaurante Don Nicolás eliminado/desconocido"

def create_menu_item(data):
    res = requests.post(f"{API_BASE}/menu-items", json=data)
    res.raise_for_status()
    return res.json()

def create_many_menu_items(items):
    res = requests.post(f"{API_BASE}/menu-items/create-many", json={"items": items})
    res.raise_for_status()
    return res.json()