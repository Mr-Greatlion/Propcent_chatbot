import json
from pathlib import Path


# -------------------------------------------------
# SAFE ABSOLUTE PATH
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "properties.json"


# -------------------------------------------------
# LOAD ONCE INTO MEMORY (VERY FAST)
# -------------------------------------------------

def load_properties():

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

            # Ensure price is numeric
            for prop in data:
                prop["price"] = int(prop.get("price", 0))

            return data

    except Exception as e:
        print("PROPERTY LOAD ERROR:", e)
        return []


PROPERTIES = load_properties()


# -------------------------------------------------
# FETCH FILTERED PROPERTIES
# -------------------------------------------------

def fetch_properties(city=None, max_price=None):

    results = PROPERTIES

    if city:
        results = [
            p for p in results
            if p.get("city", "").lower() == city.lower()
        ]

    if max_price:
        results = [
            p for p in results
            if p.get("price", 0) <= max_price
        ]

    return results


# -------------------------------------------------
# PROPERTY COUNT (VERY IMPORTANT)
# -------------------------------------------------

def get_property_count(city=None):

    if city:
        return len([
            p for p in PROPERTIES
            if p.get("city", "").lower() == city.lower()
        ])

    return len(PROPERTIES)


# -------------------------------------------------
# FORMAT FOR CHATBOT (PRETTY OUTPUT)
# -------------------------------------------------

def format_properties(properties):

    if not properties:
        return None

    formatted = []

    for p in properties[:5]:   # limit to top 5 (VERY IMPORTANT)

        formatted.append(
            f"🏡 **{p.get('title')}**\n"
            f"📍 {p.get('location')}\n"
            f"💰 ₹{p.get('price'):,}\n"
        )

    more = ""

    if len(properties) > 5:
        more = f"\n👉 Showing 5 of {len(properties)} properties."

    return "\n".join(formatted) + more
