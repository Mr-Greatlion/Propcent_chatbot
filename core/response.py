# =====================================================
# PROPCENT RESPONSE ENGINE — V6 (FULL PRODUCTION READY)
# Clean • Detailed • No Errors • UI Ready
# =====================================================

from core.intent import detect_intent_and_filters
from services.ai_engine import ask_gemini
from services.property_data import (
    fetch_properties,
    get_property_count
)


# -------------------------------------------------
# SAFE FORMATTER FOR PROPERTY DISPLAY
# -------------------------------------------------

def format_property(p: dict) -> str:

    try:
        price = p.get("price", 0)
        price_lakh = price / 100000 if price else 0

        return (
            f"🏡 {p.get('title', 'Property')}\n"
            f"📍 Location: {p.get('location', 'N/A')}\n"
            f"🏢 Builder: {p.get('builder', 'N/A')}\n"
            f"📐 Area: {p.get('area_sqft', 'N/A')} sqft\n"
            f"🛏 BHK: {p.get('bhk', 'N/A')}\n"
            f"💰 Price: ₹{price_lakh:.0f} Lakhs\n"
            f"📅 Possession: {p.get('possession', 'N/A')}\n"
            f"🔗 {p.get('url', '')}\n"
            f"────────────────────────\n"
        )

    except Exception as e:
        print("FORMAT ERROR:", e)
        return "⚠️ Error displaying property\n"


# -------------------------------------------------
# MAIN RESPONSE GENERATOR
# -------------------------------------------------

def generate_response(message: str) -> str:

    try:

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
                return f"📊 We currently have {count} verified properties in {city}."

            return f"📊 We currently have {count} verified properties available."

        # -------------------------------------------------
        # UNIT CONVERSION
        # -------------------------------------------------

        if intent == "UNIT_CONVERSION":
            return ask_gemini(message)

        # -------------------------------------------------
        # PROPERTY SEARCH
        # -------------------------------------------------

        if intent == "PROPERTY_QUERY":

            properties = fetch_properties(
                city=intent_data.get("city"),
                max_price=intent_data.get("max_price"),
                bhk=intent_data.get("bhk"),
                raw_query=message
            )

            # ---------------------------------------------
            # MATCH FOUND
            # ---------------------------------------------

            if properties:

                reply = "🏘️ Here are verified properties matching your requirement:\n\n"

                for p in properties[:5]:
                    reply += format_property(p)

                if len(properties) > 5:
                    reply += f"\n👉 Showing 5 of {len(properties)} properties."

                return reply

            # ---------------------------------------------
            # SMART FALLBACK
            # ---------------------------------------------

            alternative_props = fetch_properties(
                max_price=intent_data.get("max_price"),
                bhk=intent_data.get("bhk")
            )

            if alternative_props:

                reply = (
                    "⚠️ No exact match found in that location.\n\n"
                    "Here are similar properties within your budget:\n\n"
                )

                for p in alternative_props[:3]:
                    reply += format_property(p)

                return reply

            return (
                "❌ Sorry, I couldn't find matching properties.\n"
                "Try changing location, budget, or BHK."
            )

        # -------------------------------------------------
        # INVESTMENT / GENERAL AI
        # -------------------------------------------------

        if intent in ["INVESTMENT_ADVICE", "GENERAL_QUERY"]:
            return ask_gemini(message)

        # -------------------------------------------------
        # FINAL FALLBACK
        # -------------------------------------------------

        return (
            "I specialize in property-related queries.\n"
            "Ask about properties, locations, budget, or investment advice."
        )

    except Exception as e:

        print("❌ RESPONSE ENGINE ERROR:", e)

        return (
            "⚠️ Something went wrong while processing your request.\n"
            "Please try again."
        )
