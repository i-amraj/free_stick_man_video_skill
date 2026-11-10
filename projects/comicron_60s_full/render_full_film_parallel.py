"""
render_full_film_parallel.py
Multi-worker parallel chunk renderer for Comicron 60s Full Film (100% Procedural BG).
Uses 4 parallel Playwright browser workers + FFmpeg assembly with audio mux.
"""
import asyncio
import os
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

PROJECT = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\comicron_60s_full")
HTML    = PROJECT / "scene.html"
FRAMES  = PROJECT / "frames_full"
OUTPUT  = PROJECT / "comicron_60s_procedural_master.mp4"
AUDIO   = PROJECT / "assets" / "master_audio_65s.mp3"

FPS      = 30
DURATION = 65.5
TOTAL_FRAMES = int(DURATION * FPS) # 1965 frames
NUM_WORKERS  = 4
W, H     = 1080, 1920

FRAMES.mkdir(exist_ok=True)

async def worker(worker_id: int, start_frame: int, end_frame: int):
    url = f"file:///{HTML.as_posix()}"
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            args=["--no-sandbox", "--disable-gpu", "--disable-web-security"]
        )
        page = await browser.new_page(viewport={"width": W, "height": H})
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1000)

        for i in range(start_frame, end_frame):
            fname = FRAMES / f"frame_{i:05d}.png"
            t = round(i / FPS, 4)
            await page.evaluate(f"window.seekToTime({t})")
            await page.wait_for_timeout(8)
            await page.screenshot(path=str(fname), clip={"x": 0, "y": 0, "width": W, "height": H})
            if (i - start_frame) % 50 == 0 or i == end_frame - 1:
                print(f"[Worker {worker_id}] Frame {i}/{end_frame} (t={t:.2f}s)")

        await browser.close()
    print(f"[Worker {worker_id}] Completed frames {start_frame} to {end_frame}!")

async def main():
    chunk_size = (TOTAL_FRAMES + NUM_WORKERS - 1) // NUM_WORKERS
    tasks = []
    for w in range(NUM_WORKERS):
        s = w * chunk_size
        e = min(s + chunk_size, TOTAL_FRAMES)
        if s < e:
            tasks.append(worker(w, s, e))

    print(f"Starting {len(tasks)} workers for {TOTAL_FRAMES} frames ({DURATION}s @ {FPS}fps)...")
    await asyncio.gather(*tasks)
    print("All frames successfully captured!")

    # Assemble video with FFmpeg
    print("Assembling master MP4 with FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES / "frame_%05d.png"),
        "-i", str(AUDIO),
        "-t", str(DURATION),
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(OUTPUT)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS: Master video exported to {OUTPUT}")
    else:
        print("FFmpeg error:", res.stderr[-1000:])

if __name__ == "__main__":
    asyncio.run(main())

