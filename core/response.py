# =====================================================
# PROPCENT RESPONSE ENGINE — V7 (STRUCTURED API READY)
# UI Friendly • Stable • Production Safe
# =====================================================

from core.intent import detect_intent_and_filters
from services.ai_engine import ask_gemini
from services.property_data import (
    fetch_properties,
    get_property_count
)


# -------------------------------------------------
# MAIN RESPONSE GENERATOR (STRUCTURED OUTPUT)
# -------------------------------------------------

def generate_response(message: str) -> dict:

    try:

        # -------------------------------------------------
        # EMPTY INPUT GUARD
        # -------------------------------------------------

        if not message or not message.strip():
            return {
                "reply": "Please type your property requirement so I can assist you.",
                "replyType": "text"
            }

        intent_data = detect_intent_and_filters(message)
        intent = intent_data.get("intent")

        # -------------------------------------------------
        # GREETING
        # -------------------------------------------------

        if intent == "GREETING":
            return {
                "reply": (
                    "Hello! 👋 I help you find verified properties, "
                    "investment opportunities, and real estate insights.\n\n"
                    "Try asking:\n"
                    "• 2BHK below 1 crore in Chennai\n"
                    "• Villa in ECR\n"
                    "• Property in OMR\n"
                    "• Best investment areas"
                ),
                "replyType": "text"
            }

        # -------------------------------------------------
        # PROPERTY COUNT
        # -------------------------------------------------

        if intent == "PROPERTY_COUNT":

            city = intent_data.get("city")
            count = get_property_count(city)

            if city:
                return {
                    "reply": f"📊 We currently have {count} verified properties in {city}.",
                    "replyType": "text"
                }

            return {
                "reply": f"📊 We currently have {count} verified properties available.",
                "replyType": "text"
            }

        # -------------------------------------------------
        # UNIT CONVERSION
        # -------------------------------------------------

        if intent == "UNIT_CONVERSION":
            return {
                "reply": ask_gemini(message),
                "replyType": "text"
            }

        # -------------------------------------------------
        # PROPERTY SEARCH (MAIN FEATURE)
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

                return {
                    "reply": "Here are verified properties matching your requirement",
                    "replyType": "property_list",
                    "properties": [
                        {
                            "title": p.get("title"),
                            "location": p.get("location"),
                            "builder": p.get("builder"),
                            "area_sqft": p.get("area_sqft"),
                            "bhk": p.get("bhk"),
                            "price_in_lakhs": int(p.get("price", 0) / 100000),
                            "possession": p.get("possession"),
                            "url": p.get("url")
                        }
                        for p in properties[:5]
                    ],
                    "totalShown": min(5, len(properties)),
                    "totalAvailable": len(properties)
                }

            # ---------------------------------------------
            # FALLBACK (SIMILAR PROPERTIES)
            # ---------------------------------------------

            alternative_props = fetch_properties(
                max_price=intent_data.get("max_price"),
                bhk=intent_data.get("bhk")
            )

            if alternative_props:

                return {
                    "reply": "No exact match found. Here are similar properties within your budget",
                    "replyType": "property_list",
                    "properties": [
                        {
                            "title": p.get("title"),
                            "location": p.get("location"),
                            "builder": p.get("builder"),
                            "area_sqft": p.get("area_sqft"),
                            "bhk": p.get("bhk"),
                            "price_in_lakhs": int(p.get("price", 0) / 100000),
                            "possession": p.get("possession"),
                            "url": p.get("url")
                        }
                        for p in alternative_props[:3]
                    ],
                    "totalShown": min(3, len(alternative_props)),
                    "totalAvailable": len(alternative_props)
                }

            return {
                "reply": "Sorry, I couldn't find matching properties. Try changing location, budget, or BHK.",
                "replyType": "text"
            }

        # -------------------------------------------------
        # INVESTMENT / GENERAL AI
        # -------------------------------------------------

        if intent in ["INVESTMENT_ADVICE", "GENERAL_QUERY"]:
            return {
                "reply": ask_gemini(message),
                "replyType": "text"
            }

        # -------------------------------------------------
        # FINAL FALLBACK
        # -------------------------------------------------

        return {
            "reply": "I specialize in property-related queries. Ask about properties, locations, budget, or investment advice.",
            "replyType": "text"
        }

    except Exception as e:

        print("❌ RESPONSE ENGINE ERROR:", e)

        return {
            "reply": "Something went wrong while processing your request. Please try again.",
            "replyType": "text"
        }
