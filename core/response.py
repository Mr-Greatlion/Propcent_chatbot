# =====================================================
# PROPCENT RESPONSE ENGINE — V4.5 (REALTIME PRODUCTION)
# Real Estate Advisor Behaviour
# =====================================================

from core.intent import detect_intent_and_filters
from services.ai_engine import ask_gemini
from services.property_data import (
    fetch_properties,
    get_property_count
)


# -------------------------------------------------
# MAIN RESPONSE GENERATOR
# -------------------------------------------------

def generate_response(message: str) -> str:

    # -------------------------------------------------
    # EMPTY INPUT GUARD
    # -------------------------------------------------

    if not message or not message.strip():
        return "Please type your property requirement so I can assist you."

    intent_data = detect_intent_and_filters(message)
    intent = intent_data.get("intent")

    # -------------------------------------------------
    # GREETING
    # -------------------------------------------------

    if intent == "GREETING":
        return (
            "Hello! 👋 I help you find verified properties, "
            "investment opportunities, and real estate insights.\n\n"
            "Try asking:\n"
            "• 2BHK below 1 crore in Chennai\n"
            "• Villa in ECR\n"
            "• Property in OMR\n"
            "• Best investment areas"
        )

    # -------------------------------------------------
    # PROPERTY COUNT
    # -------------------------------------------------

    if intent == "PROPERTY_COUNT":

        city = intent_data.get("city")
        count = get_property_count(city)

        if city:
            return f"We currently have {count} verified properties in {city}."

        return f"We currently have {count} verified properties available."

    # -------------------------------------------------
    # UNIT CONVERSION
    # -------------------------------------------------

    if intent == "UNIT_CONVERSION":
        return ask_gemini(message)

    # -------------------------------------------------
    # PROPERTY SEARCH (SMART REAL ESTATE SEARCH)
    # -------------------------------------------------

    if intent == "PROPERTY_QUERY":

        properties = fetch_properties(
            city=intent_data.get("city"),
            max_price=intent_data.get("max_price"),
            bhk=intent_data.get("bhk"),
            raw_query=message   # ⭐ IMPORTANT (SMART SEARCH)
        )

        # ---------------------------------------------
        # IF MATCH FOUND
        # ---------------------------------------------

        if properties:

            reply = "Here are some verified properties matching your requirement:\n\n"

            for p in properties[:5]:

                price_lakh = p.get("price", 0) / 100000

                reply += (
                    f"🏡 {p.get('title','Property')}\n"
                    f"📍 {p.get('location','Location not specified')}\n"
                    f"💰 ₹{price_lakh:.0f} Lakhs\n\n"
                )

            if len(properties) > 5:
                reply += f"👉 Showing 5 of {len(properties)} properties."

            return reply

        # ---------------------------------------------
        # SMART FALLBACK (REAL AGENT STYLE)
        # ---------------------------------------------

        alternative_props = fetch_properties(
            max_price=intent_data.get("max_price"),
            bhk=intent_data.get("bhk")
        )

        if alternative_props:

            reply = (
                "Sorry, I don't currently have verified properties in that exact location.\n\n"
                "However, here are some similar properties within your budget:\n\n"
            )

            for p in alternative_props[:3]:

                price_lakh = p.get("price", 0) / 100000

                reply += (
                    f"🏡 {p.get('title')}\n"
                    f"📍 {p.get('location')}\n"
                    f"💰 ₹{price_lakh:.0f} Lakhs\n\n"
                )

            return reply

        return (
            "Sorry, I couldn't find matching properties right now. "
            "Please try adjusting your budget or property type."
        )

    # -------------------------------------------------
    # INVESTMENT / GENERAL AI QUESTIONS
    # -------------------------------------------------

    if intent in ["INVESTMENT_ADVICE", "GENERAL_QUERY"]:
        return ask_gemini(message)

    # -------------------------------------------------
    # FINAL FALLBACK
    # -------------------------------------------------

    return (
        "I specialize in property-related queries.\n"
        "Please ask about properties, budgets, locations, or investments."
    )
