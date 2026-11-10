---
name: ai-video-editor
description: >-
  Nafay3D automated AI video editing workflow. Use this skill to automatically cut out pauses,
  breaths, and silences, create dynamic jump-cuts with punch-in camera zooms (100% to 115%),
  overlay dynamic B-roll clips, insert SFX markers at transition points, and auto-master speech audio
  to broadcast loudness standards (-14 LUFS).
---

# Nafay3D AI Video Editor (`ai-video-editor`)

Automated, code-driven video editing designed to eliminate repetitive manual timeline tasks: automatic silence removal, dynamic jumpcut zooms, auto-leveling audio, and overlaying synchronized B-roll.

---

## 1. Automated Silence Removal & Jumpcutter

Cuts all pauses, breaths, and dead air longer than 0.4 seconds, tightening talking-head or voiceover pacing to modern retention standards:

```bash
python scripts/auto_silence_cut.py raw_input.mp4 tight_output.mp4 --threshold -32 --min-silence 0.4
```

### Parameters:
- `--threshold`: Audio silence decibel threshold (default `-30dB` to `-34dB`).
- `--min-silence`: Minimum silence duration to trigger a cut (default `0.4s`).
- `--padding`: Buffer kept around spoken words to prevent cutting off plosives (default `0.05s`).

---

## 2. Dynamic Jump-Cut Punch-Ins

To prevent jump-cuts from looking jarring or amateurish, the editor alternates between two focal lengths at every cut point:
- **Cut A**: Normal framing (100% scale, centered).
- **Cut B**: Punch-in framing (115% scale, slight crop on subject's eyes).

```bash
python scripts/punch_in_cutter.py tight_output.mp4 punch_output.mp4 --zoom 1.15
```

---

## 3. Automated Audio Leveller & Voice Enhancer

Applies high-pass filter, compression, and loudness normalization in a single pass:

```bash
ffmpeg -i input.mp4 -af "highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=15:release=150,loudnorm=I=-14:LRA=7:tp=-1.5" -c:v copy enhanced.mp4
```

---

## 4. B-Roll Ken Burns Motion Generator

Turns any static 2D image or evidence screenshot into a dynamic 1080x1920 video clip with slow cinematic zoom:

```bash
# Slow 4-second zoom-in
ffmpeg -loop 1 -i evidence.jpg -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0015,1.15)':d=120:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30" -t 4 -c:v libx264 -pix_fmt yuv420p broll_animated.mp4
```

