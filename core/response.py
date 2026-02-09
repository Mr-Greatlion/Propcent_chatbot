from core.intent import detect_intent_and_filters
from services.ai_engine import ask_gemini, ai_refine
from services.property_data import fetch_properties, get_property_count


def generate_response(message: str) -> str:

    # -------------------------------------------------
    # Empty Guard (VERY IMPORTANT)
    # -------------------------------------------------

    if not message or len(message.strip()) == 0:
        return "Please type your property requirement so I can assist you."

    intent_data = detect_intent_and_filters(message)
    intent = intent_data.get("intent")

    # -------------------------------------------------
    # GREETING
    # -------------------------------------------------

    if intent == "GREETING":
        return (
            "Hello! 👋 I help you find verified properties, "
            "investment opportunities, and real estate insights."
        )

    # -------------------------------------------------
    # PROPERTY COUNT (DATABASE ONLY)
    # -------------------------------------------------

    if intent == "PROPERTY_COUNT":

        count = get_property_count()

        return f"We currently have {count} verified properties available."

    # -------------------------------------------------
    # UNIT CONVERSION → AI GOOD HERE
    # -------------------------------------------------

    if intent == "UNIT_CONVERSION":
        return ask_gemini(message)

    # -------------------------------------------------
    # PROPERTY SEARCH → STRICT DATABASE
    # -------------------------------------------------

    if intent == "PROPERTY_QUERY":

        properties = fetch_properties(
            city=intent_data.get("city"),
            max_price=intent_data.get("max_price")
        )

        if not properties:
            return (
                "I couldn't find verified properties matching your criteria. "
                "Try adjusting your budget or location."
            )

        reply = "Here are some verified properties:\n\n"

        for p in properties[:5]:

            price_lakh = p["price"] / 100000

            reply += (
                f"🏡 {p.get('title')}\n"
                f"📍 {p.get('location')}\n"
                f"💰 ₹{price_lakh:.0f} Lakhs\n\n"
            )

        # ⭐ Tell user if more exist
        if len(properties) > 5:
            reply += f"👉 Showing 5 of {len(properties)} properties."

        # ⭐ Only refine DB responses
        return ai_refine(reply)

    # -------------------------------------------------
    # AI KNOWLEDGE (SAFE ZONE)
    # -------------------------------------------------

    if intent in ["INVESTMENT_ADVICE", "GENERAL_QUERY"]:
        return ask_gemini(message)

    # -------------------------------------------------
    # FINAL FALLBACK
    # -------------------------------------------------

    return (
        "I specialize in property-related queries. "
        "Please ask about properties, budgets, locations, or investments."
    )
