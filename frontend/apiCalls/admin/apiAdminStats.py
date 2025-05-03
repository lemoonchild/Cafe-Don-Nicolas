import requests

API_BASE = "http://localhost:3000/api"

def count_restaurants() -> int:
    """GET /api/restaurants/count"""
    r = requests.get(f"{API_BASE}/restaurants/stats/count")
    r.raise_for_status()
    return r.json()["total"]

def count_restaurants_with_image() -> int:
    """GET /api/restaurants/count-with-image"""
    r = requests.get(f"{API_BASE}/restaurants/stats/count-with-image")
    r.raise_for_status()
    return r.json()["total"]

def count_restaurants_open_now() -> int:
    """GET /api/restaurants/open-now"""
    r = requests.get(f"{API_BASE}/restaurants/stats/count-open-now")
    r.raise_for_status()
    return r.json()["openNow"]

def group_restaurants_by_open_hour() -> list[dict]:
    """
    GET /api/restaurants/group-by-open-hour
    Devuelve lista de { hour: "HH:mm", count: n }
    """
    r = requests.get(f"{API_BASE}/restaurants/stats/group-by-hour")
    r.raise_for_status()
    return r.json()

def get_restaurants_stats() -> dict:
    """
    Recolecta todas las métricas de restaurante en un solo dict:
      - total: conteo total
      - withImage: cuántos tienen imagen
      - openNow: cuántos están abiertos
      - countByOpenHour: dict mapeando hora->conteo
    """
    total       = count_restaurants()
    with_image  = count_restaurants_with_image()
    open_now    = count_restaurants_open_now()
    by_open_raw = group_restaurants_by_open_hour()
    # convertimos a { hour: count }
    count_by_open_hour = { item["hour"]: item["count"] for item in by_open_raw }

    return {
        "total": total,
        "withImage": with_image,
        "openNow": open_now,
        "countByOpenHour": count_by_open_hour
    }

def count_users() -> int:
    """GET /api/users/count"""
    r = requests.get(f"{API_BASE}/users/stats/count")
    r.raise_for_status()
    return r.json()["total"]

def count_users_by_role() -> dict[str, int]:
    """GET /api/users/count-by-role
    Devuelve lista de { role: str, count: int }"""
    r = requests.get(f"{API_BASE}/users/stats/count-by-role")
    r.raise_for_status()
    arr = r.json()  # e.g. [ {role:"cliente",count:23}, {role:"admin",count:5} ]
    return { item["role"]: item["count"] for item in arr }

def get_users_stats() -> dict:
    """
    Recolecta estadísticas de usuarios:
      - total: int
      - roleCounts: { cliente: int, admin: int, … }
    """
    total      = count_users()
    role_counts = count_users_by_role()
    # Aseguramos que existan ambas claves
    return {
        "total": total,
        "roleCounts": {
            "cliente": role_counts.get("cliente", 0),
            "admin":   role_counts.get("admin",   0),
        }
    }


def count_menu_items_available() -> int:
    available = requests.get(f"{API_BASE}/menu-items/stats/count-available").json()["count"]
    return available

def average_price_menu_items() -> float:
    r = requests.get(f"{API_BASE}/menu-items/stats/avg-price")
    r.raise_for_status()
    return r.json()["avgPrice"]


def count_by_category() -> list[dict]:
    r = requests.get(f"{API_BASE}/menu-items/stats/count-by-category")
    r.raise_for_status()
    return r.json()  # [{category, count}, …]

def avg_price_by_category() -> list[dict]:
    r = requests.get(f"{API_BASE}/menu-items/stats/avg-price-by-category")
    r.raise_for_status()
    return r.json()  # [{category, avgPrice}, …]

def top_ingredients() -> list[dict]:
    """GET /api/menu-items/stats/top-ingredients"""
    r = requests.get(f"{API_BASE}/menu-items/stats/top-ingredients")
    r.raise_for_status()
    # retorna { ingredient: "...", count: N }
    return r.json()

def price_range_menu_items() -> list[dict]:
    """GET /api/menu-items/stats/price-range"""
    r = requests.get(f"{API_BASE}/menu-items/stats/price-range")
    r.raise_for_status()
    # retorna { _id: "<bucket>", count: N } o similar
    return r.json()

def menu_items_by_restaurant() -> list[dict]:
    """GET /api/menu-items/stats/by-restaurant"""
    r = requests.get(f"{API_BASE}/menu-items/stats/by-restaurant")
    r.raise_for_status()
    # retorna { restaurantId, name, count }
    return r.json()

def get_menu_items_stats() -> dict:
    """
    Compila todas las métricas de MenuItems en un solo dict:
      - total
      - availableCount
      - avgPrice
      - avgPriceByCategory
      - countByCategory
      - topIngredients
      - priceBuckets
      - byRestaurant
    """
    available   = count_menu_items_available()
    avgPrice    = average_price_menu_items()
    avgByCat    = avg_price_by_category()
    cntByCat    = count_by_category()
    topIngr     = top_ingredients()
    priceRanges = price_range_menu_items()
    byRest      = menu_items_by_restaurant()

    return {
        "availableCount": available,
        "avgPrice": avgPrice,
        "avgPriceByCategory": avgByCat,
        "countByCategory": cntByCat,
        "topIngredients": topIngr,
        "priceBuckets": priceRanges,
        "byRestaurant": byRest,
    }

def total_sales() -> float:
    """GET /api/orders/stats/total-sales → {"totalSales": number}"""
    r = requests.get(f"{API_BASE}/orders/stats/total-sales")
    r.raise_for_status()
    return r.json().get("totalSales", 0.0)

def average_order_value() -> float:
    """GET /api/orders/stats/avg-order-value → {"avgOrderValue": number}"""
    r = requests.get(f"{API_BASE}/orders/stats/avg-order-value")
    r.raise_for_status()
    return r.json().get("avgOrderValue", 0.0)

def count_orders_by_status() -> dict[str,int]:
    """GET /api/orders/stats/count-by-status → [{ _id: status, count: n }, …]"""
    r = requests.get(f"{API_BASE}/orders/stats/count-by-status")
    r.raise_for_status()
    lst = r.json()
    # convertir lista de docs a mapping estado→conteo
    return { item["_id"]: item["count"] for item in lst }

def orders_with_restaurant(limit: int = 10) -> list[dict]:
    """
    GET /api/orders/stats/with-restaurant?limit={limit}
    Devuelve una lista de documentos con:
      { total, status, date, restaurantInfo: { name, address } }
    """
    r = requests.get(
        f"{API_BASE}/orders/stats/with-restaurant",
        params={"limit": limit}
    )
    r.raise_for_status()
    return r.json()

def unwind_order_items(limit: int = 10) -> list[dict]:
    """
    GET /api/orders/stats/unwind-items?limit={limit}
    Devuelve una lista de documentos "desenrollados" de items:
      { user_id, userInfo: { name },
        restaurant_id, restaurantInfo: { name, address },
        items: { name, quantity, unit_price },
        date, status }
    """
    r = requests.get(
        f"{API_BASE}/orders/stats/unwind-items",
        params={"limit": limit}
    )
    r.raise_for_status()
    return r.json()

def get_orders_stats() -> dict:
    """
    Junta todas las métricas de Orders:
      - totalSales
      - avgOrderValue
      - countByStatus
      - withRestaurant: lista resumida (limit=10)
      - itemsDetail: lista desenrollada (limit=10)
    """
    from .apiAdminStats import total_sales, average_order_value, count_orders_by_status

    total   = total_sales()
    avg_val = average_order_value()
    by_sta  = count_orders_by_status()
    with_res = orders_with_restaurant(limit=10)
    items_det = unwind_order_items(limit=10)

    return {
        "totalSales":    total,
        "avgOrderValue": avg_val,
        "countByStatus": by_sta,
        "withRestaurant": with_res,
        "itemsDetail":    items_det
    }

def count_reviews_by_restaurant() -> list[dict]:
    """
    GET /api/reviews/stats/count-by-restaurant
    Devuelve lista de { _id: ObjectId, count: n, restaurantName: string }
    """
    r = requests.get(f"{API_BASE}/reviews/stats/count-by-restaurant")
    r.raise_for_status()
    return r.json()

def average_rating_for_restaurant(restaurant_id: str) -> float | None:
    """
    GET /api/reviews/stats/average-rating/:restaurantId
    Devuelve avgRating o None si no hay reseñas.
    """
    url = f"{API_BASE}/reviews/stats/average-rating/{restaurant_id}"
    r = requests.get(url)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json().get("avgRating")

def get_reviews_stats() -> dict:
    """
    Recolecta estadísticas de reviews:
      - total: suma de todas las reviews
      - countByRestaurant: lista de { restaurantName, count }
    """
    by_rest = count_reviews_by_restaurant()
    total = sum(item["count"] for item in by_rest)
    # Transformamos para frontend si quisiéramos
    return {
        "total": total,
        "countByRestaurant": by_rest
    }