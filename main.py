import sys
import time

print("✅ main.py STARTED")
sys.stdout.flush()

for i in range(10):
    print(f"⏱️ Tick {i+1}")
    time.sleep(1)

print("✅ Finished script run.")
sys.stdout.flush()
