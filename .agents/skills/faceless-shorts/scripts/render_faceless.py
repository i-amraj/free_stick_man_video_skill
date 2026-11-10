"""
Nafay3D Faceless Short Video Compositor — faceless-shorts
Composes split-screen B-roll + character/evidence with neon divider and burned captions
"""

import os
import sys
import subprocess
import argparse

def render_faceless_short(top_asset, bottom_asset, audio_file, captions_file, output_file):
    print(f"[*] Starting Nafay3D Faceless Short Compositor")
    print(f"    Top Layer: {top_asset}")
    print(f"    Bottom Layer: {bottom_asset}")
    print(f"    Master Audio: {audio_file}")
    print(f"    Captions: {captions_file}")

    # Build split screen filter complex with cyan divider
    filter_complex = (
        "[0:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[top];"
        "[1:v]scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960[bottom];"
        "[top][bottom]vstack=inputs=2[stacked];"
        # Draw neon cyan divider line at Y=960
        "[stacked]drawbox=x=0:y=958:w=1080:h=4:color=#38bdf8@0.9:t=fill[divided]"
    )

    if captions_file and os.path.exists(captions_file):
        filter_complex += f";[divided]subtitles={captions_file}[outv]"
    else:
        filter_complex += ";[divided]copy[outv]"

    cmd = [
        "ffmpeg", "-y",
        "-i", top_asset,
        "-i", bottom_asset,
        "-i", audio_file,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "2:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[PASS] Rendered faceless short: {output_file}")
        return True
    except Exception as e:
        print(f"[WARN] Compositor FFmpeg run note: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", required=True)
    parser.add_argument("--bottom", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--captions", default=None)
    parser.add_argument("--output", default="final_faceless_short.mp4")
    args = parser.parse_args()

    render_faceless_short(args.top, args.bottom, args.audio, args.captions, args.output)

