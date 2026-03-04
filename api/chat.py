# =====================================================
# PROPCENT CHAT API — V4.5 (PRODUCTION READY)
# FastAPI Chat Endpoint + Chat Logging
# =====================================================

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from core.response import generate_response
from services.chat_logger import save_chat


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
def chat(payload: ChatRequest, request: Request):

    try:
        user_message = payload.message.strip()

        # Safety guard
        if not user_message:
            return {
                "reply": "Please enter a valid message."
            }

        # ---------------------------------------------
        # GENERATE RESPONSE
        # ---------------------------------------------

        reply = generate_response(user_message)

        if not reply:
            reply = (
                "I'm unable to respond right now. "
                "Please try again shortly."
            )

        # ---------------------------------------------
        # CAPTURE USER IP
        # ---------------------------------------------

        ip_address = request.client.host

        # ---------------------------------------------
        # STORE CHAT LOG
        # ---------------------------------------------

        try:
            save_chat(ip_address, user_message, reply)
        except Exception as log_error:
            print("CHAT LOG ERROR:", log_error)

        # ---------------------------------------------
        # RETURN RESPONSE
        # ---------------------------------------------

        return {"reply": reply}

    except Exception as e:

        # Never expose internal errors to users
        print("CHAT API ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
