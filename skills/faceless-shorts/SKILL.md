---
name: faceless-shorts
description: >-
  Nafay3D viral faceless video production workflow. Use this skill to create automated,
  high-retention 9:16 vertical videos (YouTube Shorts, Instagram Reels, TikTok) end-to-end.
  Covers viral hook formulas (21 hook taxonomy), text-to-speech voice generation, dynamic karaoke/ASS
  word-level caption overlays, Ken Burns B-roll motion, split-screen layouts with neon dividers,
  and retention-maximizing editing pacing (visual pattern interrupts every 2.5s).
---

# Nafay3D Faceless Shorts Pipeline (`faceless-shorts`)

The battle-tested viral short-form pipeline developed by Nafay3D for scaling automated, faceless channels across YouTube Shorts, Instagram Reels, and TikTok.

---

## 1. The Viral Anatomy (30–60s Formula)

1. **The 3-Second Scroll-Stopper**:
   - High-contrast visual + audio sounder + bold question/statement.
   - Example: *"What if I told you Earth is not actually round?"*
   - Never say "Welcome to my channel" or "In this video". Start in *medias res*.

2. **The 2.5-Second Pacing Rule**:
   - The eye resets focus every 2.5 seconds. If a single visual frame lingers past 3.0 seconds without motion, zoom, caption highlight, or SFX, retention drops by 35%.
   - Inject continuous motion: Ken Burns slow zooms, camera drift, animated stickers, or b-roll cutaways.

3. **High-Impact Kinetic Subtitles**:
   - Centered vertically (Y: ~1100–1250 on 1080x1920 canvas).
   - 1–3 words visible at a time.
   - Highlight current spoken word in bright yellow (`#facc15`) or cyan (`#38bdf8`) with black heavy outline.

4. **Split-Screen Layouts**:
   - Top 50%: Dynamic B-roll or 3D set animation.
   - Center: Glowing neon divider line (1080x4px cyan or magenta glow).
   - Bottom 50%: Secondary supporting visual, waveform, or stickman character narrator.

---

## 2. 21 Viral Hook Taxonomy

| Category | Hook Formula Example | Best For |
|----------|----------------------|----------|
| **The Negative Warning** | "Stop doing [common habit] right now, or this happens..." | Productivity / Health |
| **The Hidden Conspiracy** | "In 1983, a scientist discovered something so dark that..." | History / Mystery |
| **The Direct Challenge** | "Only 1% of people can solve this riddle in 5 seconds." | Trivia / Brain Teasers |
| **The Asymmetry** | "How this 16-year-old made $100,000 using only a free website." | Wealth / Business |
| **The Impossible Truth** | "Everything you know about [famous event] is completely fake." | Documentaries |

---

## 3. End-to-End Pipeline Commands

### 1. Generate Voiceover & Word Timestamps
```bash
python scripts/generate_tts.py --text "Script text here" --voice "en-US-ChristopherNeural" --output voice.mp3
```

### 2. Generate Word-Level ASS Captions
```bash
python scripts/generate_captions.py --audio voice.mp3 --output captions.ass --style viral_yellow
```

### 3. Assemble & Render Vertical Short
```bash
python scripts/render_faceless.py \
  --top broll.mp4 \
  --bottom narrator.mp4 \
  --audio voice.mp3 \
  --captions captions.ass \
  --output final_short.mp4
```

---

## 4. 9:16 Safe Zones Specification

```text
+------------------------------+  0px (Top)
|  CRITICAL DEAD ZONE (15%)    |  Avoid important text / faces
|  (Search bar, header UI)     |  0px - 288px
+------------------------------+  288px
|                              |
|                              |
|       ACTIVE CONTENT         |
|         SWEET SPOT           |
|      (Keep Stickman,         |
|       Evidence &             |
|       Action Here)           |  288px - 1450px
|                              |
|      [KINETIC CAPTIONS]      |  Y: 1150px - 1300px
|                              |
+------------------------------+  1450px
|  CRITICAL DEAD ZONE (25%)    |  Account name, sound title,
|  (Pill, CTA, Seekbar)        |  like/comment buttons (right 140px)
+------------------------------+  1920px (Bottom)
```

