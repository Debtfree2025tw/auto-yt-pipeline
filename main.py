# main.py
# Version: 1.1.1 — Enhanced logging for Railway + API visibility
print("✅ main.py has started running...")

import sys
print("✅ Python version:", sys.version)
print("✅ Python path:", sys.executable)
print("✅ Installed packages:")
import subprocess
subprocess.run(["pip", "list"])


from youtube_trending_scraper import get_trending_video_ids, run_full_pipeline
import os

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

    print("🔍 Fetching trending videos for keywords...")
    video_ids = get_trending_video_ids(keywords, max_results=2)

    if video_ids:
        print(f"🎯 Found {len(video_ids)} videos. Starting full pipeline...")
        run_full_pipeline(video_ids)
    else:
        print("⚠️ No video IDs returned. Check your YOUTUBE_API_KEY or quota. Verify keywords.")

print("✅ Script finished running.")



