from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat import chat_router
from core.config import GOOGLE_API_KEY, CORS_ORIGINS


# -------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------

app = FastAPI(
    title="Property Intelligence Engine",
    description="Backend service for verified and unverified property intelligence",
    version="1.0.0"
)


# -------------------------------------------------
# CORS Middleware (VERY IMPORTANT)
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# -------------------------------------------------
# Routes
# -------------------------------------------------

app.include_router(chat_router)


# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get("/")
def health_check():
    return {
        "status": "Backend is running successfully"
    }


# -------------------------------------------------
# Gemini Key Load Status (Internal)
# -------------------------------------------------

@app.get("/internal/ai-status")
def ai_status():
    return {
        "gemini_key_loaded": bool(GOOGLE_API_KEY)
    }
