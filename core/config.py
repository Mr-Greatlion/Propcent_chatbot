import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------
# API Keys
# -------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# -------------------------------------------------
# CORS Configuration
# -------------------------------------------------
# Add ALL allowed frontend origins here

CORS_ORIGINS = [
    "http://localhost:3000",   # React default
    "http://127.0.0.1:3000",
    # Add production domain later:
    "https://chat.propcent.in"
    "https://propcent.in"
    
]



