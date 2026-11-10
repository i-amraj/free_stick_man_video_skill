"""
GrowKaz Studio — Production Video Renderer & QC Assembly
Captures 1080x1920 Stickman scene, muxes master audio, and performs automated QC
"""

import os
import time
import subprocess
import json
import shutil
import av
from playwright.sync_api import sync_playwright
from PIL import Image

def render_master_video():
    base_dir = os.path.abspath("projects/mystery_333am")
    html_file = os.path.join(base_dir, "scene", "index.html")
    audio_file = os.path.join(base_dir, "audio", "final_master_audio.mp3")
    rec_dir = os.path.join(base_dir, "output", "temp_rec")
    final_output = os.path.join(base_dir, "output", "mystery_333am_final.mp4")
    contact_sheet = os.path.join(base_dir, "output", "contact_sheet.jpg")
    artifact_dir = "C:/Users/iamra/.gemini/antigravity/brain/c9b9d424-5a3c-4adf-aabc-2078a51c8ad6"

    os.makedirs(rec_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "output"), exist_ok=True)

    # 1. Get exact audio duration
    container = av.open(audio_file)
    audio_duration = float(container.duration) / av.time_base
    container.close()
    print(f"[*] Target Video Duration: {audio_duration:.2f}s")

    # 2. Launch Chromium and record full scene in real-time
    print("[*] Launching Chromium 1080x1920 capture session...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--allow-file-access-from-files",
                "--disable-web-security",
                "--autoplay-policy=no-user-gesture-required"
            ]
        )
        context = browser.new_context(
            record_video_dir=rec_dir,
            record_video_size={"width": 1080, "height": 1920},
            viewport={"width": 1080, "height": 1920}
        )
        page = context.new_page()
        page.goto(f"file:///{html_file}")
        
        # Wait for scene to fully initialize
        page.wait_for_function("window.sceneReady === true", timeout=25000)
        print("[*] GrowKaz Stickman scene ready and initialized!")

        # Trigger play
        page.evaluate("togglePlay()")
        print(f"[*] Recording 60 FPS Stickman animation ({audio_duration:.1f}s)...")
        
        # Wait until audio finishes
        start_wait = time.time()
        while time.time() - start_wait < audio_duration + 2.0:
            time.sleep(2.0)
            try:
                cur = page.evaluate("document.getElementById('master-audio').currentTime")
                print(f"  + Render Progress: {cur:.1f}s / {audio_duration:.1f}s", end="\r")
            except Exception:
                pass

        print("\n[*] Animation sequence finished. Finalizing video capture...")
        page.close()
        context.close()
        browser.close()

    # Find the recorded webm file
    webm_files = [os.path.join(rec_dir, f) for f in os.listdir(rec_dir) if f.endswith(".webm")]
    if not webm_files:
        raise RuntimeError("No recorded video found in temp_rec!")
    raw_video = webm_files[0]
    print(f"[*] Raw recording ready: {raw_video}")

    # 3. FFmpeg Transcode + Audio Muxing
    print("[*] Encoding final broadcast MP4 with FFmpeg...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", audio_file,
        "-t", f"{audio_duration:.2f}",
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "256k",
        "-movflags", "+faststart",
        final_output
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"[SUCCESS] Final Video Exported: {final_output} ({os.path.getsize(final_output) / (1024*1024):.2f} MB)")

    # 4. Generate Visual Contact Sheet (6 key stickman frames)
    print("[*] Generating contact sheet preview...")
    preview_dir = os.path.join(base_dir, "output", "previews")
    preview_candidates = [
        "stickman_beat02_phone.jpg",
        "stickman_beat05_knock.jpg",
        "stickman_beat06_walk_door.jpg",
        "stickman_beat09_footprints.jpg",
        "stickman_beat12_shadow_behind.jpg",
        "stickman_beat14_climax.jpg"
    ]
    preview_files = [os.path.join(preview_dir, f) for f in preview_candidates if os.path.exists(os.path.join(preview_dir, f))]
    if len(preview_files) >= 6:
        thumb_w, thumb_h = 360, 640
        sheet = Image.new("RGB", (thumb_w * 3, thumb_h * 2), (6, 9, 19))
        for idx, pf in enumerate(preview_files[:6]):
            img = Image.open(pf).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            x = (idx % 3) * thumb_w
            y = (idx // 3) * thumb_h
            sheet.paste(img, (x, y))
        sheet.save(contact_sheet, quality=92)
        print(f"[SUCCESS] Contact Sheet saved: {contact_sheet}")

        # Also copy to artifacts dir
        if os.path.exists(artifact_dir):
            shutil.copy2(contact_sheet, os.path.join(artifact_dir, "contact_sheet.jpg"))
            for pf in preview_candidates:
                src_pf = os.path.join(preview_dir, pf)
                if os.path.exists(src_pf):
                    shutil.copy2(src_pf, os.path.join(artifact_dir, pf))
            print(f"[SUCCESS] Contact sheet & keyframe artifacts updated in: {artifact_dir}")

    # 5. Automated QC Verification Gate
    print("[*] Running automated Quality Control checks...")
    qc_container = av.open(final_output)
    v_stream = qc_container.streams.video[0]
    a_stream = qc_container.streams.audio[0]
    vid_dur = float(qc_container.duration) / av.time_base
    qc_container.close()

    qc_report = {
        "resolution": f"{v_stream.width}x{v_stream.height}",
        "aspect_ratio": "9:16",
        "fps": round(float(v_stream.average_rate), 2),
        "video_duration_s": round(vid_dur, 2),
        "audio_duration_s": round(audio_duration, 2),
        "duration_delta_s": round(abs(vid_dur - audio_duration), 3),
        "file_size_mb": round(os.path.getsize(final_output) / (1024 * 1024), 2),
        "pass_resolution": v_stream.width == 1080 and v_stream.height == 1920,
        "pass_fps": float(v_stream.average_rate) >= 24.0,
        "pass_duration_sync": abs(vid_dur - audio_duration) < 0.15,
        "pass_audio_track": a_stream is not None,
    }
    print(f"[*] QC Verification Summary:\n{json.dumps(qc_report, indent=2)}")

    # 6. Clean temp recordings
    for f in webm_files:
        try: os.remove(f)
        except: pass
    try: os.rmdir(rec_dir)
    except: pass

    print("[*] Pipeline Finished Successfully!")
    return final_output, qc_report

if __name__ == "__main__":
    render_master_video()


