# whisper_gpt_analyzer.py
# Version: 1.2.1 — Robust error handling and traceable logging

import os
import subprocess
import json
import whisper

try:
    model = whisper.load_model("base")
    print("[WHISPER] Model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load Whisper model: {e}")
    model = None

def download_audio(video_id):
    temp_path = f"/tmp/audio_{video_id}.%(ext)s"
    ytdlp_cmd = [
        "yt-dlp",
        f"https://www.youtube.com/watch?v={video_id}",
        "-f", "bestvideo+bestaudio",
        "--merge-output-format", "mp4",
        "-o", temp_path,
        "--print", "after_move:filepath"
    ]

    try:
        result = subprocess.run(ytdlp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
        stdout = result.stdout.decode().strip()
        stderr = result.stderr.decode().strip()
        print("[YT-DLP STDOUT]", stdout)
        print("[YT-DLP STDERR]", stderr)

        if stdout and os.path.exists(stdout):
            print(f"[ANALYZER] Confirmed audio file path: {stdout}")
            return stdout
    except Exception as e:
        print(f"❌ yt-dlp failed: {e}")

    print("[ANALYZER] Attempting fallback in /tmp...")
    for f in os.listdir("/tmp"):
        if f.startswith(f"audio_{video_id}") and f.endswith((".mp4", ".webm", ".mkv", ".m4a")):
            fallback_path = os.path.join("/tmp", f)
            print(f"[ANALYZER] Fallback audio file match: {fallback_path}")
            return fallback_path

    raise FileNotFoundError("Audio file not found after yt-dlp run.")

def analyze_video(video_id):
    print(f"[ANALYZER] Processing video: {video_id}")

    if not model:
        print("❌ Whisper model not available.")
        return []

    try:
        audio_path = download_audio(video_id)
        if not audio_path or not os.path.exists(audio_path):
            print("❌ Audio path is invalid or missing.")
            return []

        result = model.transcribe(audio_path, word_timestamps=False)
        segments = result.get("segments", [])
        print(f"[WHISPER] Segment count: {len(segments)}")
    except Exception as e:
        print(f"[ANALYZER] Whisper error: {e}")
        return []

    parsed_segments = []
    for seg in segments:
        parsed_segments.append({
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"].strip()
        })

    if not parsed_segments:
        print("⚠️ No segments found by Whisper.")
        return []

    top_segments = sorted(parsed_segments, key=lambda x: len(x["text"]), reverse=True)[:3]
    print(f"[WHISPER] Top segment previews: {[s['text'][:40] for s in top_segments]}")
    return top_segments
