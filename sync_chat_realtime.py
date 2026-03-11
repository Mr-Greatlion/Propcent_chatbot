import json
import uuid
import requests
import time
from pathlib import Path

# ======================================
# CONFIG
# ======================================

API_URL = "https://api.propcent.in/v1/chat"

BASE_DIR = Path(__file__).resolve().parent
CHAT_FILE = BASE_DIR / "data" / "chat_logs.json"

BATCH_SIZE = 10


# ======================================
# LOAD CHAT LOGS
# ======================================

def load_logs():

    if not CHAT_FILE.exists():
        return []

    try:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# ======================================
# SAVE REMAINING LOGS
# ======================================

def save_logs(logs):

    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


# ======================================
# CONVERT FORMAT
# ======================================

def convert_batch(batch):

    session_id = f"anon-{uuid.uuid4()}"

    messages = []

    ip_address = "0.0.0.0"

    for log in batch:

        ip_address = log.get("ip_address", "0.0.0.0")

        messages.append({
            "role": "USER",
            "content": log.get("user_message", "")
        })

        messages.append({
            "role": "ASSISTANT",
            "content": log.get("bot_reply", "")
        })

    payload = {
        "sessionId": session_id,
        "ipAddress": ip_address,
        "title": "Property Chat Session",
        "messages": messages
    }

    return payload


# ======================================
# SEND BATCH
# ======================================

def send_batch(payload):

    try:

        r = requests.post(
            API_URL,
            json=payload,
            timeout=20
        )

        print("Sent batch:", r.status_code)

        return r.status_code == 200

    except Exception as e:

        print("Send error:", e)
        return False


# ======================================
# REALTIME LOOP
# ======================================

def monitor():

    print("Realtime chat sync started...")

    while True:

        logs = load_logs()

        if len(logs) >= BATCH_SIZE:

            batch = logs[:BATCH_SIZE]

            payload = convert_batch(batch)

            success = send_batch(payload)

            if success:

                remaining = logs[BATCH_SIZE:]

                save_logs(remaining)

                print("Batch sent. Remaining logs:", len(remaining))

        time.sleep(5)


# ======================================
# START
# ======================================

if __name__ == "__main__":
    monitor()