import requests

API_BASE = "http://localhost:3000/api"

def fetch_restaurant_by_id(restaurant_id: str):
    r = requests.get(f"{API_BASE}/restaurants/{restaurant_id}")
    r.raise_for_status()
    return r.json()

def fetch_restaurants(**params):
    r = requests.get(f"{API_BASE}/restaurants", params=params)
    r.raise_for_status()
    return r.json()