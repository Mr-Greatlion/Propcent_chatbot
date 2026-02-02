import re

def detect_intent_and_filters(message: str):
    msg = message.strip().lower()

    # -------------------------------
    # 1️⃣ GREETING (FIRST)
    # -------------------------------
    if msg in ["hi", "hello", "hey", "hai"]:
        return {
            "intent": "GREETING",
            "city": None,
            "max_price": None
        }

    # -------------------------------
    # 2️⃣ UNIT / AREA CONVERSION (SECOND)
    # -------------------------------
    if any(word in msg for word in [
        "sq feet", "sqft", "square feet",
        "cent", "cents",
        "acre", "acres",
        "square meter", "sqm"
    ]):
        return {
            "intent": "UNIT_CONVERSION",
            "city": None,
            "max_price": None
        }

    # -------------------------------
    # 3️⃣ PROPERTY SEARCH (LAST)
    # -------------------------------
    city = None
    max_price = None

    if "chennai" in msg:
        city = "Chennai"

    lakh_match = re.search(r"(\d+)\s*(l|lakh|lakhs)", msg)
    crore_match = re.search(r"(\d+)\s*(c|cr|crore|crores)", msg)

    if lakh_match:
        max_price = int(lakh_match.group(1)) * 100000
    elif crore_match:
        max_price = int(crore_match.group(1)) * 10000000

    return {
        "intent": "PROPERTY_QUERY",
        "city": city,
        "max_price": max_price
    }
