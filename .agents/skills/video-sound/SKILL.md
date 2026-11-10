---
name: video-sound
description: >-
  Audio engineering, music beds, Foley/SFX choreography, and voiceover stem mixing.
  Use this skill whenever adding background music (BGM), synchronizing sound effects (whooshes, pops,
  impacts, mystery drones), applying automated sidechain ducking, aligning beat drops with scene cuts,
  or mastering audio to platform broadcast standards (-14 LUFS YouTube/TikTok).
---

# Video Sound & Audio Engineering (`video-sound`)

Sound drives over 60% of viewer retention. In GrowKaz and viral short-form storytelling, the audio track is built with three distinct layers:
1. **Narration / Voiceover (Foreground)**: Crystal clear, compressed, de-essed dialogue.
2. **SFX / Foley (Midground)**: High-impact cues locked to stickman gestures, UI reveals, and scene seams.
3. **Music Bed (Background)**: Sub-bass, rhythmic synth, or mystery drone auto-ducked under speech.

---

## 1. The SFX Choreography Taxonomy

| SFX Trigger | Sound Type | Purpose | Frequency / Rule |
|-------------|------------|---------|------------------|
| Scene Cut / Seam | Fast airy whoosh / swoosh | Masks the cut, propels momentum | Every scene transition |
| Stickman Gesture | Soft pop / cartoon snap | Emphasizes pointing, nodding, shrug | On primary keyframe |
| Plot Twist / Climax | Sub-bass drop / cinematic impact | Freezes viewer attention | 1–2 per short video |
| Data / Stat Reveal | Digital typewriter / cash register | Grounds metrics & facts | Synced to number counter |
| Mystery / Question | Tension riser / reverse cymbal | Builds suspense before answer | Before key reveal |

---

## 2. Automated Sidechain Ducking with FFmpeg

Never keep background music at a constant volume. When the voice speaks, the music must dynamically drop by **-6dB to -8dB**, and smoothly rise during breath pauses:

```bash
# Automated Sidechain Ducking Script
ffmpeg -i voiceover.mp3 -i music.mp3 -filter_complex \
"[1:a]volume=0.35[music_vol]; \
 [music_vol][0:a]sidechaincompress=threshold=0.12:ratio=4:attack=20:release=350[ducked_music]; \
 [0:a][ducked_music]amix=inputs=2:duration=first:dropout_transition=2[mixed_audio]; \
 [mixed_audio]loudnorm=I=-14:LRA=7:tp=-1.5[out]" \
-map "[out]" -c:a aac -b:a 256k master_audio.mp3
```

---

## 3. Python Stem Mixer Tool (`scripts/mix_audio.py`)

Run the automated audio mixer:
```bash
python scripts/mix_audio.py \
  --voice voiceover.mp3 \
  --music music_track.mp3 \
  --sfx-manifest sfx_cues.json \
  --output master_mix.mp3
```

### SFX Manifest Format (`sfx_cues.json`):
```json
[
  { "time": 0.0, "file": "sfx/whoosh_entry.mp3", "volume": 0.8 },
  { "time": 2.35, "file": "sfx/pop_pointer.mp3", "volume": 0.6 },
  { "time": 5.10, "file": "sfx/sub_impact.mp3", "volume": 0.9 }
]
```

---

## 4. Audio Mastering Checklist (-14 LUFS)

- [ ] **Target Integrated Loudness**: -14.0 LUFS (±1 LUFS).
- [ ] **True Peak Ceiling**: -1.5 dBTP (prevents DAC clipping on phones).
- [ ] **Loudness Range (LRA)**: 6 to 9 LU (tight, consistent, readable on mobile speakers).
- [ ] **High-pass Filter**: Cut all frequencies below 80Hz on voiceover to remove mic rumble.

