import requests
import os
from dotenv import load_dotenv

# Load env vars from .env file
load_dotenv()

url = os.getenv("DISCORD_WEBHOOK")
message = {"content": "✅ Discord webhook is working!"}

response = requests.post(url, json=message)

if response.status_code == 204:
    print("✅ Webhook sent successfully.")
else:
    print(f"❌ Failed to send webhook: {response.status_code} - {response.text}")
