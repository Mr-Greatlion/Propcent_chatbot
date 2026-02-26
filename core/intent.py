# =====================================================
# PROPCENT INTENT ENGINE — V4 (PRODUCTION READY)
# Fast rule-based intent detection
# =====================================================

import re


# -------------------------------------------------
# SUPPORTED DATA
# -------------------------------------------------

SUPPORTED_CITIES = {
    "chennai": "Chennai",
    "bangalore": "Bangalore",
    "bengaluru": "Bangalore",
    "hyderabad": "Hyderabad"
}

GREETING_WORDS = ["hi", "hello", "hey", "hai"]


PROPERTY_KEYWORDS = [
    "property", "properties", "house", "home",
    "flat", "apartment", "villa",
    "plot", "land", "bhk", "buy", "sale"
]


INVESTMENT_KEYWORDS = [
    "investment", "roi", "growth",
    "future", "appreciation",
    "best area", "hot area"
]


UNIT_KEYWORDS = [
    "sqft", "square feet", "sq feet",
    "cent", "acre",
    "sqm", "square meter", "square metre"
]


# -------------------------------------------------
# SPELL CORRECTION (VERY IMPORTANT FOR USERS)
# -------------------------------------------------

def normalize_text(msg: str):

    fixes = {
        "properts": "properties",
        "propets": "properties",
        "crour": "crore",
        "lak": "lakh",
        "sq ft": "sqft"
    }

    msg = msg.lower()

    for wrong, correct in fixes.items():
        msg = msg.replace(wrong, correct)

    return msg.strip()


# -------------------------------------------------
# CITY DETECTION
# -------------------------------------------------

def detect_city(msg: str):

    for key, value in SUPPORTED_CITIES.items():
        if key in msg:
            return value

    return None


# -------------------------------------------------
# BUDGET DETECTION
# -------------------------------------------------

def detect_budget(msg: str):

    lakh_match = re.search(r"(\d+)\s*(lakh|lakhs|l)\b", msg)
    crore_match = re.search(r"(\d+)\s*(crore|crores|cr|c)\b", msg)

    if lakh_match:
        return int(lakh_match.group(1)) * 100000

    if crore_match:
        return int(crore_match.group(1)) * 10000000

    return None


# -------------------------------------------------
# BHK DETECTION
# -------------------------------------------------

def detect_bhk(msg: str):

    bhk_match = re.search(r"(\d+)\s*bhk", msg)

    if bhk_match:
        return bhk_match.group(1)

    return None


# -------------------------------------------------
# MAIN INTENT DETECTOR
# -------------------------------------------------

def detect_intent_and_filters(message: str):

    if not message:
        return {"intent": "GENERAL_QUERY"}

    msg = normalize_text(message)

    # -----------------------------
    # GREETING
    # -----------------------------
    if msg in GREETING_WORDS:
        return {"intent": "GREETING"}

    # -----------------------------
    # PROPERTY COUNT
    # -----------------------------
    if "how many" in msg and any(
        w in msg for w in ["property", "properties", "listing"]
    ):
        return {"intent": "PROPERTY_COUNT"}

    # -----------------------------
    # UNIT CONVERSION
    # -----------------------------
    if any(word in msg for word in UNIT_KEYWORDS):
        return {"intent": "UNIT_CONVERSION"}

    # -----------------------------
    # Extract Filters
    # -----------------------------
    city = detect_city(msg)
    max_price = detect_budget(msg)
    bhk = detect_bhk(msg)

    # -----------------------------
    # PROPERTY SEARCH
    # -----------------------------
    if any(word in msg for word in PROPERTY_KEYWORDS):

        return {
            "intent": "PROPERTY_QUERY",
            "city": city,
            "max_price": max_price,
            "bhk": bhk
        }

    # -----------------------------
    # INVESTMENT ADVICE
    # -----------------------------
    if any(word in msg for word in INVESTMENT_KEYWORDS):

        return {
            "intent": "INVESTMENT_ADVICE",
            "city": city
        }

    # -----------------------------
    # FALLBACK
    # -----------------------------
    return {
        "intent": "GENERAL_QUERY",
        "city": city,
        "max_price": max_price,
        "bhk": bhk
    }
