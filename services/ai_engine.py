import requests
from core.config import GOOGLE_API_KEY


GEMINI_MODEL = "models/gemini-2.5-flash"

GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"{GEMINI_MODEL}:generateContent"
)


# -------------------------------------------------
# REAL AI THINKING
# -------------------------------------------------

def ask_gemini(prompt: str) -> str:

    if not GOOGLE_API_KEY:
        return "AI service is temporarily unavailable."

    try:

        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={GOOGLE_API_KEY}",
            json={
                "contents": [{
                    "parts": [{
                        "text": (
                            "You are a senior real estate advisor in India.\n"
                            "Give practical, location-aware advice.\n"
                            "Avoid generic responses.\n\n"
                            f"User Question:\n{prompt}"
                        )
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 500
                }
            },
            timeout=15
        )

        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]

        return "I couldn't process that request."

    except Exception:
        return "AI service is currently unavailable."


# -------------------------------------------------
# RESPONSE POLISHER
# -------------------------------------------------

def ai_refine(text: str) -> str:

    if not text or len(text.strip()) < 30:
        return text

    if not GOOGLE_API_KEY:
        return text

    try:

        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={GOOGLE_API_KEY}",
            json={
                "contents": [{
                    "parts": [{
                        "text": (
                            "Rewrite professionally without changing meaning:\n\n"
                            + text
                        )
                    }]
                }]
            },
            timeout=10
        )

        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]

        return text

    except Exception:
        return text
