import json
from pathlib import Path

DATA_FILE = Path("data/properties.json")

def load_properties():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def find_verified_properties(city=None, max_price=None):
    properties = load_properties()
    results = []

    for p in properties:
        if city and city.lower() not in p["location"].lower():
            continue
        if max_price and p["price_value"] > max_price:
            continue
        results.append(p)

    return results
