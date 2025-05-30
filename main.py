from youtube_trending_scraper import get_trending_video_ids, run_full_pipeline

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
