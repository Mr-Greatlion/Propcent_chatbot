import requests
from core.config import GOOGLE_API_KEY


GEMINI_MODEL = "models/gemini-2.5-flash"

GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"{GEMINI_MODEL}:generateContent"
)

# ✅ Persistent TCP connection (VERY FAST)
session = requests.Session()


# -------------------------------------------------
# INTERNAL SAFE GEMINI CALL
# -------------------------------------------------

def _call_gemini(payload, timeout=15, retries=2):

    if not GOOGLE_API_KEY:
        return None

    url = f"{GEMINI_ENDPOINT}?key={GOOGLE_API_KEY}"

    for attempt in range(retries):

        try:
            res = session.post(url, json=payload, timeout=timeout)

            if res.status_code == 200:

                data = res.json()

                text = (
                    data.get("candidates", [{}])[0]
                        .get("content", {})
                        .get("parts", [{}])[0]
                        .get("text")
                )

                # ✅ Hallucination guard
                if text and len(text.strip()) > 5:
                    return text

            else:
                print("Gemini Error:", res.text)

        except Exception as e:
            print("Gemini Exception:", str(e))

    return None


# -------------------------------------------------
# AI THINKING (Primary Brain)
# -------------------------------------------------

SYSTEM_PROMPT = """
You are an expert real estate advisor in India.

RULES:
- Be practical and realistic.
- Avoid generic AI phrases.
- Do NOT say "As an AI".
- Keep answers under 120 words.
- Prefer bullet points when useful.
"""


def ask_gemini(user_prompt: str):

    payload = {
        "contents": [{
            "parts": [{
                "text": SYSTEM_PROMPT + f"\n\nUser Question:\n{user_prompt}"
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

    # ✅ Smart fallback (NEVER show scary errors)
    return "I'm having trouble accessing AI insights right now. Please try again in a moment."


# -------------------------------------------------
# RESPONSE POLISH
# ONLY FOR PROPERTY DATABASE TEXT
# -------------------------------------------------

REFINE_PROMPT = """
Rewrite this property listing professionally.

STRICT RULES:
- Do NOT add information.
- Do NOT hallucinate amenities.
- Keep it concise.
- Make it sound premium but factual.
"""


def ai_refine(text: str):

    # Skip tiny responses
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
