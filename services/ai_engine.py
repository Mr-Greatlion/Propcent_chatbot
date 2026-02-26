# =====================================================
# PROPCENT AI ENGINE — V4 (PRODUCTION READY)
# Gemini REST API (VPS Optimized)
# =====================================================

import requests
from core.config import GOOGLE_API_KEY


# -------------------------------------------------
# GEMINI CONFIG
# -------------------------------------------------

GEMINI_MODEL = "models/gemini-2.5-flash"

GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"{GEMINI_MODEL}:generateContent"
)

# Persistent TCP session (VERY IMPORTANT for VPS)
session = requests.Session()


# -------------------------------------------------
# INTERNAL GEMINI CALL (SAFE + RETRY)
# -------------------------------------------------

def _call_gemini(payload, timeout=15, retries=2):

    if not GOOGLE_API_KEY:
        print("Missing GOOGLE_API_KEY")
        return None

    url = f"{GEMINI_ENDPOINT}?key={GOOGLE_API_KEY}"

    for attempt in range(retries):

        try:
            response = session.post(
                url,
                json=payload,
                timeout=timeout
            )

            if response.status_code == 200:

                data = response.json()

                text = (
                    data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text")
                )

                # Hallucination / empty guard
                if text and len(text.strip()) > 5:
                    return text.strip()

            else:
                print("Gemini API Error:", response.text)

        except Exception as e:
            print("Gemini Exception:", str(e))

    return None


# -------------------------------------------------
# SYSTEM PROMPT (MAIN AI PERSONALITY)
# -------------------------------------------------

SYSTEM_PROMPT = """
You are Propcent AI — an expert Indian real estate advisor.

RULES:
- Be practical and realistic.
- Never say "As an AI".
- Give actionable advice.
- Keep answers under 120 words.
- Prefer bullet points when useful.
"""


# -------------------------------------------------
# PRIMARY AI CHAT
# -------------------------------------------------

def ask_gemini(user_prompt: str):

    payload = {
        "contents": [{
            "parts": [{
                "text": SYSTEM_PROMPT +
                        f"\n\nUser Question:\n{user_prompt}"
            }]
        }],
        "generationConfig": {
            "temperature": 0.35,
            "topP": 0.9,
            "maxOutputTokens": 300
        }
    }

    result = _call_gemini(payload, timeout=18)

    if result:
        return result

    # Safe fallback
    return (
        "I'm having trouble accessing AI insights right now. "
        "Please try again in a moment."
    )


# -------------------------------------------------
# PROPERTY EXPLANATION (LEVEL-4 FEATURE)
# -------------------------------------------------

PROPERTY_PROMPT = """
You are a professional real estate consultant.

Explain the following property options clearly.

RULES:
- Be concise
- Highlight value
- No fake amenities
- Encourage user naturally
"""


def explain_properties(user_query: str, property_text: str):

    payload = {
        "contents": [{
            "parts": [{
                "text": (
                    PROPERTY_PROMPT +
                    f"\n\nUser Need:\n{user_query}\n\n"
                    f"Available Properties:\n{property_text}"
                )
            }]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 250
        }
    }

    result = _call_gemini(payload, timeout=18)

    return result if result else property_text


# -------------------------------------------------
# RESPONSE POLISHER
# (Used for database listings only)
# -------------------------------------------------

REFINE_PROMPT = """
Rewrite this property listing professionally.

STRICT RULES:
- Do NOT add information
- Do NOT hallucinate amenities
- Keep concise
- Premium but factual tone
"""


def ai_refine(text: str):

    # Skip tiny content
    if not text or len(text.split()) < 20:
        return text

    payload = {
        "contents": [{
            "parts": [{
                "text": REFINE_PROMPT + "\n\n" + text
            }]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 200
        }
    }

    result = _call_gemini(payload, timeout=10)

    return result if result else text
