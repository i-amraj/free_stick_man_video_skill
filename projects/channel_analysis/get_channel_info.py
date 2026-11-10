import os
import json
import yt_dlp

out_dir = os.path.abspath("projects/channel_analysis")
video_dir = os.path.join(out_dir, "videos")
os.makedirs(video_dir, exist_ok=True)

url = "https://youtube.com/shorts/8eeoDztahuM"

ydl_opts = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': False
}

print(f"[*] Fetching metadata for {url}...")
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    
channel_url = info.get('channel_url') or f"https://www.youtube.com/channel/{info.get('channel_id')}"
channel_name = info.get('channel') or info.get('uploader')
title = info.get('title')

print(f"Title: {title}")
print(f"Channel: {channel_name}")
print(f"Channel URL: {channel_url}")
print(f"Duration: {info.get('duration')}s")

# Save primary video metadata
with open(os.path.join(out_dir, "video1_meta.json"), "w", encoding="utf-8") as f:
    json.dump({
        'id': info.get('id'),
        'title': title,
        'channel': channel_name,
        'channel_url': channel_url,
        'duration': info.get('duration'),
        'description': info.get('description'),
        'tags': info.get('tags'),
        'fps': info.get('fps'),
        'width': info.get('width'),
        'height': info.get('height')
    }, f, indent=2, ensure_ascii=False)

print("[*] Now fetching recent shorts from the channel...")
# Fetch recent shorts from channel shorts tab or channel
channel_shorts_url = f"{channel_url}/shorts"
ydl_channel_opts = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,
    'playlist_items': '1-5'
}

with yt_dlp.YoutubeDL(ydl_channel_opts) as ydl:
    try:
        ch_info = ydl.extract_info(channel_shorts_url, download=False)
    except Exception as e:
        print(f"Could not load shorts tab directly: {e}, falling back to channel URL")
        ch_info = ydl.extract_info(channel_url, download=False)

entries = ch_info.get('entries') or []
print(f"Found {len(entries)} entries from channel.")

target_videos = []
# Ensure primary video is in target
target_videos.append({
    'id': info.get('id'),
    'url': f"https://www.youtube.com/shorts/{info.get('id')}",
    'title': title
})

for e in entries:
    vid_id = e.get('id')
    if vid_id and vid_id != info.get('id'):
        target_videos.append({
            'id': vid_id,
            'url': f"https://www.youtube.com/shorts/{vid_id}",
            'title': e.get('title')
        })
    if len(target_videos) >= 3:
        break

print("[*] Target videos for deep analysis:")
for i, tv in enumerate(target_videos, 1):
    print(f"  {i}. [{tv['id']}] {tv['title']} ({tv['url']})")

with open(os.path.join(out_dir, "target_videos.json"), "w", encoding="utf-8") as f:
    json.dump(target_videos, f, indent=2, ensure_ascii=False)

