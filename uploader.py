# main.py
# Entry point for Render to run YouTube Shorts automation

import os
from dotenv import load_dotenv
from youtube_trending_scraper import get_trending_video_ids, run_full_pipeline
from uploader import upload_all_clips
from telegram_notifier import send_telegram_update
from mount_guard import verify_drive, safe_cd
from datetime import datetime
import logging

# ✅ Optional: Verify and navigate to working directory if using Google Drive
verify_drive()
safe_cd("/content/drive/MyDrive/YT_Automation")

# ✅ Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("7319296439")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ✅ Start logging
log_path = f"logs/batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(message)s')

if __name__ == "__main__":
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
        video_ids = get_trending_video_ids(keywords)
        print("\n🎯 Final Batch Video IDs:")
        for vid in video_ids:
            print(vid)
        run_full_pipeline(video_ids)

        print("\n📤 Uploading to YouTube...")
        upload_all_clips()

        print("\n📨 Notifying Telegram...")
        send_telegram_update(f"✅ Batch upload complete. Processed {len(video_ids)} videos.")

    except Exception as e:
        error_message = f"❌ Error during batch run: {str(e)}"
        print(error_message)
        logging.error(error_message)
        send_telegram_update(error_message)
