# clip_editor.py
# Version: 1.1.2
# Updated: 2025-04-22 — restored missing import

import os
import json
import re
from moviepy.editor import VideoFileClip
from pathlib import Path

def parse_segments(json_string):
    if isinstance(json_string, str):
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON input for segments.") from e
    elif isinstance(json_string, list):
        data = json_string
    else:
        raise TypeError("Expected JSON string or list of segments.")

    segments = []
    for item in data:
        if "start" in item and "end" in item and "text" in item:
            quote = item["text"]
            quote = re.sub(r'[\n\r]', ' ', quote)
            quote = re.sub(r'[“”"\'`]', '', quote)
            quote = re.sub(r'[\(\)\[\]\{\}]', '', quote)
            quote = re.sub(r'[^\w\s\-]', '', quote)
            quote = quote.strip()
            segments.append({
                "start": float(item["start"]),
                "end": float(item["end"]),
                "quote": quote
            })
    return segments

# Synced safe_filename with global usage pattern
def safe_filename(text):
    text = re.sub(r"[^\w\s-]", "", text)  # remove special chars
    text = re.sub(r"\s+", "_", text)       # replace spaces with _
    return text[:50]                          # trim length

def cut_clips_from_segments(video_path, segments_json, max_duration=59.0):
    print("🧪 Parsing segments...")
    segments = parse_segments(segments_json)
    if not segments:
        raise ValueError("No valid segments parsed.")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    clips_dir = Path("clips")
    clips_dir.mkdir(parents=True, exist_ok=True)

    clip = VideoFileClip(video_path)
    print(f"🎬 Loaded video: {video_path} ({clip.duration:.2f} sec)")

    for i, seg in enumerate(segments):
        start = seg["start"]
        end = min(seg["end"], start + max_duration)
        quote = seg.get("quote", "")
        base_name = safe_filename(f"clip_{i+1}_{quote[:30]}")
        filename = base_name + ".mp4"
        output_path = clips_dir / filename
        try:
            clip.subclip(start, end).write_videofile(
                str(output_path), codec='libx264', audio_codec='aac', verbose=False, logger=None
            )
            print(f"✅ Saved clip: {output_path}")
        except Exception as e:
            print(f"❌ Failed to cut clip {filename}: {e}")

    clip.close()
