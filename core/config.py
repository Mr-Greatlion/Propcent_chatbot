import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------
# API Keys
# -------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# -------------------------------------------------
# CORS
# -------------------------------------------------

CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://chat.propcent.in",
    "https://propcent.in",
]

# ⭐ FUTURE-PROOF (optional but recommended)
CORS_REGEX = r"https://.*\.propcent\.in"
