import re


def detect_intent_and_filters(message: str):

    msg = message.lower().strip()

    # -------------------------------------------------
    # GREETING
    # -------------------------------------------------

    if msg in ["hi", "hello", "hey", "hai"]:
        return {"intent": "GREETING"}

    # -------------------------------------------------
    # PROPERTY COUNT (VERY IMPORTANT)
    # -------------------------------------------------

    if "how many" in msg and (
        "property" in msg or
        "properties" in msg or
        "listing" in msg
    ):
        return {"intent": "PROPERTY_COUNT"}

    # -------------------------------------------------
    # UNIT CONVERSION
    # -------------------------------------------------

    if any(word in msg for word in [
        "sqft", "square feet", "sq feet",
        "cent", "acre",
        "sqm", "square meter"
    ]):
        return {"intent": "UNIT_CONVERSION"}

    # -------------------------------------------------
    # Detect City
    # -------------------------------------------------

    city = None

    if "chennai" in msg:
        city = "Chennai"

    # (Later you can add Bangalore, Hyderabad etc)

    # -------------------------------------------------
    # Detect Budget
    # -------------------------------------------------

    lakh_match = re.search(r"(\d+)\s*(lakh|lakhs|l)\b", msg)
    crore_match = re.search(r"(\d+)\s*(crore|crores|cr|c)\b", msg)

    max_price = None

    if lakh_match:
        max_price = int(lakh_match.group(1)) * 100000

    elif crore_match:
        max_price = int(crore_match.group(1)) * 10000000

    # -------------------------------------------------
    # PROPERTY SEARCH (STRONG VERSION)
    # -------------------------------------------------

    property_words = [
        "property",
        "properties",
        "house",
        "home",
        "flat",
        "apartment",
        "villa",
        "plot",
        "land",
        "bhk",
        "buy"
    ]

    if any(word in msg for word in property_words):

        return {
            "intent": "PROPERTY_QUERY",
            "city": city,
            "max_price": max_price
        }

    # -------------------------------------------------
    # INVESTMENT (Only if NOT property search)
    # -------------------------------------------------

    investment_words = [
        "investment",
        "roi",
        "growth",
        "future",
        "appreciation",
        "best area",
        "hot area"
    ]

    if any(word in msg for word in investment_words):

        return {
            "intent": "INVESTMENT_ADVICE",
            "city": city
        }

    # -------------------------------------------------
    # FALLBACK → AI
    # -------------------------------------------------

    return {"intent": "GENERAL_QUERY"}
