import requests

API_BASE = "http://localhost:3000/api"

def fetch_users(
    search: str = None,
    role: str = None,
    email: str = None,
    hasLocation: bool = None,
    near: str = None,
    maxDistance: int = None,
    sort: str = None,
    order: str = None,
    limit: int = None,
    skip: int = None,
    fields: str = None,
):
    """
    GET /api/users
    Parámetros opcionales: search, role, email, hasLocation, near, maxDistance,
    sort, order, limit, skip, fields
    """
    params = {}
    if search is not None:    params["search"]      = search
    if role is not None:      params["role"]        = role
    if email is not None:     params["email"]       = email
    if hasLocation is not None:
        # si quieres forzar que exista campo location
        params["hasLocation"] = "true"
    if near is not None:      params["near"]        = near
    if maxDistance is not None:
        params["maxDistance"] = maxDistance
    if sort is not None:      params["sort"]        = sort
    if order is not None:     params["order"]       = order
    if limit is not None:     params["limit"]       = limit
    if skip is not None:      params["skip"]        = skip
    if fields is not None:    params["fields"]      = fields

    r = requests.get(f"{API_BASE}/users", params=params)
    r.raise_for_status()
    data = r.json()
    # dependiendo de si vino pipeline geo, devuelvo result o users
    return data.get("users") or data.get("result")




def fetch_user_by_id(user_id: str):
    """
    GET /api/users/:id
    """
    r = requests.get(f"{API_BASE}/users/{user_id}")
    r.raise_for_status()
    return r.json()["user"]

def create_user(payload: dict):
    """
    POST /api/users
    Body: { ...campos del usuario... }
    """
    r = requests.post(f"{API_BASE}/users", json=payload)
    r.raise_for_status()
    return r.json()["user"]


def update_user(user_id: str, payload: dict):
    """
    PUT /api/users/:id
    Body: { ...campos a actualizar... }
    """
    r = requests.put(f"{API_BASE}/users/{user_id}", json=payload)
    r.raise_for_status()
    return r.json()["user"]


def delete_user(user_id: str):
    """
    DELETE /api/users/:id
    """
    r = requests.delete(f"{API_BASE}/users/{user_id}")
    r.raise_for_status()
    return r.json()["msg"]


def create_many_users(items: list):
    """
    POST /api/users/create-many
    Body: { "items": [ { ...usuario1... }, { ...usuario2... } ] }
    """
    r = requests.post(f"{API_BASE}/users/create-many", json={"items": items})
    r.raise_for_status()
    return r.json()


def update_many_users(filter_: dict, update: dict):
    """
    POST /api/users/update-many
    Body: { "filter": {...}, "update": {...} }
    """
    r = requests.post(
        f"{API_BASE}/users/update-many",
        json={"filter": filter_, "update": update}
    )
    r.raise_for_status()
    return r.json()


def update_many_users_by_ids(ids: list, update: dict):
    """
    POST /api/users/update-many-by-ids
    Body: { "ids": [...], "update": {...} }
    """
    r = requests.post(
        f"{API_BASE}/users/update-many-by-ids",
        json={"ids": ids, "update": update}
    )
    r.raise_for_status()
    return r.json()


def delete_many_users(filter_: dict):
    """
    POST /api/users/delete-many
    Body: { "filter": {...} }
    """
    r = requests.post(f"{API_BASE}/users/delete-many", json={"filter": filter_})
    r.raise_for_status()
    return r.json()


def delete_many_users_by_ids(ids: list):
    """
    POST /api/users/delete-many-by-ids
    Body: { "ids": [...] }
    """
    r = requests.post(f"{API_BASE}/users/delete-many-by-ids", json={"ids": ids})
    r.raise_for_status()
    return r.json()