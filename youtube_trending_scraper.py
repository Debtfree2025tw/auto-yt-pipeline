# youtube_trending_scraper.py
# Version: 1.4.2
# Updated: 2025-04-23 — Hardened error trapping + logging visibility

import os
from googleapiclient.discovery import build
from whisper_gpt_analyzer import download_audio, analyze_video
from clip_editor import cut_clips_from_segments

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise EnvironmentError("Missing YOUTUBE_API_KEY environment variable. Set it before running.")

def get_trending_video_ids(keywords, max_results=2):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    video_ids = []

    for keyword in keywords:
        print(f"\n🔍 Searching: {keyword}")
        try:
            request = youtube.search().list(
                part="snippet",
                maxResults=max_results,
                q=keyword,
                type="video",
                order="relevance"
            )
            response = request.execute()
            items = response.get("items", [])
            if not items:
                print("⚠️ No results found for keyword:", keyword)

            for item in items:
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                print(f"🆔 {video_id} — {title}")
                video_ids.append(video_id)
        except Exception as e:
            print(f"❌ YouTube API error on keyword '{keyword}': {e}")

    return video_ids

def run_full_pipeline(video_ids):
    for vid in video_ids:
        try:
            print(f"\n🚀 Processing: {vid}")
            video_path = download_audio(vid)
            print(f"📥 Downloaded: {video_path}")

            segments = analyze_video(vid)
            print(f"🧠 Segments received: {segments}")

            if segments and isinstance(segments, list) and all(isinstance(s, dict) for s in segments):
                cut_clips_from_segments(video_path, segments)
            else:
                print(f"⚠️ Invalid or empty segments returned for {vid}")
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
