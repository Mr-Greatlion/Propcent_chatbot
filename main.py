from fastapi import FastAPI
from api.chat import chat_router
from core.config import GOOGLE_API_KEY

# -------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------

app = FastAPI(
    title="Property Intelligence Engine",
    description="Backend service for verified and unverified property intelligence",
    version="1.0.0"
)

# -------------------------------------------------
# Routes
# -------------------------------------------------

# Chat API (used by frontend)
app.include_router(chat_router)

# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get("/")
def health_check():
    """
    Basic health check to confirm backend is running
    """
    return {
        "status": "Backend is running successfully"
    }

# -------------------------------------------------
# Gemini Key Load Status (Internal)
# -------------------------------------------------

@app.get("/internal/ai-status")
def ai_status():
    """
    Confirms whether the Gemini API key is loaded.
    DOES NOT make an external API call.
    """
    return {
        "gemini_key_loaded": bool(GOOGLE_API_KEY)
    }
