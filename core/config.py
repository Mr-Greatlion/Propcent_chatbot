from dotenv import load_dotenv
import os

load_dotenv()

# -------------------------------------------------
# GOOGLE API KEY
# -------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY missing")


# -------------------------------------------------
# CORS SETTINGS
# -------------------------------------------------

CORS_ORIGINS = [
    "https://propcent.in",
    "https://www.propcent.in",
    "https://chat.propcent.in",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://admin.propcent.in"
]

# allow all propcent subdomains
CORS_REGEX = r"https://.*\.propcent\.in"
