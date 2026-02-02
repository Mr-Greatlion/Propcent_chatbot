from services.property_data import find_verified_properties
from services.ai_engine import ai_refine
from core.intent import detect_intent_and_filters


def generate_response(message: str):
    # 🔒 ALWAYS extract values first
    data = detect_intent_and_filters(message)

    intent = data.get("intent")
    city = data.get("city")          # ✅ FIXED
    max_price = data.get("max_price")  # ✅ FIXED

    # -------------------------------
    # GREETING
    # -------------------------------
    if intent == "GREETING":
        return (
            "Hello! 👋\n\n"
            "I can help you find verified properties and answer real-estate questions.\n\n"
            "Try asking:\n"
            "• Properties under 1 crore\n"
            "• 2 BHK flats below 90 lakhs\n"
            "• Area and unit conversions"
        )

    # -------------------------------
    # UNIT CONVERSION
    # -------------------------------
    if intent == "UNIT_CONVERSION":
        return (
            "Here are common real-estate unit conversions:\n\n"
            "• 1 square foot = 0.0929 square meters\n"
            "• 1 cent = 435.6 square feet\n"
            "• 1 acre = 43,560 square feet\n"
            "• 1 square meter = 10.764 square feet\n\n"
            "If you want a specific conversion, please tell me."
        )

    # -------------------------------
    # PROPERTY SEARCH
    # -------------------------------
    verified = find_verified_properties(city, max_price)

    if verified:
        lines = ["Here are the verified properties matching your requirement:\n"]

        for p in verified[:5]:
            lines.append(
                f"• {p['bhk']} BHK in {p['location']} – ₹{p['price']}"
            )

        lines.append(
            "\nThese listings are verified from our property database.\n"
            "Would you like to refine this further by budget, location, or BHK?"
        )

        return ai_refine("\n".join(lines))

    # -------------------------------
    # SAFE FALLBACK
    # -------------------------------
    return (
        "Currently, we do not have verified properties matching this request.\n\n"
        "You can try a different budget, location, or ask about area conversions."
    )
