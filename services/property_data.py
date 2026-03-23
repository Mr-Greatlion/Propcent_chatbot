# =====================================================
# PROPCENT PROPERTY DATA ENGINE — V6 (FULL PRODUCTION)
# Clean • Safe • Scalable • No Duplicate Functions
# =====================================================

import json
from pathlib import Path
from typing import List, Dict, Optional


# -------------------------------------------------
# PATH CONFIGURATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "properties.json"


# -------------------------------------------------
# PROPERTY LOADER
# -------------------------------------------------

def load_properties() -> List[Dict]:

    if not DATA_FILE.exists():
        print("❌ ERROR: properties.json file not found")
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        cleaned_data = []

        for prop in raw_data:

            # ---------------------------
            # SAFE FIELD EXTRACTION
            # ---------------------------

            try:
                price = int(prop.get("price", 0))
            except:
                price = 0

            try:
                area = int(prop.get("area_sqft", 0))
            except:
                area = 0

            try:
                bhk = int(prop.get("bhk", 0))
            except:
                bhk = 0

            cleaned_property = {
                "title": str(prop.get("title", "Property")).strip(),
                "city": str(prop.get("city", "")).strip(),
                "location": str(prop.get("location", "")).strip(),
                "price": price,
                "bhk": bhk,
                "area_sqft": area,
                "builder": str(prop.get("builder", "N/A")).strip(),
                "possession": str(prop.get("possession", "N/A")).strip(),
                "url": str(prop.get("url", "")).strip()
            }

            cleaned_data.append(cleaned_property)

        print(f"✅ SUCCESS: Loaded {len(cleaned_data)} properties into memory")
        return cleaned_data

    except Exception as e:
        print("❌ PROPERTY LOAD FAILED:", e)
        return []


# -------------------------------------------------
# GLOBAL MEMORY CACHE (VERY FAST)
# -------------------------------------------------

PROPERTIES = load_properties()


# -------------------------------------------------
# PROPERTY COUNT FUNCTION
# -------------------------------------------------

def get_property_count(city: Optional[str] = None) -> int:

    if not PROPERTIES:
        return 0

    if city:
        return sum(
            1 for p in PROPERTIES
            if city.lower() in p["city"].lower()
        )

    return len(PROPERTIES)


# -------------------------------------------------
# MAIN SEARCH ENGINE (SMART MATCHING)
# -------------------------------------------------

def fetch_properties(
    city: Optional[str] = None,
    max_price: Optional[int] = None,
    bhk: Optional[int] = None,
    raw_query: Optional[str] = None
) -> List[Dict]:

    if not PROPERTIES:
        return []

    query = (raw_query or "").lower()

    scored_results = []

    for p in PROPERTIES:

        score = 0

        city_text = p["city"].lower()
        location_text = p["location"].lower()
        title_text = p["title"].lower()

        # ---------------------------
        # LOCATION MATCH (HIGH PRIORITY)
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
            score += 25

        if "plot" in query and "plot" in title_text:
            score += 25

        if "apartment" in query or "flat" in query:
            if "apartment" in title_text or "flat" in title_text:
                score += 20

        # ---------------------------
        # BHK MATCH
        # ---------------------------
        if bhk and p["bhk"] == bhk:
            score += 20

        # ---------------------------
        # PRICE MATCH
        # ---------------------------
        if max_price:
            if p["price"] <= max_price:
                score += 30
            elif p["price"] <= max_price * 1.2:
                score += 10  # near budget

        # ---------------------------
        # MINIMUM QUALITY FILTER
        # ---------------------------
        if score > 0:
            scored_results.append((score, p))

    # ---------------------------
    # SORT RESULTS (BEST FIRST)
    # ---------------------------
    scored_results.sort(key=lambda x: x[0], reverse=True)

    # ---------------------------
    # FILTER QUALITY LEVELS
    # ---------------------------
    strong = [p for s, p in scored_results if s >= 60]
    medium = [p for s, p in scored_results if 30 <= s < 60]

    if strong:
        return strong

    if medium:
        return medium

    return []


# -------------------------------------------------
# SMART BUDGET PARSER
# -------------------------------------------------

def parse_budget(text: str) -> Optional[int]:

    if not text:
        return None

    msg = text.lower()

    # Crore detection
    if "crore" in msg or "cr" in msg:
        return 10000000

    # Lakh detection
    if "lakh" in msg or "lac" in msg:
        return 100000

    return None


# -------------------------------------------------
# DEBUG FUNCTION (OPTIONAL)
# -------------------------------------------------

def debug_sample():

    print("\n🔍 DEBUG TEST RUN")

    results = fetch_properties(
        city="Chennai",
        max_price=10000000,
        bhk=2,
        raw_query="2bhk in omr"
    )

    for p in results[:3]:
        print(p)


# -------------------------------------------------
# RUN DEBUG
# -------------------------------------------------

if __name__ == "__main__":
    debug_sample()
