# main.py
# Version: 1.2.2 — Railway-ready, secure env-based key loading, no uploader

import sys
import os
import subprocess
from datetime import datetime
from youtube_trending_scraper import get_trending_video_ids, run_full_pipeline
from telegram_notifier import send_telegram_update

# Diagnostics
print("✅ main.py has started running...")
print("✅ Python version:", sys.version)
print("✅ Python path:", sys.executable)
print("📦 Installed packages:")
subprocess.run(["pip", "list"])

# Working dir check
print("📁 Current working directory contents:")
print(os.listdir("."))

# Load from Railway environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Check required keys
if not YOUTUBE_API_KEY:
    print("❌ Missing YOUTUBE_API_KEY")
    exit(1)
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("⚠️ Telegram notification setup incomplete (bot token or chat ID missing)")

# Confirm launch
print("✅ Pipeline initialized. Railway OK.")

keywords = [
    "AI agents",
    "n8n automation workflows",
    "ElevenLabs voice cloning",
    "AI voice assistants",
    "ai business ideas",
    "best business ideas for 2025",
    "deepseek"
]

try:
    print("🔍 Fetching trending video IDs...")
    video_ids = get_trending_video_ids(keywords, max_results=2)

    if video_ids:
        print(f"🎯 Found {len(video_ids)} videos. Starting pipeline...")
        run_full_pipeline(video_ids)

        print("\n📨 Sending Telegram notification...")
        send_telegram_update(f"✅ Batch complete. Processed {len(video_ids)} videos.")
    else:
        print("⚠️ No videos found.")
except Exception as e:
    error_message = f"❌ Error during batch run: {e}"
    print(error_message)
    try:
        send_telegram_update(error_message)
    except Exception as notify_error:
        print(f"❌ Telegram failed: {notify_error}")

print("✅ Script finished.")
