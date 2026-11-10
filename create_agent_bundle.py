"""
create_agent_bundle.py
Assembles all skills, agent rules, analysis reports, core libraries,
and working pipeline templates into a single master ZIP file: growkaz_agent_bundle.zip
"""

import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man")
STAGE = ROOT / "bundle_staging"
OUTPUT_ZIP = ROOT / "growkaz_agent_bundle.zip"

if STAGE.exists():
    shutil.rmtree(STAGE)
STAGE.mkdir(parents=True)

print("1. Packaging .agents/skills directory...")
dest_agents = STAGE / ".agents"
shutil.copytree(ROOT / ".agents", dest_agents, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))

print("2. Packaging docs and analysis reports...")
dest_docs = STAGE / "docs"
dest_docs.mkdir(parents=True)

# Copy docs from projects/comicron_60s_full/docs
docs_src = ROOT / "projects" / "comicron_60s_full" / "docs"
if docs_src.exists():
    for f in docs_src.glob("*.md"):
        shutil.copy2(f, dest_docs / f.name)

# Copy AGENTS.md and GEMINI.md
shutil.copy2(ROOT / "AGENTS.md", dest_docs / "AGENTS.md")
shutil.copy2(ROOT / "GEMINI.md", dest_docs / "GEMINI.md")

# Copy target_videos.json and video metadata from channel_analysis
analysis_src = ROOT / "projects" / "channel_analysis"
if analysis_src.exists():
    dest_analysis = dest_docs / "channel_analysis_data"
    dest_analysis.mkdir(parents=True)
    for ext in ["*.json", "*.py"]:
        for f in analysis_src.glob(ext):
            shutil.copy2(f, dest_analysis / f.name)
    if (analysis_src / "transcripts").exists():
        shutil.copytree(analysis_src / "transcripts", dest_analysis / "transcripts")

print("3. Packaging core libraries (rig.js, props.js, gsap.min.js)...")
dest_core = STAGE / "core_libraries"
dest_core.mkdir(parents=True)
shutil.copy2(ROOT / ".agents" / "skills" / "character-animation" / "assets" / "rig.js", dest_core / "rig.js")
shutil.copy2(ROOT / ".agents" / "skills" / "character-animation" / "assets" / "props.js", dest_core / "props.js")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "gsap.min.js", dest_core / "gsap.min.js")

print("4. Packaging production templates & working pipelines...")
dest_templates = STAGE / "templates_and_pipelines"
dest_templates.mkdir(parents=True)

# 4A. 10s Character Demo Template
t10 = dest_templates / "10s_character_demo"
t10.mkdir(parents=True)
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "demo_10s_character.html", t10 / "demo_10s_character.html")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "build_demo_10s_html.py", t10 / "build_demo_10s_html.py")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "render_demo_10s.py", t10 / "render_demo_10s.py")
shutil.copy2(dest_core / "rig.js", t10 / "rig.js")
shutil.copy2(dest_core / "props.js", t10 / "props.js")
shutil.copy2(dest_core / "gsap.min.js", t10 / "gsap.min.js")

# 4B. 20s Dialogue Video Template (with continuous camera & custom faces)
t20 = dest_templates / "20s_dialogue_video"
t20.mkdir(parents=True)
shutil.copy2(ROOT / "projects" / "video_20s_dialogue" / "scene_20s.html", t20 / "scene_20s.html")
shutil.copy2(ROOT / "projects" / "video_20s_dialogue" / "build_scene_20s_html.py", t20 / "build_scene_20s_html.py")
shutil.copy2(ROOT / "projects" / "video_20s_dialogue" / "build_audio_with_dialogue.py", t20 / "build_audio_with_dialogue.py")
shutil.copy2(ROOT / "projects" / "video_20s_dialogue" / "render_20s_video.py", t20 / "render_20s_video.py")
shutil.copy2(ROOT / "projects" / "video_20s_dialogue" / "audio_master_20s.mp3", t20 / "audio_master_20s.mp3")
shutil.copy2(ROOT / "projects" / "video_20s_dialogue" / "subtitle_chunks_20s.json", t20 / "subtitle_chunks_20s.json")
shutil.copy2(ROOT / "projects" / "video_20s_dialogue" / "word_timings_20s.json", t20 / "word_timings_20s.json")
shutil.copy2(dest_core / "rig.js", t20 / "rig.js")
shutil.copy2(dest_core / "props.js", t20 / "props.js")
shutil.copy2(dest_core / "gsap.min.js", t20 / "gsap.min.js")

# 4C. Full 65s Procedural Master Film Template
t65 = dest_templates / "65s_full_procedural_film"
t65.mkdir(parents=True)
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "build_procedural_components.py", t65 / "build_procedural_components.py")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "generate_scene_v2_ultra_detailed.py", t65 / "generate_scene_v2_ultra_detailed.py")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "render_full_film_parallel.py", t65 / "render_full_film_parallel.py")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "subtitle_chunks.json", t65 / "subtitle_chunks.json")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "word_timings.json", t65 / "word_timings.json")
shutil.copy2(dest_core / "gsap.min.js", t65 / "gsap.min.js")

# 5. Master README for the AI Agent
readme_content = """# GrowKaz Stickman Studio — Master Agent Package

This package contains everything an AI Agent or Developer needs to generate, animate, and render 100% code-based viral 2D stickman / toon videos in the signature Comicron / GrowKaz style.

---

## 📁 Package Directory Map

```
growkaz_agent_bundle/
├── .agents/skills/              # 21 Programmatic Animation & Video Skills
│   ├── character-animation/     # Master FK-by-rotation rig, face shapes, IK, lip-sync
│   ├── procedural-backgrounds/  # 100% SVG procedural sets (zero image files)
│   ├── gsap-motion/             # "Camera Kabhi Rukta Nahi" (continuous camera & parallax)
│   ├── motion-doctrine/         # Vector law, momentum cuts, causal motion
│   ├── cut-the-curve/           # 5 velocity-matched transition seams
│   ├── seam-craft/              # Render correctness, zero white-flash
│   ├── captions-overlay/        # Montserrat 900 gold karaoke subtitles
│   ├── video-sound/             # -14 LUFS broadcast audio, SFX & ducking
│   ├── video-styles/            # Look lock (growkaz_mystery)
│   └── ui-ux-pro-max/           # Design intelligence, HUD cards & color palettes
├── docs/                        # Project Intelligence & Analysis Reports
│   ├── ANALYSIS_REPORT.md       # Comicron Channel Deep Reverse-Engineering Report
│   ├── AGENT_PLAYBOOK.md        # Step-by-step playbook for AI coding agents
│   ├── CHARACTER_ANIMATION_GUIDE.md # Rig v2.0 reference, face styles & IK
│   ├── STYLE_GUIDE.md           # Locked dimensions, stroke weights & color palettes
│   ├── AGENTS.md / GEMINI.md    # Workspace intelligence & system prompt rules
│   └── channel_analysis_data/   # Transcripts & metadata from analyzed reference videos
├── core_libraries/              # Direct Production JS Engines
│   ├── rig.js                   # Forward-Kinematics Rig v2.0 with custom face shapes
│   ├── props.js                 # ~35 pure SVG procedural props & costumes
│   └── gsap.min.js              # GSAP 3.12 Deterministic Virtual Clock
└── templates_and_pipelines/     # Complete, working project pipelines
    ├── 10s_character_demo/      # 10s welded skeleton demonstration
    ├── 20s_dialogue_video/      # 20s dialogue video (continuous camera, character speech)
    └── 65s_full_procedural_film/# Complete 8-scene 65s procedural master film
```

---

## ⚡ The 3 Immutable Production Laws

1. **"Camera Kabhi Rukta Nahi"** (`gsap-motion`):
   - The camera NEVER stands completely still. It maintains continuous motion (slow push-in, subtle lateral tracking, or organic handheld sway) across every single frame.
   - Pacing: A visual change, pose shift, or camera focal nudge must occur every 2.0 to 2.8 seconds.
2. **Forward Kinematics by Rotation** (`character-animation`):
   - Never move bones by editing `x2, y2` coordinates.
   - Every bone rotates around its joint pivot (`translate -> rotate`). All child bones are nested inside parents. Limbs can never separate.
   - Supports 5 face shapes: `square` (chiseled jaw), `pointed` (sly chin), `oval`, `chubby`, and `round`.
3. **100% Procedural SVG Environments** (`procedural-backgrounds`):
   - Zero external raster images. Everything (walls, timber beams, cobblestones, windows, fireplaces, shadows, crates, chairs, tables, coins, shoes) is procedurally authored in pure SVG code.

---

## 🚀 How Any Agent Can Render a New Video

1. **Step 1: Audio & Subtitles**
   - Place voiceover in `audio_master.mp3`.
   - Transcribe with Whisper to extract word timestamps (`word_timestamps=True`).
2. **Step 2: HTML Scene Composition**
   - Import `gsap.min.js`, `rig.js`, and `props.js`.
   - Create characters: `const hero = GK.createCharacter(stage, { view: 'side', headShape: 'square' })`.
   - Animate poses, walking, speech lip-sync (`hero.talk()`), and continuous camera movement on ONE master timeline `masterTimeline`.
   - Expose `window.seekToTime = function(t) { masterTimeline.seek(t, false); updateSubtitles(t); }`.
3. **Step 3: Headless Parallel Render**
   - Run the 4-worker Playwright script (`render_20s_video.py`).
   - Frames are saved deterministically at 30 FPS.
   - FFmpeg encodes the final 9:16 vertical MP4 (`libx264 -preset slow -crf 18 -c:a aac -b:a 192k`).
"""

with open(STAGE / "README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("5. Compressing into growkaz_agent_bundle.zip...")
if OUTPUT_ZIP.exists():
    OUTPUT_ZIP.unlink()

with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(STAGE):
        for f in files:
            full_p = Path(root) / f
            rel_p = full_p.relative_to(STAGE)
            zf.write(full_p, rel_p)

# Clean up staging
shutil.rmtree(STAGE)

size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
print(f"SUCCESS: Master Agent Bundle created at {OUTPUT_ZIP} ({size_mb:.2f} MB)")

