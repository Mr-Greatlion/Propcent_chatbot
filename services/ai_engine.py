import requests
from core.config import GOOGLE_API_KEY  # ✅ THIS WAS MISSING

# -------------------------------------------------
# Gemini Configuration
# -------------------------------------------------

GEMINI_MODEL = "models/gemini-2.5-flash"
GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"{GEMINI_MODEL}:generateContent"
)

# -------------------------------------------------
# AI Refinement Layer (USED BY CHAT)
# -------------------------------------------------

def ai_refine(text: str) -> str:
    """
    Uses Google Gemini to:
    - Fix spelling mistakes
    - Improve grammar
    - Make responses professional
    - Keep meaning EXACTLY the same
    """

    # 🔒 Safety checks
    if not text:
        return "Could you please clarify what you are looking for?"

    if len(text.strip()) < 40:
        # Too short → don't send to AI
        return text

    if not GOOGLE_API_KEY:
        return text  # fallback if key missing

    try:
        response = requests.post(
            f"{GEMINI_ENDPOINT}?key={GOOGLE_API_KEY}",
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    "Rewrite the following message in a professional, "
                                    "clear, and friendly tone without changing its meaning:\n\n"
                                    + text
                                )
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,
                    "topP": 0.9,
                    "maxOutputTokens": 300
                }
            },
            timeout=10
        )

        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]

        return text

    except Exception:
        return text
