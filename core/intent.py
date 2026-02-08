import re


def detect_intent_and_filters(message: str):
    msg = message.strip().lower()

    # -------------------------------
    # 1️⃣ GREETING
    # -------------------------------
    if msg in ["hi", "hello", "hey", "hai"]:
        return {
            "intent": "GREETING",
            "city": None,
            "max_price": None
        }

    # -------------------------------
    # 2️⃣ UNIT / AREA CONVERSION
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
    # 3️⃣ INVESTMENT / AREA ADVICE ⭐⭐⭐
    # -------------------------------
    investment_keywords = [
        "best area",
        "investment",
        "roi",
        "growth",
        "future",
        "appreciation",
        "where should i buy",
        "good area",
        "hot locations"
    ]

    if any(word in msg for word in investment_keywords):
        return {
            "intent": "INVESTMENT_ADVICE",
            "city": "Chennai" if "chennai" in msg else None,
            "max_price": None
        }

    # -------------------------------
    # 4️⃣ PROPERTY SEARCH
    # -------------------------------
    property_keywords = [
        "bhk", "flat", "apartment",
        "house", "villa",
        "budget", "under", "price"
    ]

    if any(word in msg for word in property_keywords):

        city = "Chennai" if "chennai" in msg else None

        lakh_match = re.search(r"(\d+)\s*(l|lakh|lakhs)", msg)
        crore_match = re.search(r"(\d+)\s*(c|cr|crore|crores)", msg)

        max_price = None

        if lakh_match:
            max_price = int(lakh_match.group(1)) * 100000
        elif crore_match:
            max_price = int(crore_match.group(1)) * 10000000

        return {
            "intent": "PROPERTY_QUERY",
            "city": city,
            "max_price": max_price
        }

    # -------------------------------
    # 5️⃣ GENERAL AI QUESTION ⭐⭐⭐
    # -------------------------------
    return {
        "intent": "GENERAL_QUERY",
        "city": None,
        "max_price": None
    }

