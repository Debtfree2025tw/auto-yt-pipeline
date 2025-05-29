# main.py
# Version: 1.1.2 — Forced stdout flushing for Railway
print("[✓] main.py started running")

import time
print("🚀 Script started. Holding for 60 seconds to view logs.")
time.sleep(60)

import sys
import os
import subprocess
import time

def log(msg):
    print(msg)
    sys.stdout.flush()

log("✅ Python version: " + sys.version)
log("✅ Python path: " + sys.executable)
log("✅ Installed packages:")
subprocess.run(["pip", "list"])
sys.stdout.flush()

from youtube_trending_scraper import get_trending_video_ids, run_full_pipeline

def health_check():
    log("✅ Pipeline initialized. Railway OK.")

if __name__ == "__main__":
    log("✅ main.py has started running...")
    health_check()

    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    if not YOUTUBE_API_KEY:
        log("❌ Missing YOUTUBE_API_KEY. Check Railway environment variables.")
        exit(1)

    keywords = [
        "AI agents",
        "n8n automation workflows",
        "ElevenLabs voice cloning",
        "AI voice assistants",
        "ai business ideas",
        "best business ideas for 2025",
        "deepseek"
    ]

    log("🔍 Fetching trending videos for keywords...")
    video_ids = get_trending_video_ids(keywords, max_results=2)

    if video_ids:
        log(f"🎯 Found {len(video_ids)} videos. Starting full pipeline...")
        run_full_pipeline(video_ids)
        log("✅ Done.")
    else:
        log("⚠️ No video IDs returned. Check your YOUTUBE_API_KEY or quota. Verify keywords.")
