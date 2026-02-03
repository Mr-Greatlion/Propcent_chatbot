import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

print("🧪 Gemini API KEY TESTER")
print("------------------------")

question = input("Enter a question to test Gemini:\n> ")

if not GOOGLE_API_KEY:
    print("❌ Google API key not found")
    exit()

response = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    f"?key={GOOGLE_API_KEY}",
    json={
        "contents": [
            {
                "parts": [{"text": question}]
            }
        ]
    },
    timeout=15
)

if response.status_code == 200:
    answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    print("\n✅ Gemini Response:\n")
    print(answer)
else:
    print("\n❌ Gemini Error:\n")
    print(response.text)
