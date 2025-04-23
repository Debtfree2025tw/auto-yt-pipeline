# main.py
# Version: 1.1.2 — Debug-enhanced for Railway execution trace

print("✅ main.py has started running...")

import sys
import subprocess
import os

# System diagnostics
print("✅ Python version:", sys.version)
print("✅ Python path:", sys.executable)
print("✅ Installed packages:")
subprocess.run(["pip", "list"])

# Working directory check
print("📁 Current working directory contents:")
print(os.listdir("."))

from youtube_trending_scraper import get_trending_video_ids, run_full_pipeline

def health_check():
    print("✅ Pipeline initialized. Railway OK.")

if __name__ == "__main__":
    health_check()

    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    if not YOUTUBE_API_KEY:
        print("❌ Missing YOUTUBE_API_KEY. Check Railway environment variables.")
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

    try:
        print("🔍 Fetching trending videos for keywords...")
        video_ids = get_trending_video_ids(keywords, max_results=2)

        if video_ids:
            print(f"🎯 Found {len(video_ids)} videos. Starting full pipeline...")
            run_full_pipeline(video_ids)
        else:
            print("⚠️ No video IDs returned. Check your YOUTUBE_API_KEY or quota. Verify keywords.")
    except Exception as e:
        print(f"❌ Pipeline error: {e}")

print("✅ Script finished running.")
