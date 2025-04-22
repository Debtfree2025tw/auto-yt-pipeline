from youtube_trending_scraper import *

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
    video_ids = get_trending_video_ids(keywords)
    print("\n🎯 Final Batch Video IDs:")
    for vid in video_ids:
        print(vid)

    run_full_pipeline(video_ids)
