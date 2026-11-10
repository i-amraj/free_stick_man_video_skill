# Comicron Video Production Agent Playbook

> **Purpose**: This playbook gives any AI agent or software engineer complete end-to-end instructions to inspect, extend, modify, or render full Comicron-style vertical 9:16 viral videos directly from code.

---

## 1. Architecture Overview

Comicron videos combine:
1. **Photorealistic Stylized 3D Low-Poly Environments**: Pre-rendered 9:16 background sets with volumetric lighting, atmospheric fog, and depth.
2. **Hierarchical 2D Vector Puppets**: SVG bean/stickman characters with locked 7px linework, white circular heads, segmented torso/limbs, and physics-driven GSAP animation.
3. **Continuous Kinetic Camera**: Subtle continuous pan/zoom/sway ("Camera Kabhi Rukta Nahi") maintaining visual momentum.
4. **Deterministic Virtual Clock**: `window.seekToTime(t)` allowing frame-accurate headless rendering (Playwright) at 30 FPS with zero frame drops or audio drift.
5. **Dynamic Kinetic Captions**: Montserrat 900 uppercase karaoke word highlights synchronized to Whisper word-level timestamps.

---

## 2. Directory Structure

```
projects/comicron_60s_full/
├── assets/
│   ├── master_audio_65s.mp3          # Full voiceover + background music bed (65.5s)
│   ├── bg_scene1_shop_night.jpg      # 3D low-poly cobbler workshop (night)
│   ├── bg_scene2_window.jpg          # 3D low-poly shop exterior window
│   ├── bg_scene3_street.jpg          # 3D low-poly European cobblestone street (day)
│   ├── bg_scene4_winter.jpg          # 3D low-poly winter workshop with fireplace
│   └── bg_scene5_grand_shop.jpg      # 3D low-poly luxury shoe boutique
├── docs/
│   ├── ANALYSIS_REPORT.md            # Deep reverse-engineering analysis of original channel
│   ├── STYLE_GUIDE.md                # Character proportions, color tokens, typography laws
│   └── AGENT_PLAYBOOK.md             # This document (operational guide for agents)
├── word_timings.json                 # 214 words with exact start/end timestamps from Whisper
├── scene.html                        # Master 65.5s HTML/GSAP animation composition
├── render_full_video.py              # Parallel chunk renderer & FFmpeg assembler
└── inspect_story.py                  # CLI utility to inspect story beats & word timings
```

---

## 3. The 8-Scene Storyboard Breakdown (65.5 Seconds)

| Scene | Time Range | Beat Range | Background Asset | Key Action / Puppets |
|---|---|---|---|---|
| **Scene 1** | 0.0s – 5.2s | Beat 01 | `bg_scene1_shop_night.jpg` | Thief in dark cloak dangling from skylight rope, grabbing left shoe from shelf. |
| **Scene 2** | 5.2s – 8.2s | Beats 02–03 | `bg_scene3_street.jpg` | Chief Guard in tall top hat & Deputy Guard in fedora laughing on sunny street. |
| **Scene 3** | 8.2s – 18.0s | Beats 04–07 | `bg_scene2_window.jpg` | Corvin holding "ONE RIGHT SHOE HALF PRICE" wooden sign by shop window. |
| **Scene 4** | 18.0s – 24.5s | Beats 08–10 | `bg_scene1_shop_night.jpg` | 2 Guards hiding behind counter at night; glowing green left boots vanish with smoke. |
| **Scene 5** | 24.5s – 29.0s | Beats 11–12 | `bg_scene3_street.jpg` | Cobblestone street, kids hopping on one foot past "The Hopping Shop". |
| **Scene 6** | 29.0s – 33.2s | Beats 13–14 | `bg_scene4_winter.jpg` | Broke Corvin shivering next to dying fireplace embers and unsold right shoes. |
| **Scene 7** | 33.2s – 41.7s | Beats 15–17 | `bg_scene1_shop_night.jpg` | Quiet stranger walks into shop, drops 5 gold coins onto counter for "firewood". Corvin weeps. |
| **Scene 8** | 41.7s – 65.5s | Beats 18–23 | `bg_scene5_grand_shop.jpg` | Grand boutique, 300 complete pairs on shelves. Stranger behind counter smiling as wealthiest cobbler. |

---

## 4. How to Modify or Extend the Pipeline

### Adding a New Video Script:
1. Place voiceover audio into `assets/master_audio.mp3`.
2. Extract word-level timestamps using Whisper:
   ```bash
   python -c "import whisper, json; model = whisper.load_model('base'); res = model.transcribe('assets/master_audio.mp3', word_timestamps=True); json.dump(res, open('word_timings.json', 'w'), indent=2)"
   ```
3. Generate 3D background sets following `docs/STYLE_GUIDE.md` prompt syntax.
4. Update `scene.html` with SVG characters and GSAP timeline events.

### Rendering the Video:
```bash
python projects/comicron_60s_full/render_full_video.py
```
This headless script uses Playwright to seek `window.seekToTime(t)` frame-by-frame (30 FPS), saves high-res JPEG frames into a temp buffer, and encodes `comicron_60s_full.mp4` via FFmpeg with H.264 video and AAC audio.

---

## 5. Subtitle System Doctrine

Per user specification, subtitles strictly follow **Demo 1 Style**:
- Font: `'Montserrat', sans-serif`, weight `900`.
- Text transformation: `UPPERCASE`, letter-spacing `1.5px`.
- Inactive words: White (`#FFFFFF`) with dense multi-directional black shadow.
- Active highlighted word: Bright Yellow (`#FFD700`), scaled `1.18x` with golden glow drop-shadow.
- Word gap: Minimum `18px – 24px` to prevent touching letters.

