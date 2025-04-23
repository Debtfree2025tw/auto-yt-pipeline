# telegram_notifier.py
# Version: 1.0.0 — Sends a message to your Telegram channel/chat via bot

import os
import requests

def send_telegram_update(message: str):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("⚠️ Telegram bot token or chat ID not set in environment.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        res = requests.post(url, data=payload)
        if res.ok:
            print("📨 Telegram notification sent.")
        else:
            print(f"❌ Telegram error: {res.status_code} — {res.text}")
    except Exception as e:
        print(f"❌ Telegram exception: {e}")
