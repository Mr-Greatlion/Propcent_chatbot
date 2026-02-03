import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("❌ Google API key not found")
    exit()

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GOOGLE_API_KEY}"

response = requests.get(url, timeout=15)

print("Status Code:", response.status_code)
print("Response:")
print(response.text)
