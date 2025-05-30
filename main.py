# main.py
# Version: Stable — Full runtime logic + stdout flushing for Railway

import os
import sys
import time
import subprocess

def log(msg):
    print(msg)
    sys.stdout.flush()

log("[✓] main.py started")

# Optional diagnostics (can remove if not needed)
log("✅ Python version: " + sys.version)
log("✅ Python path: " + sys.executable)
log("✅ Installed packages:")
subprocess.run(["pip", "list"])
sys.stdout.flush()

# Try importing pipeline
try:
    from youtube_trending_scraper import get_trending_video_ids, run_full_pipeline
except Exception as e:
    log(f"❌ Failed to import scraper module: {e}")
    exit(1)

# Entry point
if __name__ == "__main__":
    log("✅ main.py is running full pipeline")

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
        log("✅ Pipeline completed.")
    else:
        log("⚠️ No video IDs returned. Check API key, quota, or keywords.")
