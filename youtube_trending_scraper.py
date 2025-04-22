# youtube_trending_scraper.py
# Version: 1.4.1
# Updated: 2025-04-22 — limits each video to top 3 Whisper segments; 2 videos per keyword

import os
from googleapiclient.discovery import build
from whisper_gpt_analyzer import download_audio, analyze_video
from clip_editor import cut_clips_from_segments

# ✅ Set your YouTube API key here or via environment variable
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise EnvironmentError("Missing YOUTUBE_API_KEY environment variable. Set it before running.")

def get_trending_video_ids(keywords, max_results=2):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    video_ids = []
    for keyword in keywords:
        print(f"\n🔍 Searching: {keyword}")
        request = youtube.search().list(
            part="snippet",
            maxResults=max_results,
            q=keyword,
            type="video",
            order="relevance"
        )
        response = request.execute()

        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            print(f"🆔 {video_id} — {title}")
            video_ids.append(video_id)

    return video_ids

def run_full_pipeline(video_ids):
    for vid in video_ids:
        try:
            print(f"\n🚀 Processing: {vid}")
            video_path = download_audio(vid)
            segments = analyze_video(vid)  # Whisper returns top 3 segments now
            if segments and isinstance(segments, (list, str)):
                cut_clips_from_segments(video_path, segments)
            else:
                print(f"⚠️ No segments returned for {vid}")
        except Exception as e:
            print(f"❌ Failed on video {vid}: {e}")

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
