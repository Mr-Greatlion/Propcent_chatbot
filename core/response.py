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
        response = (
            "Hello! 👋 I can help you find verified properties, "
            "give investment guidance, and answer real estate questions."
        )

    # ---------------------------------
    # UNIT CONVERSION → AI handles better
    # ---------------------------------

    elif intent == "UNIT_CONVERSION":
        response = ask_gemini(message)

    # ---------------------------------
    # PROPERTY SEARCH → DATABASE ONLY
    # ---------------------------------

    elif intent == "PROPERTY_QUERY":

        properties = fetch_properties(
            city=intent_data.get("city"),
            max_price=intent_data.get("max_price")
        )

        if not properties:
            response = (
                "I couldn't find properties matching your criteria. "
                "Try adjusting your budget or location."
            )
        else:
            response = properties

    # ---------------------------------
    # INVESTMENT + GENERAL → AI THINKS
    # ---------------------------------

    elif intent in ["INVESTMENT_ADVICE", "GENERAL_QUERY"]:
        response = ask_gemini(message)

    # ---------------------------------
    # SAFETY FALLBACK
    # ---------------------------------

    else:
        response = ask_gemini(message)

    # ---------------------------------
    # FINAL PROFESSIONAL POLISH
    # ---------------------------------

    response = ai_refine(response)

    return response

