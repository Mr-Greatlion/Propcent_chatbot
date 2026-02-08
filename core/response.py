from core.intent import detect_intent_and_filters
from services.ai_engine import ask_gemini, ai_refine
from services.property_data import fetch_properties


def generate_response(message: str) -> str:

    intent_data = detect_intent_and_filters(message)
    intent = intent_data.get("intent")

    # ---------------------------------
    # GREETING
    # ---------------------------------

    if intent == "GREETING":
        return (
            "Hello! 👋 I can help you find verified properties, "
            "provide investment guidance, and answer real estate questions."
        )

    # ---------------------------------
    # UNIT CONVERSION → AI GOOD HERE
    # ---------------------------------

    if intent == "UNIT_CONVERSION":
        return ask_gemini(message)

    # ---------------------------------
    # PROPERTY SEARCH → DATABASE ONLY
    # ---------------------------------

    if intent == "PROPERTY_QUERY":

        properties = fetch_properties(
            city=intent_data.get("city"),
            max_price=intent_data.get("max_price")
        )

        if not properties:
            return (
                "I couldn't find verified properties matching your criteria. "
                "Try increasing your budget or changing the location."
            )

        # ✅ FORMAT HERE (NOT in service)
        reply = "Here are some verified properties:\n\n"

        for p in properties[:5]:

            price_lakh = p["price"] / 100000

            reply += (
                f"• {p.get('title')} — ₹{price_lakh:.0f} Lakhs\n"
                f"Location: {p.get('location')}\n\n"
            )

        # ✅ Only refine DATABASE responses
        return ai_refine(reply)

    # ---------------------------------
    # AI KNOWLEDGE QUESTIONS
    # ---------------------------------

    if intent in ["INVESTMENT_ADVICE", "GENERAL_QUERY"]:
        return ask_gemini(message)

    # ---------------------------------
    # FALLBACK
    # ---------------------------------

    return ask_gemini(message)
