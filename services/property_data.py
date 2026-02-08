import json
from pathlib import Path


DATA_FILE = Path("data/properties.json")


# -------------------------------------------------
# LOAD ONCE (FAST)
# -------------------------------------------------

def load_properties():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


# ⭐ Cached in memory
PROPERTIES = load_properties()


# -------------------------------------------------
# FETCH FILTERED PROPERTIES
# -------------------------------------------------

def fetch_properties(city=None, max_price=None):

    results = PROPERTIES

    # Filter by city
    if city:
        results = [
            p for p in results
            if p.get("city", "").lower() == city.lower()
        ]

    # Filter by price
    if max_price:
        results = [
            p for p in results
            if p.get("price", 0) <= max_price
        ]

    return results  # ALWAYS return list
