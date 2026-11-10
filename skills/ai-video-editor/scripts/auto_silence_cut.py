"""
Automated Silence Detection and Video Jumpcutter.
Detects silence via ffmpeg silencedetect filter and splices non-silent segments together.
"""

import argparse
import subprocess
import re
import os
import sys

def get_silence_intervals(input_file, noise_db="-30dB", duration=0.5):
    cmd = [
        "ffmpeg", "-i", input_file,
        "-af", f"silencedetect=noise={noise_db}:d={duration}",
        "-f", "null", "-"
    ]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    stderr = proc.stderr

    silence_starts = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", stderr)]
    silence_ends = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", stderr)]
    
    return list(zip(silence_starts, silence_ends))

def get_video_duration(input_file):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_file
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
    return float(proc.stdout.strip())

def build_filter_complex(keep_intervals):
    filter_parts = []
    concat_inputs = []
    for idx, (start, end) in enumerate(keep_intervals):
        filter_parts.append(
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{idx}];"
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{idx}]"
        )
        concat_inputs.append(f"[v{idx}][a{idx}]")
    
    n = len(keep_intervals)
    concat_str = "".join(concat_inputs) + f"concat=n={n}:v=1:a=1[outv][outa]"
    return ";".join(filter_parts) + ";" + concat_str

def main():
    parser = argparse.ArgumentParser(description="Cut silence from video.")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("output", help="Output video file")
    parser.add_argument("--threshold", default="-30dB", help="Silence threshold in dB (e.g. -30dB)")
    parser.add_argument("--min-silence", type=float, default=0.5, help="Minimum silence duration in seconds")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: input file {args.input} not found.")
        sys.exit(1)

    print(f"Analyzing {args.input} for silence...")
    total_dur = get_video_duration(args.input)
    silence_intervals = get_silence_intervals(args.input, args.threshold, args.min_silence)

    if not silence_intervals:
        print("No silence detected. Copying file as is.")
        subprocess.run(["ffmpeg", "-i", args.input, "-c", "copy", args.output, "-y"], check=True)
        return

    # Invert silence to keep non-silent parts
    keep = []
    prev_end = 0.0
    for s_start, s_end in silence_intervals:
        if s_start > prev_end + 0.1:
            keep.append((prev_end, s_start))
        prev_end = s_end
    if prev_end < total_dur - 0.1:
        keep.append((prev_end, total_dur))

    print(f"Keeping {len(keep)} active speech segments. Trimming with FFmpeg...")
    fc = build_filter_complex(keep)
    cmd = [
        "ffmpeg", "-i", args.input,
        "-filter_complex", fc,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        args.output, "-y"
    ]
    subprocess.run(cmd, check=True)
    print(f"Done! Saved cut video to {args.output}")

if __name__ == "__main__":
    main()
