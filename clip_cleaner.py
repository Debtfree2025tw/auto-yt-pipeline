# clip_cleaner.py — Cleans old clips if storage exceeds threshold or schedule

import os
import shutil
from pathlib import Path
import time

CLIP_DIR = Path("/content/drive/MyDrive/YT_Automation/clips")
FALLBACK_DIR = Path("/tmp/fallback_clips")
MAX_STORAGE_MB = 20000  # Example: 20 GB max clip size before cleanup

def get_total_clip_size_mb():
    return sum(f.stat().st_size for f in CLIP_DIR.glob("*.mp4")) / 1_000_000

def clean_old_clips(threshold_mb=MAX_STORAGE_MB):
    total_mb = get_total_clip_size_mb()
    if total_mb < threshold_mb:
        print(f"🧼 Clip storage under limit ({int(total_mb)}MB < {threshold_mb}MB). No cleanup needed.")
        return

    CLIP_DIR.mkdir(parents=True, exist_ok=True)
    FALLBACK_DIR.mkdir(parents=True, exist_ok=True)

    clips = sorted(CLIP_DIR.glob("*.mp4"), key=os.path.getctime)
    to_delete = clips[:len(clips)//4]  # remove oldest 25%
    for clip in to_delete:
        print(f"🗑️ Moving old clip to fallback: {clip.name}")
        shutil.move(str(clip), FALLBACK_DIR / clip.name)
    print("✅ Cleanup complete.")
