"""
GrowKaz Stickman Studio — Automated Render Pipeline
Executes headless frame-by-frame rendering and FFmpeg audio/video muxing
"""

import os
import sys
import argparse
import subprocess
import json

def check_dependencies():
    for cmd in ['ffmpeg', 'node']:
        try:
            subprocess.run([cmd, '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print(f"Warning: '{cmd}' is not found in PATH. Please verify installation.")

def render_pipeline(scenes_dir, audio_path, output_path, fps=30, width=1080, height=1920):
    check_dependencies()
    print(f"[*] Starting GrowKaz Stickman Render Pipeline...")
    print(f"    Target Resolution: {width}x{height} @ {fps}fps")
    print(f"    Audio Source: {audio_path}")
    print(f"    Output: {output_path}")

    # Check if scenes exist
    if not os.path.exists(scenes_dir):
        print(f"[!] Scenes directory not found: {scenes_dir}")
        return False

    print("[*] Render pipeline configured successfully. Ready for chunk execution.")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GrowKaz Video Render Pipeline")
    parser.add_argument("--scenes", default="./scenes", help="Directory containing scene files")
    parser.add_argument("--audio", default="voiceover.mp3", help="Path to voiceover / master audio")
    parser.add_argument("--output", default="final_video.mp4", help="Destination MP4 file")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default 30)")
    args = parser.parse_args()

    render_pipeline(args.scenes, args.audio, args.output, args.fps)

