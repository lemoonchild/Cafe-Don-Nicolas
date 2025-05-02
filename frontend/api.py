import requests

API_BASE = "http://localhost:3000/api"

def get_user_by_email(email: str):
    r = requests.get(f"{API_BASE}/users", params={"email": email})
    r.raise_for_status()
    data = r.json().get("users") or r.json()
    return data[0] if isinstance(data, list) and data else None

def fetch_restaurants(**params):
    r = requests.get(f"{API_BASE}/restaurants", params=params)
    r.raise_for_status()
    return r.json()

def fetch_menu_items(restaurant_id: str):
    r = requests.get(f"{API_BASE}/menu-items", params={"restaurant_id": restaurant_id})
    r.raise_for_status()
    return r.json()

def create_order(payload: dict):
    r = requests.post(f"{API_BASE}/orders", json=payload)
    r.raise_for_status()
    return r.json()

def fetch_orders_for_user(user_id: str):
    r = requests.get(f"{API_BASE}/orders", params={"user_id": user_id})
    r.raise_for_status()
    return r.json()

def create_review(payload: dict):
    r = requests.post(f"{API_BASE}/reviews", json=payload)
    r.raise_for_status()
    return r.json()
