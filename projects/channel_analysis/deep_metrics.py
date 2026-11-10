import numpy as np
from PIL import Image
from collections import Counter
import json
import subprocess

def get_dominant_colors(img_path, k=5):
    im = Image.open(img_path).convert('RGB')
    im = im.resize((150, 150))
    pixels = np.array(im).reshape(-1, 3)
    quant = (pixels // 24) * 24
    counts = Counter(map(tuple, quant))
    top = counts.most_common(k)
    return [f'#{r:02x}{g:02x}{b:02x}' for (r,g,b), _ in top]

print("=== COLOR ANALYSIS ===")
for vid in ['8eeoDztahuM', 'V5qnOWYIL7Y', 'N_R7ZHTDNVo']:
    c1 = get_dominant_colors(f'projects/channel_analysis/frames/{vid}/frame_03.0s.jpg')
    c2 = get_dominant_colors(f'projects/channel_analysis/frames/{vid}/frame_15.0s.jpg')
    print(f"{vid} Colors: frame 3s -> {c1}")
    print(f"{vid} Colors: frame 15s -> {c2}")

print("\n=== SCRIPT & CADENCE METRICS ===")
for vid in ['8eeoDztahuM', 'V5qnOWYIL7Y', 'N_R7ZHTDNVo']:
    with open(f'projects/channel_analysis/transcripts/transcript_{vid}.json', encoding='utf-8') as f:
        t = json.load(f)
    words = len(t['text'].split())
    dur = t['segments'][-1]['end']
    wpm = round((words / dur) * 60)
    segs = len(t['segments'])
    avg_seg = dur / segs
    print(f"{vid}: Duration={dur}s | Words={words} | Cadence={wpm} WPM | Segments={segs} | Avg Cut Beat={avg_seg:.2f}s")

# Let's inspect audio loudness with ffmpeg ebur128
print("\n=== AUDIO LOUDNESS (LUFS) ===")
for vid in ['8eeoDztahuM', 'V5qnOWYIL7Y', 'N_R7ZHTDNVo']:
    cmd = ['ffmpeg', '-i', f'projects/channel_analysis/videos/video_{vid}.mp3', '-filter_complex', 'ebur128', '-f', 'null', '-']
    res = subprocess.run(cmd, capture_output=True, text=True)
    for line in res.stderr.splitlines():
        if 'Integrated loudness:' in line or 'LRA:' in line:
            print(f"{vid} -> {line.strip()}")

