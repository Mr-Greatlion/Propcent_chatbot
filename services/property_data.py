import json


DATA_FILE = "data/properties.json"


# -------------------------------------------------
# LOAD ALL PROPERTIES
# -------------------------------------------------

def load_properties():

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    except Exception:
        return []


# -------------------------------------------------
# FETCH FILTERED PROPERTIES
# -------------------------------------------------

def fetch_properties(city=None, max_price=None):

    properties = load_properties()

    results = []

    for prop in properties:

        # Filter by city
        if city and prop.get("city", "").lower() != city.lower():
            continue

        # Filter by price
        if max_price and prop.get("price", 0) > max_price:
            continue

        results.append(prop)

    # No matches
    if not results:
        return None

    # Format nicely for AI / user
    formatted = []

    for p in results:

        formatted.append(
            f"• {p.get('title')} — ₹{p.get('price'):,}\n"
            f"Location: {p.get('location')}"
        )

    return "\n\n".join(formatted)
