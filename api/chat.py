# =====================================================
# PROPCENT CHAT API — V4 (PRODUCTION READY)
# FastAPI Chat Endpoint
# =====================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from core.response import generate_response


# -------------------------------------------------
# ROUTER CONFIG
# -------------------------------------------------

chat_router = APIRouter(
    prefix="/chat",
    tags=["Property Chat"]
)


# -------------------------------------------------
# REQUEST MODEL
# -------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User chat message"
    )


# -------------------------------------------------
# RESPONSE MODEL
# -------------------------------------------------

class ChatResponse(BaseModel):
    reply: str


# -------------------------------------------------
# CHAT ENDPOINT
# -------------------------------------------------

@chat_router.post("/", response_model=ChatResponse)
def chat(payload: ChatRequest):

    try:
        user_message = payload.message.strip()

        # Safety guard
        if not user_message:
            return {
                "reply": "Please enter a valid message."
            }

        # Generate AI response
        reply = generate_response(user_message)

        # Final safety fallback
        if not reply:
            reply = (
                "I'm unable to respond right now. "
                "Please try again shortly."
            )

        return {"reply": reply}

    except Exception as e:
        # Never expose internal errors to users
        print("CHAT API ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
