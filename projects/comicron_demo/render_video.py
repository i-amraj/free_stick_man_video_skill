import os
import time
import subprocess
from playwright.sync_api import sync_playwright

FPS = 30
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)

FRAMES_DIR = "projects/comicron_demo/frames_v3"
os.makedirs(FRAMES_DIR, exist_ok=True)

OUT_MP4 = "projects/comicron_demo/comicron_10s_demo_v3.mp4"
AUDIO_PATH = "projects/comicron_demo/master_audio.mp3"
HTML_PATH = "file:///" + os.path.abspath("projects/comicron_demo/scene_v5.html").replace("\\", "/")

print(f"--- Starting Render Pipeline ---")
print(f"Total Frames: {TOTAL_FRAMES} ({DURATION}s @ {FPS} FPS)")
print(f"HTML Scene: {HTML_PATH}")

t0 = time.time()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    page.goto(HTML_PATH)
    
    viewport = page.locator("#viewport")
    
    for i in range(TOTAL_FRAMES):
        t = i / FPS
        page.evaluate(f"window.seekToTime({t})")
        frame_file = f"{FRAMES_DIR}/frame_{i:04d}.png"
        viewport.screenshot(path=frame_file)
        
        if (i + 1) % 50 == 0 or i == TOTAL_FRAMES - 1:
            elapsed = time.time() - t0
            fps_speed = (i + 1) / elapsed
            print(f"Rendered [{i+1}/{TOTAL_FRAMES}] frames ({((i+1)/TOTAL_FRAMES)*100:.1f}%) - Speed: {fps_speed:.1f} fps")
            
    browser.close()

render_time = time.time() - t0
print(f"\nAll {TOTAL_FRAMES} frames captured in {render_time:.1f}s!")

# Assemble with FFmpeg
print("\nAssembling final MP4 with FFmpeg...")
cmd = [
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", f"{FRAMES_DIR}/frame_%04d.png",
    "-i", AUDIO_PATH,
    "-c:v", "libx264",
    "-profile:v", "high",
    "-level", "4.2",
    "-pix_fmt", "yuv420p",
    "-crf", "18",
    "-preset", "fast",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUT_MP4
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    size_mb = os.path.getsize(OUT_MP4) / (1024 * 1024)
    print(f"SUCCESS! Exported video: {OUT_MP4} ({size_mb:.2f} MB)")
else:
    print("FFmpeg error:", res.stderr[:500])

