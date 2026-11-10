import os
import json
import yt_dlp

out_dir = os.path.abspath("projects/channel_analysis")
video_dir = os.path.join(out_dir, "videos")
os.makedirs(video_dir, exist_ok=True)

with open(os.path.join(out_dir, "target_videos.json"), "r", encoding="utf-8") as f:
    target_videos = json.load(f)

for idx, tv in enumerate(target_videos, 1):
    vid_id = tv['id']
    target_path = os.path.join(video_dir, f"video_{idx}_{vid_id}.mp4")
    if os.path.exists(target_path):
        print(f"[+] Already downloaded: {target_path}")
        continue
    
    print(f"[*] Downloading Video {idx}: {tv['title']} ({vid_id})...")
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(video_dir, f"video_{idx}_{vid_id}.%(ext)s"),
        'merge_output_format': 'mp4',
        'quiet': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([tv['url']])
    print(f"[SUCCESS] Video {idx} downloaded!")

print("[*] All downloads complete!")

