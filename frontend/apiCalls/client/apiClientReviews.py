import requests

API_BASE = "http://localhost:3000/api"

def fetch_reviews(user_id=None, **params):
    if user_id:
        params["user_id"] = user_id
    r = requests.get(f"{API_BASE}/reviews", params=params)
    r.raise_for_status()
    return r.json()

def fetch_reviews_with_filters(
    restaurant_id: str = None,
    user_id: str = None,
    order_id: str = None,
    rating: int = None,
    ratingMin: int = None,
    ratingMax: int = None,
    search: str = None,
    sort: str = None,
    order: str = None,
    limit: int = None,
    skip: int = None,
    fields: str = None,
):
    params = {}
    if restaurant_id: params["restaurant_id"] = restaurant_id
    if user_id:       params["user_id"]       = user_id
    if order_id:      params["order_id"]      = order_id
    if rating is not None:   params["rating"]      = rating
    if ratingMin is not None: params["ratingMin"]   = ratingMin
    if ratingMax is not None: params["ratingMax"]   = ratingMax
    if search:        params["search"]        = search
    if sort:          params["sort"]          = sort
    if order:         params["order"]         = order
    if limit is not None:    params["limit"]       = limit
    if skip is not None:     params["skip"]        = skip
    if fields:        params["fields"]        = fields

    r = requests.get(f"{API_BASE}/reviews", params=params)
    r.raise_for_status()
    return r.json()


def fetch_review_by_id(review_id: str):
    """GET /api/reviews/:id"""
    r = requests.get(f"{API_BASE}/reviews/{review_id}")
    r.raise_for_status()
    return r.json()

def create_review(payload: dict):
    """POST /api/reviews"""
    r = requests.post(f"{API_BASE}/reviews", json=payload)
    r.raise_for_status()
    return r.json()

def update_review(review_id: str, payload: dict):
    """PUT /api/reviews/:id"""
    r = requests.put(f"{API_BASE}/reviews/{review_id}", json=payload)
    r.raise_for_status()
    return r.json()

def delete_review(review_id: str):
    """DELETE /api/reviews/:id"""
    r = requests.delete(f"{API_BASE}/reviews/{review_id}")
    r.raise_for_status()
    return r.json()

def create_many_reviews(items: list):
    """
    POST /api/reviews/create-many
    Body: { "items": [ { ... }, ... ] }
    """
    r = requests.post(f"{API_BASE}/reviews/create-many", json={"items": items})
    r.raise_for_status()
    return r.json()

def update_many_reviews(filter_: dict, update: dict):
    """
    POST /api/reviews/update-many
    Body: { "filter": { ... }, "update": { ... } }
    """
    r = requests.post(
        f"{API_BASE}/reviews/update-many",
        json={"filter": filter_, "update": update}
    )
    r.raise_for_status()
    return r.json()

def update_many_reviews_by_ids(ids: list, update: dict):
    """
    POST /api/reviews/update-many-by-ids
    Body: { "ids": [...], "update": { ... } }
    """
    r = requests.post(
        f"{API_BASE}/reviews/update-many-by-ids",
        json={"ids": ids, "update": update}
    )
    r.raise_for_status()
    return r.json()

def delete_many_reviews(filter_: dict):
    """
    POST /api/reviews/delete-many
    Body: { "filter": { ... } }
    """
    r = requests.post(f"{API_BASE}/reviews/delete-many", json={"filter": filter_})
    r.raise_for_status()
    return r.json()

def delete_many_reviews_by_ids(ids: list):
    """
    POST /api/reviews/delete-many-by-ids
    Body: { "ids": [...] }
    """
    r = requests.post(f"{API_BASE}/reviews/delete-many-by-ids", json={"ids": ids})
    r.raise_for_status()
    return r.json()
