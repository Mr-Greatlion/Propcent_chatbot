from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat import chat_router
from core.config import CORS_ORIGINS, GOOGLE_API_KEY


app = FastAPI(
    title="Propcent Property Intelligence Engine",
    version="2.0",
    description="Production Real Estate AI Backend"
)

# -------------------------------------------------
# CORS
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
# Routes
# -------------------------------------------------

app.include_router(chat_router)

# -------------------------------------------------
# Health
# -------------------------------------------------

@app.get("/")
def health():
    return {"status": "Propcent AI running"}

@app.get("/internal/ai-status")
def ai_status():
    return {"gemini_loaded": bool(GOOGLE_API_KEY)}
