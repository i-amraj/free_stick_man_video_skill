"""
render_codebg_5s.py
Renders demo_codebg_5s.html → demo_codebg_5s.mp4
Uses virtual clock (window.seekToTime) + Playwright + FFmpeg
"""
import asyncio, os, subprocess
from pathlib import Path
from playwright.async_api import async_playwright

PROJECT = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\comicron_60s_full")
HTML    = PROJECT / "demo_codebg_5s.html"
FRAMES  = PROJECT / "frames_codebg"
OUTPUT  = PROJECT / "demo_codebg_5s.mp4"
AUDIO   = PROJECT / "assets" / "master_audio_65s.mp3"
FPS     = 30
DURATION = 5.0
W, H    = 1080, 1920

FRAMES.mkdir(exist_ok=True)

async def render_frames():
    total = int(DURATION * FPS)
    print(f"Rendering {total} frames at {FPS} fps …")
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            args=["--no-sandbox","--disable-gpu",
                  "--font-render-hinting=none","--disable-web-security"]
        )
        page = await browser.new_page(viewport={"width": W, "height": H})

        # Load page (needs internet for Google Fonts - falls back gracefully)
        await page.goto(f"file:///{HTML.as_posix()}", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(1500)

        for i in range(total):
            fname = FRAMES / f"frame_{i:05d}.png"
            if fname.exists() and fname.stat().st_size > 100000:
                if i % 30 == 0:
                    print(f"  frame {i}/{total} already exists, skipping")
                continue
            t = round(i / FPS, 4)
            await page.evaluate(f"window.seekToTime({t})")
            await page.wait_for_timeout(16)   # ~1 frame paint
            await page.screenshot(path=str(fname), clip={"x":0,"y":0,"width":W,"height":H})
            if i % 15 == 0 or i == total - 1:
                print(f"  frame {i}/{total}  t={t:.2f}s")

        await browser.close()
    print("All frames captured.")

def assemble_video():
    print("Assembling video with FFmpeg …")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES / "frame_%05d.png"),
        # Audio: trim first 5s of master audio
        "-i", str(AUDIO),
        "-t", str(DURATION),
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(OUTPUT)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("FFmpeg STDERR:", result.stderr[-2000:])
        # Try without audio if audio missing
        cmd2 = [
            "ffmpeg", "-y",
            "-framerate", str(FPS),
            "-i", str(FRAMES / "frame_%05d.png"),
            "-t", str(DURATION),
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-pix_fmt", "yuv420p",
            str(OUTPUT)
        ]
        result2 = subprocess.run(cmd2, capture_output=True, text=True)
        if result2.returncode == 0:
            print("Video assembled (no audio).")
        else:
            print("FFmpeg failed:", result2.stderr[-1000:])
    else:
        print(f"Video saved: {OUTPUT}")

if __name__ == "__main__":
    asyncio.run(render_frames())
    assemble_video()

