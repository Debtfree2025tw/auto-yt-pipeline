# main.py
# Version: 1.0.2 — Optimized for Render Free Tier (512MB RAM)

from youtube_trending_scraper import get_trending_video_ids, run_full_pipeline

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

    # ⚠️ RAM-Safe Mode: Limit to 1 video across all keywords
    video_ids = get_trending_video_ids(keywords, max_results=1)

    # Just run the first video to avoid memory overflow
    if video_ids:
        first_video = video_ids[0] if isinstance(video_ids, list) else video_ids
        run_full_pipeline([first_video])
    else:
        print("No video IDs returned. Skipping pipeline.")

