# =====================================================
# PROPCENT CHAT API — FINAL PRODUCTION VERSION
# PostgreSQL + Local JSON Chat Logging
# =====================================================

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
import psycopg2
import uuid

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


# -------------------------------------------------
# GET DATABASE CONNECTION
# -------------------------------------------------

def get_db_connection():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
    except Exception as e:
        print("❌ DATABASE CONNECTION ERROR:", e)
        return None


# -------------------------------------------------
# CREATE CHAT SESSION
# -------------------------------------------------

def create_chat_session(ip_address):

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        if not conn:
            return None

        cursor = conn.cursor()

        session_uuid = str(uuid.uuid4())

        cursor.execute(
            """
            INSERT INTO "ChatSession"
            ("ipAddress","sessionId","createdAt","updatedAt")
            VALUES (%s,%s,NOW(),NOW())
            RETURNING id
            """,
            (ip_address, session_uuid)
        )

        session_id = cursor.fetchone()[0]

        conn.commit()

        return session_id

    except Exception as e:

        print("❌ SESSION CREATE ERROR:", e)
        return None

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# -------------------------------------------------
# SAVE CHAT MESSAGE
# -------------------------------------------------

def save_chat_message(session_id, role, content):

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO "ChatMessage"
            ("chatSessionId","role","content","createdAt","updatedAt")
            VALUES (%s,%s,%s,NOW(),NOW())
            """,
            (session_id, role, content)
        )

        conn.commit()

    except Exception as e:

        print("❌ CHAT MESSAGE SAVE ERROR:", e)

    finally:

        if cursor:
            cursor.close()

        if conn:
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
        max_length=1000
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

        # GET USER IP
        ip_address = request.client.host

        # CREATE OR USE SESSION
        session_id = payload.sessionId

        if not session_id:
            session_id = create_chat_session(ip_address)

        if not session_id:
            print("⚠️ SESSION CREATION FAILED")
            session_id = 0

        # SAVE USER MESSAGE
        if session_id:
            save_chat_message(session_id, "USER", user_message)

        # GENERATE AI RESPONSE
        reply = generate_response(user_message)

        if not reply:
            reply = "I'm unable to respond right now. Please try again shortly."

        # SAVE ASSISTANT MESSAGE
        if session_id:
            save_chat_message(session_id, "ASSISTANT", reply)

        # SAVE LOCAL JSON BACKUP
        try:
            save_chat(ip_address, user_message, reply)
        except Exception as e:
            print("⚠️ LOCAL JSON LOG ERROR:", e)

        return {
            "reply": reply,
            "sessionId": session_id
        }

    except Exception as e:

        print("❌ CHAT API ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
