# =====================================================
# PROPCENT PROPERTY DATA ENGINE — V4.5 (REALTIME READY)
# Smart Location + Keyword Property Search
# =====================================================

import json
from pathlib import Path


# -------------------------------------------------
# SAFE ABSOLUTE PATH
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "properties.json"


# -------------------------------------------------
# LOAD PROPERTIES INTO MEMORY (ONCE)
# -------------------------------------------------

def load_properties():

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            cleaned = []

            for prop in data:

                # Safe numeric conversion
                try:
                    price = int(prop.get("price", 0))
                except:
                    price = 0

                cleaned.append({
                    "title": prop.get("title", "Property"),
                    "city": prop.get("city", "").strip(),
                    "location": prop.get("location", "").strip(),
                    "price": price,
                    "bhk": prop.get("bhk"),
                    "area_sqft": prop.get("area_sqft"),
                    "url": prop.get("url", "")
                })

            print(f"✅ Loaded {len(cleaned)} properties into memory")

            return cleaned

    except FileNotFoundError:
        print("❌ properties.json not found")
        return []

    except Exception as e:
        print("PROPERTY LOAD ERROR:", e)
        return []


# Global RAM cache (FAST)
PROPERTIES = load_properties()


# -------------------------------------------------
# SMART LOCATION MATCH
# -------------------------------------------------

def location_match(property_item, query):

    q = query.lower()

    return (
        q in property_item["city"].lower()
        or q in property_item["location"].lower()
        or q in property_item["title"].lower()
    )


# -------------------------------------------------
# FETCH FILTERED PROPERTIES (SMART SEARCH)
# -------------------------------------------------

def fetch_properties(city=None, max_price=None, bhk=None, raw_query=None):

    results = PROPERTIES

    # ---------------------------------------
    # SMART TEXT SEARCH (REAL ESTATE STYLE)
    # ---------------------------------------

    if raw_query:
        query_words = raw_query.lower().split()

        results = [
            p for p in results
            if any(location_match(p, word) for word in query_words)
        ]

    # ---------------------------------------
    # CITY FILTER (IF STRONGLY DETECTED)
    # ---------------------------------------

    if city:
        results = [
            p for p in results
            if city.lower() in p["city"].lower()
        ]

    # ---------------------------------------
    # PRICE FILTER
    # ---------------------------------------

    if max_price:
        results = [
            p for p in results
            if p["price"] <= max_price
        ]

    # ---------------------------------------
    # BHK FILTER
    # ---------------------------------------

    if bhk:
        results = [
            p for p in results
            if str(p.get("bhk")) == str(bhk)
        ]

    return results


# -------------------------------------------------
# PROPERTY COUNT
# -------------------------------------------------

def get_property_count(city=None):

    if city:
        return sum(
            1 for p in PROPERTIES
            if city.lower() in p["city"].lower()
        )

    return len(PROPERTIES)


# -------------------------------------------------
# FORMAT FOR CHATBOT
# -------------------------------------------------

def fetch_properties(city=None, max_price=None, bhk=None, raw_query=None):

    if not PROPERTIES:
        return []

    query = (raw_query or "").lower()

    results = []

    # -----------------------------------------
    # SCORING SYSTEM (REAL ESTATE SEARCH)
    # -----------------------------------------

    for p in PROPERTIES:

        score = 0

        city_text = p["city"].lower()
        location_text = p["location"].lower()
        title_text = p["title"].lower()

        # ---------------------------
        # LOCATION MATCH (80%)
        # ---------------------------
        if query:
            if city_text in query:
                score += 50
            if location_text in query:
                score += 40

        # ---------------------------
        # PROPERTY TYPE MATCH
        # ---------------------------
        if "villa" in query and "villa" in title_text:
            score += 20

        if "plot" in query and "plot" in title_text:
            score += 20

        if "apartment" in query or "flat" in query:
            if "apartment" in title_text or "flat" in title_text:
                score += 20

        # ---------------------------
        # BHK MATCH
        # ---------------------------
        if bhk and str(p.get("bhk")) == str(bhk):
            score += 15

        # ---------------------------
        # PRICE MATCH
        # ---------------------------
        price = p["price"]

        if max_price:
            if price <= max_price:
                score += 25
            elif price <= max_price * 1.2:
                score += 10  # slightly above budget

        results.append((score, p))

    # -----------------------------------------
    # SORT BY BEST MATCH
    # -----------------------------------------

    results.sort(key=lambda x: x[0], reverse=True)

    # -----------------------------------------
    # FILTER QUALITY RESULTS
    # -----------------------------------------

    strong_matches = [p for s, p in results if s >= 60]
    medium_matches = [p for s, p in results if 30 <= s < 60]

    if strong_matches:
        return strong_matches

    if medium_matches:
        return medium_matches

    return []


# -------------------------------------------------
# SMART PRICE PARSER
# -------------------------------------------------

def parse_budget(text: str):

    if not text:
        return None

    msg = text.lower()

    if "crore" in msg or "cr" in msg:
        return 10000000

    if "lakh" in msg or "lac" in msg:
        return 1000000

    return None
