# whisper_gpt_analyzer.py
# Version: 1.2.0
# Updated: 2025-04-22 — limits to top 3 Whisper segments per video

import os
import subprocess
import json
import whisper

model = whisper.load_model("base")

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
    result = subprocess.run(ytdlp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode().strip()
    stderr = result.stderr.decode().strip()
    print("[YT-DLP STDOUT]", stdout)
    print("[YT-DLP STDERR]", stderr)

    if stdout and os.path.exists(stdout):
        print(f"[ANALYZER] Confirmed audio file path: {stdout}")
        return stdout

    for f in os.listdir("/tmp"):
        if f.startswith(f"audio_{video_id}"):
            fallback_path = os.path.join("/tmp", f)
            print(f"[ANALYZER] Fallback audio file match: {fallback_path}")
            return fallback_path

    raise FileNotFoundError("Audio file not found after yt-dlp run.")

def analyze_video(video_id):
    print(f"[ANALYZER] Processing video: {video_id}")
    audio_path = download_audio(video_id)

    try:
        result = model.transcribe(audio_path, word_timestamps=False)
        segments = result.get("segments", [])
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
    return top_segments
