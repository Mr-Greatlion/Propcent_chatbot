# =====================================================
# PROPCENT CHAT LOGGER — V1
# Stores chat logs with IP address
# =====================================================

import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "data" / "chat_logs.json"


def save_chat(ip_address: str, user_message: str, bot_reply: str):

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": ip_address,
        "user_message": user_message,
        "bot_reply": bot_reply
    }

    try:
        # If file exists, load existing logs
        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(log_entry)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)

    except Exception as e:
        print("CHAT LOG ERROR:", e)