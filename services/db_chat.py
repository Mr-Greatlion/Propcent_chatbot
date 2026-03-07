# =====================================================
# PROPCENT DATABASE CHAT SERVICE
# Handles PostgreSQL Chat Storage
# =====================================================

import psycopg2


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

def get_connection():

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

def create_chat_session(ip_address):

    conn = get_connection()

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

        print("CREATE SESSION ERROR:", e)

        conn.close()
        return None


# -------------------------------------------------
# SAVE CHAT MESSAGE
# -------------------------------------------------

def save_chat_message(session_id, role, content):

    conn = get_connection()

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

        print("SAVE MESSAGE ERROR:", e)

        conn.close()