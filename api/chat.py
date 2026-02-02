from fastapi import APIRouter
from pydantic import BaseModel
from core.response import generate_response

chat_router = APIRouter(prefix="/chat", tags=["Property Chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@chat_router.post("/", response_model=ChatResponse)
def chat(payload: ChatRequest):
    reply = generate_response(payload.message)
    return {"reply": reply}
