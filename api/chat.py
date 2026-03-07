# =====================================================
# PROPCENT CHAT API — FINAL STABLE VERSION
# PostgreSQL + Local JSON Chat Logging
# =====================================================

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
import psycopg2

from core.response import generate_response
from services.chat_logger import save_chat


# -------------------------------------------------
# DATABASE CONFIG
# -------------------------------------------------

DB_HOST = "localhost"
DB_NAME = "propcent_backend"
DB_USER = "propcent_db_user"
DB_PASS = "qmDTdDvImAGsfRg"
DB_PORT = "5432"


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print("DATABASE CONNECTION ERROR:", e)
        return None


# -------------------------------------------------
# CREATE CHAT SESSION
# -------------------------------------------------

def create_chat_session(ip_address: str):

    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO "ChatSession" ("ipAddress")
            VALUES (%s)
            RETURNING id
            """,
            (ip_address,)
        )

        session_id = cursor.fetchone()[0]

        conn.commit()

        cursor.close()
        conn.close()

        return session_id

    except Exception as e:
        print("SESSION CREATE ERROR:", e)
        conn.close()
        return None


# -------------------------------------------------
# SAVE CHAT MESSAGE
# -------------------------------------------------

def save_chat_message(session_id: int, role: str, content: str):

    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO "ChatMessage"
            ("chatSessionId", "role", "content")
            VALUES (%s, %s, %s)
            """,
            (session_id, role, content)
        )

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        print("CHAT MESSAGE SAVE ERROR:", e)
        conn.close()


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

    sessionId: Optional[int] = None


# -------------------------------------------------
# RESPONSE MODEL
# -------------------------------------------------

class ChatResponse(BaseModel):

    reply: str
    sessionId: int


# -------------------------------------------------
# CHAT ENDPOINT
# -------------------------------------------------

@chat_router.post("/", response_model=ChatResponse)
def chat(payload: ChatRequest, request: Request):

    try:

        user_message = payload.message.strip()

        if not user_message:
            return {
                "reply": "Please enter a valid message.",
                "sessionId": payload.sessionId or 0
            }

        # -----------------------------------------
        # GET USER IP
        # -----------------------------------------

        ip_address = request.client.host

        # -----------------------------------------
        # CREATE OR USE SESSION
        # -----------------------------------------

        session_id = payload.sessionId

        if not session_id:
            session_id = create_chat_session(ip_address)

        if not session_id:
            print("Failed to create chat session")
            session_id = 0

        # -----------------------------------------
        # SAVE USER MESSAGE TO DATABASE
        # -----------------------------------------

        try:
            if session_id:
                save_chat_message(session_id, "USER", user_message)
        except Exception as e:
            print("USER MESSAGE ERROR:", e)

        # -----------------------------------------
        # GENERATE AI RESPONSE
        # -----------------------------------------

        reply = generate_response(user_message)

        if not reply:
            reply = "I'm unable to respond right now. Please try again shortly."

        # -----------------------------------------
        # SAVE AI MESSAGE TO DATABASE
        # -----------------------------------------

        try:
            if session_id:
                save_chat_message(session_id, "ASSISTANT", reply)
        except Exception as e:
            print("ASSISTANT MESSAGE ERROR:", e)

        # -----------------------------------------
        # SAVE LOCAL JSON BACKUP
        # -----------------------------------------

        try:
            save_chat(ip_address, user_message, reply)
        except Exception as e:
            print("LOCAL LOG ERROR:", e)

        # -----------------------------------------
        # RETURN RESPONSE
        # -----------------------------------------

        return {
            "reply": reply,
            "sessionId": session_id
        }

    except Exception as e:

        print("CHAT API ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
