"""
Video Sound Master Mixer — video-sound
Automated multi-stem audio assembly with ducking and -14 LUFS loudness mastering
"""

import os
import sys
import subprocess
import argparse
import json

def mix_audio(voice_file, music_file, output_file, sfx_manifest=None):
    print(f"[*] Starting Video Sound Engine")
    print(f"    Voice: {voice_file}")
    print(f"    Music: {music_file}")
    print(f"    Output: {output_file}")

    if not os.path.exists(voice_file):
        print(f"[!] Error: Voice file not found: {voice_file}")
        return False

    # Execute FFmpeg sidechain ducking + loudnorm
    cmd = [
        "ffmpeg", "-y",
        "-i", voice_file,
        "-i", music_file,
        "-filter_complex",
        "[1:a]volume=0.35[bg];"
        "[bg][0:a]sidechaincompress=threshold=0.12:ratio=4:attack=20:release=350[ducked];"
        "[0:a][ducked]amix=inputs=2:duration=first[mix];"
        "[mix]loudnorm=I=-14:LRA=7:tp=-1.5[out]",
        "-map", "[out]",
        "-c:a", "aac",
        "-b:a", "256k",
        output_file
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[PASS] Master audio mixed and normalized to -14 LUFS -> {output_file}")
        return True
    except Exception as e:
        print(f"[WARN] Direct FFmpeg execution note: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--voice", required=True, help="Voiceover audio file")
    parser.add_argument("--music", required=True, help="Background music audio file")
    parser.add_argument("--output", default="master_audio.mp3", help="Output file")
    parser.add_argument("--sfx-manifest", default=None, help="JSON file with SFX cue timings")
    args = parser.parse_args()

    mix_audio(args.voice, args.music, args.output, args.sfx_manifest)

