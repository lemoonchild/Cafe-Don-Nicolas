import requests

API_BASE = "http://localhost:3000/api"

def fetch_user_by_id(user_id: str):
    """
    GET /api/users/:id
    """
    r = requests.get(f"{API_BASE}/users/{user_id}")
    r.raise_for_status()
    return r.json()["user"]