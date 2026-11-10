"""
render_20s_video.py
Parallel 4-worker renderer for scene_20s.html
Duration: 20.0s (600 frames at 30 fps)
Outputs: video_20s_dialogue_master.mp4 with audio_master_20s.mp3
"""

import asyncio
import os
import subprocess
import time
from pathlib import Path
from playwright.async_api import async_playwright

PROJ = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\video_20s_dialogue")
HTML = PROJ / "scene_20s.html"
FRAMES_DIR = PROJ / "frames"
OUTPUT_MP4 = PROJ / "video_20s_dialogue_master.mp4"
AUDIO_FILE = PROJ / "audio_master_20s.mp3"

FPS = 30
DURATION = 20.0
TOTAL_FRAMES = int(DURATION * FPS) # 600 frames
W, H = 1080, 1920
NUM_WORKERS = 4

FRAMES_DIR.mkdir(exist_ok=True)

async def render_worker(worker_id: int, frame_indices: list):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--font-render-hinting=none",
                "--disable-web-security"
            ]
        )
        page = await browser.new_page(viewport={"width": W, "height": H})
        file_url = f"file:///{HTML.as_posix()}"
        await page.goto(file_url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(1000)

        for count, i in enumerate(frame_indices):
            fname = FRAMES_DIR / f"frame_{i:05d}.png"
            if fname.exists() and fname.stat().st_size > 100000:
                continue

            t = round(i / FPS, 4)
            await page.evaluate(f"window.seekToTime({t}); void 0;")
            await page.wait_for_timeout(16)
            await page.screenshot(path=str(fname), clip={"x": 0, "y": 0, "width": W, "height": H})

            if count % 25 == 0 or count == len(frame_indices) - 1:
                print(f"[Worker {worker_id}] Frame {i}/{TOTAL_FRAMES} (t={t:.2f}s)")

        await browser.close()

async def main():
    print(f"=== Starting 20s Dialogue Video Render: {TOTAL_FRAMES} frames across {NUM_WORKERS} workers ===")
    t0 = time.time()

    chunks = [[] for _ in range(NUM_WORKERS)]
    for i in range(TOTAL_FRAMES):
        chunks[i % NUM_WORKERS].append(i)

    tasks = [render_worker(w, chunks[w]) for w in range(NUM_WORKERS)]
    await asyncio.gather(*tasks)

    elapsed = time.time() - t0
    print(f"All {TOTAL_FRAMES} frames rendered in {elapsed:.1f}s!")

    # Assemble MP4 with FFmpeg
    print("Assembling master MP4 with FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%05d.png"),
        "-i", str(AUDIO_FILE),
        "-t", str(DURATION),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-af", "afade=t=out:st=19.2:d=0.8",
        "-shortest",
        str(OUTPUT_MP4)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        size_mb = OUTPUT_MP4.stat().st_size / (1024 * 1024)
        print(f"SUCCESS: Video exported to {OUTPUT_MP4} ({size_mb:.2f} MB)")
    else:
        print("FFmpeg error:", res.stderr[-1000:])

if __name__ == "__main__":
    asyncio.run(main())

