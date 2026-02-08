from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat import chat_router
from core.config import CORS_ORIGINS, CORS_REGEX

import os


app = FastAPI(
    title="Property Intelligence Engine",
    description="Backend service for verified property intelligence",
    version="2.0.0"
)


# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=CORS_REGEX,
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
# HEALTH
# -------------------------------------------------

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "Backend running ✅"}


# -------------------------------------------------
# INTERNAL (Hidden)
# -------------------------------------------------

@app.get("/internal-ops/ai-status", tags=["Internal"])
def ai_status():
    return {
        "gemini_key_loaded": bool(os.getenv("GOOGLE_API_KEY"))
    }
