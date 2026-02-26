# =====================================================
# PROPCENT AI — MAIN APPLICATION (V4 FINAL)
# FastAPI Production Entry Point
# =====================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat import chat_router
from core.config import CORS_ORIGINS, GOOGLE_API_KEY


# -------------------------------------------------
# APP INITIALIZATION
# -------------------------------------------------

app = FastAPI(
    title="Propcent Property Intelligence Engine",
    version="4.0",
    description="Production Real Estate AI Backend"
)


# -------------------------------------------------
# STARTUP CHECKS (VERY IMPORTANT)
# -------------------------------------------------

@app.on_event("startup")
def startup_checks():

    print("\n🚀 Starting Propcent AI...")

    if GOOGLE_API_KEY:
        print("✅ Google Gemini API key loaded")
    else:
        print("⚠️ WARNING: GOOGLE_API_KEY missing")

    print("✅ API Ready\n")


# -------------------------------------------------
# CORS CONFIGURATION
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS"
    ],
    allow_headers=["*"],
)


# -------------------------------------------------
# ROUTES
# -------------------------------------------------

app.include_router(chat_router)


# -------------------------------------------------
# HEALTH CHECK (PUBLIC)
# -------------------------------------------------

@app.get("/", tags=["Health"])
def health():
    return {
        "status": "Propcent AI running",
        "version": "4.0"
    }


# -------------------------------------------------
# INTERNAL AI STATUS
# -------------------------------------------------

@app.get("/internal/ai-status", tags=["Internal"])
def ai_status():
    return {
        "gemini_loaded": bool(GOOGLE_API_KEY),
        "service": "Propcent AI"
    }
