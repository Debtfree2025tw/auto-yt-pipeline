# main.py
# Version: 1.1.0 — Optimized for Railway (8GB RAM)

import sys
sys.stdout.reconfigure(line_buffering=True)

from youtube_trending_scraper import get_trending_video_ids, run_full_pipeline

def health_check():
    print("✅ Pipeline initialized. Railway OK.")

if __name__ == "__main__":
    health_check()

    keywords = [
        "AI agents",
        "n8n automation workflows",
        "ElevenLabs voice cloning",
        "AI voice assistants",
        "ai business ideas",
        "best business ideas for 2025",
        "deepseek"
    ]

    # Now safe to run up to 2 per keyword
    video_ids = get_trending_video_ids(keywords, max_results=2)

    if video_ids:
        run_full_pipeline(video_ids)
   else:
    print("⚠️ No video IDs returned. Check your YOUTUBE_API_KEY or quota.")


