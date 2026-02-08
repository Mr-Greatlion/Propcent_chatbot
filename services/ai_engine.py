import requests
from core.config import GOOGLE_API_KEY


GEMINI_MODEL = "models/gemini-2.5-flash"

GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"{GEMINI_MODEL}:generateContent"
)

# ✅ Reuse TCP connection (FASTER)
session = requests.Session()


# -------------------------------------------------
# SAFE GEMINI CALL
# -------------------------------------------------

def _call_gemini(payload, timeout=15):

    try:

        res = session.post(
            f"{GEMINI_ENDPOINT}?key={GOOGLE_API_KEY}",
            json=payload,
            timeout=timeout
        )

        if res.status_code != 200:
            print("Gemini Error:", res.text)
            return None

        data = res.json()

        # ✅ SAFE PARSE
        return (
            data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text")
        )

    except Exception as e:
        print("Gemini Exception:", str(e))
        return None


# -------------------------------------------------
# AI THINKING
# -------------------------------------------------

def ask_gemini(prompt: str):

    if not GOOGLE_API_KEY:
        return "AI service unavailable."

    payload = {
        "contents": [{
            "parts": [{
                "text": (
                    "You are a senior real estate advisor in India.\n"
                    "Be practical. Avoid generic advice.\n"
                    "Keep answers under 120 words.\n\n"
                    f"User Question:\n{prompt}"
                )
            }]
        }],
        "generationConfig": {
            "temperature": 0.35,
            "maxOutputTokens": 300
        }
    }

    result = _call_gemini(payload)

    if result:
        return result

    return "AI service temporarily unavailable."


# -------------------------------------------------
# RESPONSE POLISH (ONLY FOR DATABASE TEXT)
# -------------------------------------------------

def ai_refine(text: str):

    # ✅ Use WORD COUNT, not char count
    if not text or len(text.split()) < 20:
        return text

    if not GOOGLE_API_KEY:
        return text

    payload = {
        "contents": [{
            "parts": [{
                "text": (
                    "Rewrite this property listing professionally.\n"
                    "DO NOT add new information.\n"
                    "Keep it concise.\n\n"
                    + text
                )
            }]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 200
        }
    }

    result = _call_gemini(payload, timeout=10)

    return result if result else text
