"""
build_audio_with_dialogue.py
Generates the 20-second audio track with narration and character dialogue:
- Voiceover & Character speech via gTTS
- Audio positioning & padding to exact 20.0 seconds
- BGM bed ducked underneath
- Word-level alignment via Whisper
"""

import os
import subprocess
import json
from pathlib import Path
from gtts import gTTS
import whisper

PROJ = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\video_20s_dialogue")
ASSETS = PROJ / "assets"
ASSETS.mkdir(exist_ok=True)

# 1. Generate Voice Clips
lines = [
    # (id, speaker, text, target_start_time)
    ("part1_narr", "narrator", "At midnight, Detective Gary tracked the missing gold to the old warehouse.", 0.2),
    ("part2_gary", "gary", "Aha! Nobody can hide treasure from Detective Gary!", 5.6),
    ("part3_gary", "gary", "Wait! It is just an old dirty shoe?!", 11.8),
    ("part4_narr", "narrator", "The thief had already exchanged the gold for firewood!", 15.6)
]

clip_paths = []
for cid, speaker, text, target_start in lines:
    cpath = ASSETS / f"{cid}.mp3"
    print(f"Generating {cid} ({speaker}): '{text}'")
    # For narrator use default en, for gary use co.uk or similar accent if possible
    tld = "co.uk" if speaker == "gary" else "com"
    tts = gTTS(text=text, lang="en", tld=tld, slow=False)
    tts.save(str(cpath))
    clip_paths.append((cid, speaker, text, target_start, cpath))

# 2. Assemble Master Voice Track on 20.0s timeline using FFmpeg
# We delay each clip to its target_start_time and mix them
filter_inputs = ""
filter_delays = ""
mix_inputs = ""

for i, (cid, speaker, text, target_start, cpath) in enumerate(clip_paths):
    delay_ms = int(target_start * 1000)
    filter_delays += f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}];"
    mix_inputs += f"[a{i}]"

mix_filter = f"{filter_delays}{mix_inputs}amix=inputs={len(clip_paths)}:dropout_transition=0:normalize=0[voiceout]"

cmd_voice = [
    "ffmpeg", "-y"
]
for _, _, _, _, cpath in clip_paths:
    cmd_voice.extend(["-i", str(cpath)])

cmd_voice.extend([
    "-filter_complex", mix_filter,
    "-map", "[voiceout]",
    "-t", "20.0",
    str(ASSETS / "voice_track_20s.mp3")
])

print("Mixing voice clips...")
res = subprocess.run(cmd_voice, capture_output=True, text=True)
if res.returncode != 0:
    print("FFmpeg voice mix error:", res.stderr)
else:
    print("Voice track assembled:", ASSETS / "voice_track_20s.mp3")

# 3. Add subtle BGM from existing assets
bgm_source = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\mystery_333am\audio\dance_beat.mp3")
if not bgm_source.exists():
    bgm_source = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\.agents\skills\changelog-video\assets\bgm.mp3")

final_audio = PROJ / "audio_master_20s.mp3"
if bgm_source.exists():
    cmd_master = [
        "ffmpeg", "-y",
        "-i", str(ASSETS / "voice_track_20s.mp3"),
        "-stream_loop", "-1", "-i", str(bgm_source),
        "-filter_complex",
        "[1:a]volume=0.18,afade=t=out:st=19.0:d=1.0[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=0[aout]",
        "-map", "[aout]",
        "-t", "20.0",
        str(final_audio)
    ]
else:
    cmd_master = [
        "ffmpeg", "-y",
        "-i", str(ASSETS / "voice_track_20s.mp3"),
        "-t", "20.0",
        str(final_audio)
    ]

subprocess.run(cmd_master, capture_output=True, text=True)
print("Master audio created:", final_audio)

# 4. Transcribe with Whisper for exact word timestamps
print("Transcribing with Whisper base model for word timestamps...")
model = whisper.load_model("base")
result = model.transcribe(str(final_audio), word_timestamps=True, language="en")

words_data = []
segments_data = []
for seg in result["segments"]:
    seg_entry = {
        "start": seg["start"],
        "end": seg["end"],
        "text": seg["text"].strip(),
        "words": []
    }
    for w in seg.get("words", []):
        word_clean = w["word"].strip()
        words_data.append({
            "word": word_clean,
            "start": round(w["start"], 2),
            "end": round(w["end"], 2)
        })
        seg_entry["words"].append({
            "word": word_clean,
            "start": round(w["start"], 2),
            "end": round(w["end"], 2)
        })
    segments_data.append(seg_entry)

# Save JSONs
with open(PROJ / "word_timings_20s.json", "w", encoding="utf-8") as f:
    json.dump(words_data, f, indent=2)

with open(PROJ / "subtitle_chunks_20s.json", "w", encoding="utf-8") as f:
    json.dump(segments_data, f, indent=2)

print(f"Transcription complete! {len(words_data)} words captured across {len(segments_data)} chunks.")

