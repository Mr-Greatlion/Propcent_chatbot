import json
import uuid
import requests
import time
from pathlib import Path

API_URL = "https://api.propcent.in/v1/chat"

BASE_DIR = Path(__file__).resolve().parent
CHAT_FILE = BASE_DIR / "data" / "chat_logs.json"


def load_logs():

    if not CHAT_FILE.exists():
        return []

    try:
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_logs(logs):

    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)


def send_chat(log):

    payload = {
        "sessionId": f"anon-{uuid.uuid4()}",
        "ipAddress": log.get("ip_address", "0.0.0.0"),
        "title": "Property Chat Session",
        "messages": [
            {
                "role": "USER",
                "content": log.get("user_message", "")
            },
            {
                "role": "ASSISTANT",
                "content": log.get("bot_reply", "")
            }
        ]
    }

    try:

        r = requests.post(API_URL, json=payload, timeout=20)

        if r.status_code in [200, 201]:

            print("Chat shared:", r.status_code)
            return True

        print("Failed:", r.status_code)
        return False

    except Exception as e:

        print("Error:", e)
        return False


def monitor():

    print("Realtime instant chat sync started...")

    while True:

        logs = load_logs()

        updated = False

        for log in logs:

            if log.get("shared") == True:
                continue

            success = send_chat(log)

            if success:

                log["shared"] = True
                updated = True

        if updated:
            save_logs(logs)

        time.sleep(2)


if __name__ == "__main__":
    monitor()