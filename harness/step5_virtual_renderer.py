"""
step5_virtual_renderer.py
Deterministic Virtual Clock Headless Frame Capture & FFmpeg Assembly:
- Directly pipes raw PNG frames from Playwright into FFmpeg image2pipe stdin
- Zero temporary disk frame dumps
- Guaranteed frame-accurate sync with zero audio drift
"""

import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

def render_scene_to_video(
    html_path: Path,
    audio_path: Path,
    output_mp4: Path,
    duration: float,
    fps: int = 30
) -> None:
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    total_frames = int(duration * fps)
    
    # FFmpeg command reading from stdin pipe
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-f", "image2pipe",
        "-vcodec", "png",
        "-i", "-",
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ]
    
    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(html_path.resolve().as_uri())
        page.wait_for_timeout(500)
        
        print(f"  [Rendering] Capturing {total_frames} frames ({duration:.1f}s @ {fps}fps)...")
        for f in range(total_frames):
            t = f / fps
            page.evaluate(f"window.seekToTime({t}); void 0;")
            screenshot_bytes = page.screenshot(type="png")
            ffmpeg_proc.stdin.write(screenshot_bytes)
            
            if f % 60 == 0:
                print(f"    Frame {f}/{total_frames} ({t:.1f}s)")
                
        browser.close()
        
    ffmpeg_proc.stdin.close()
    ffmpeg_proc.wait()
    print(f"  [Done] Video rendered to: {output_mp4} ({output_mp4.stat().st_size / (1024*1024):.2f} MB)")

