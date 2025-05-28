import requests
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def send_discord(msg):
    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK is not set.")
        return

    payload = {"content": msg}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("✅ Discord alert sent.")
        else:
            print(f"⚠️ Discord error: {response.status_code} {response.text}")
    except Exception as e:
        print(f"❌ Discord alert failed: {e}")
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def send_discord(message):
    if not DISCORD_WEBHOOK:
        print("❌ DISCORD_WEBHOOK not set in environment.")
        return

    try:
        payload = {"content": message}
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        if response.status_code == 204:
            print("✅ Discord alert sent.")
        else:
            print(f"❌ Discord error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception while sending Discord alert: {e}")
