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
# CORS Middleware (CRITICAL FOR FRONTEND)
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,   # ✅ Loaded from config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Routes
# -------------------------------------------------

app.include_router(chat_router)


# -------------------------------------------------
# Health Check (Used by Load Balancers / DevOps)
# -------------------------------------------------

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "Backend is running successfully"
    }


# -------------------------------------------------
# Internal AI Status (DO NOT EXPOSE PUBLICLY LATER)
# -------------------------------------------------

@app.get("/internal/ai-status", tags=["Internal"])
def ai_status():
    return {
        "gemini_key_loaded": bool(GOOGLE_API_KEY)
    }
