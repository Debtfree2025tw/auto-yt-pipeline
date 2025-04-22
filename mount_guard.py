# mount_guard.py — ensures Drive is mounted + fallback restore + pre-check validation

import os
import time
from google.colab import drive
from pathlib import Path
import shutil

MOUNT_PATH = "/content/drive"
YT_AUTOMATION_PATH = f"{MOUNT_PATH}/MyDrive/YT_Automation"
FALLBACK_DIR = Path("/tmp/fallback_clips")
CLIP_DIR = Path(f"{YT_AUTOMATION_PATH}/clips")


def ensure_drive_mounted():
    if not Path(YT_AUTOMATION_PATH).exists():
        print("🔁 Drive mount dropped. Re-mounting...")
        drive.mount(MOUNT_PATH, force_remount=True)
        Path(YT_AUTOMATION_PATH).mkdir(parents=True, exist_ok=True)
        print("✅ Drive re-mounted.")


def verify_drive():
    try:
        test_path = Path(YT_AUTOMATION_PATH)
        test_path.mkdir(parents=True, exist_ok=True)
        _ = os.listdir(test_path)
        return True
    except OSError:
        print("🚫 Drive verification failed — remounting...")
        ensure_drive_mounted()
        return False


def safe_cd():
    if verify_drive():
        try:
            os.chdir(YT_AUTOMATION_PATH)
            print(f"📂 Changed to: {YT_AUTOMATION_PATH}")
        except Exception as e:
            print(f"❌ Failed to cd into automation folder: {e}")
    else:
        print("⚠️ Drive path still not available. Skipping cd.")


def restore_fallback_clips():
    if FALLBACK_DIR.exists() and CLIP_DIR.exists():
        files = list(FALLBACK_DIR.glob("*.mp4"))
        if files:
            print(f"📦 Restoring {len(files)} fallback clips to Drive...")
            for file in files:
                shutil.move(str(file), CLIP_DIR / file.name)
            print("✅ Fallback recovery complete.")


# Optional background watchdog (disabled in prod)
def start_mount_watchdog(poll_interval=15):
    import threading

    def watchdog():
        while True:
            if not verify_drive():
                print("🚨 Watchdog triggered remount.")
            time.sleep(poll_interval)

    thread = threading.Thread(target=watchdog, daemon=True)
    thread.start()
