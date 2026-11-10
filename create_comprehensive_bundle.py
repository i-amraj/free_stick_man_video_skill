"""
create_comprehensive_bundle.py
Assembles 100% of all skills across workspace and system:
- .agents/skills (all 22 workspace video skills)
- skills/ (top-level alias for agents that look for ./skills/)
- builtin_skills (Antigravity system skills: automation, customizations, generative UI, etc.)
- docs/ (Analysis reports, Playbooks, Guides, Style Guide, AGENTS.md, GEMINI.md)
- core_libraries/ (rig.js, props.js, gsap.min.js)
- templates_and_pipelines/ (10s, 20s dialogue, 65s master film)
- README.md
Outputs: growkaz_agent_bundle.zip (and copies to root and artifacts)
"""

import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man")
STAGE = ROOT / "bundle_staging"
OUTPUT_ZIP = ROOT / "growkaz_agent_bundle.zip"
ARTIFACTS_ZIP = Path(r"C:\Users\iamra\.gemini\antigravity\brain\c9b9d424-5a3c-4adf-aabc-2078a51c8ad6\growkaz_agent_bundle.zip")

if STAGE.exists():
    shutil.rmtree(STAGE)
STAGE.mkdir(parents=True)

# 1. Package .agents/skills
print("1. Packaging .agents directory...")
dest_agents = STAGE / ".agents"
shutil.copytree(ROOT / ".agents", dest_agents, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))

# 2. Also package top-level skills/
print("2. Packaging top-level skills/ directory...")
dest_skills = STAGE / "skills"
skills_src = ROOT / "skills"
if skills_src.exists():
    # If it's a symlink or directory, copy tree
    try:
        shutil.copytree(skills_src, dest_skills, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))
    except Exception as e:
        print("Note on skills copy:", e)
        # Fallback copy from .agents/skills
        shutil.copytree(ROOT / ".agents" / "skills", dest_skills, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))
else:
    shutil.copytree(ROOT / ".agents" / "skills", dest_skills, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))

# 3. Package Builtin Antigravity Skills
print("3. Packaging builtin system skills...")
builtin_src = Path(r"C:\Users\iamra\.gemini\antigravity\builtin\skills")
if builtin_src.exists():
    dest_builtin = STAGE / "builtin_skills"
    dest_builtin.mkdir(parents=True)
    shutil.copytree(builtin_src, dest_builtin, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))

# 4. Package docs and analysis reports
print("4. Packaging docs and analysis reports...")
dest_docs = STAGE / "docs"
dest_docs.mkdir(parents=True)

docs_src = ROOT / "projects" / "comicron_60s_full" / "docs"
if docs_src.exists():
    for f in docs_src.glob("*.md"):
        shutil.copy2(f, dest_docs / f.name)

shutil.copy2(ROOT / "AGENTS.md", dest_docs / "AGENTS.md")
shutil.copy2(ROOT / "GEMINI.md", dest_docs / "GEMINI.md")

# Also copy AGENTS.md and GEMINI.md to root of bundle
shutil.copy2(ROOT / "AGENTS.md", STAGE / "AGENTS.md")
shutil.copy2(ROOT / "GEMINI.md", STAGE / "GEMINI.md")

analysis_src = ROOT / "projects" / "channel_analysis"
if analysis_src.exists():
    dest_analysis = dest_docs / "channel_analysis_data"
    dest_analysis.mkdir(parents=True)
    for ext in ["*.json", "*.py"]:
        for f in analysis_src.glob(ext):
            shutil.copy2(f, dest_analysis / f.name)
    if (analysis_src / "transcripts").exists():
        shutil.copytree(analysis_src / "transcripts", dest_analysis / "transcripts")

# 5. Core Libraries
print("5. Packaging core libraries (rig.js, props.js, gsap.min.js)...")
dest_core = STAGE / "core_libraries"
dest_core.mkdir(parents=True)
shutil.copy2(ROOT / ".agents" / "skills" / "character-animation" / "assets" / "rig.js", dest_core / "rig.js")
shutil.copy2(ROOT / ".agents" / "skills" / "character-animation" / "assets" / "props.js", dest_core / "props.js")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "gsap.min.js", dest_core / "gsap.min.js")

# 6. Production Templates & Pipelines
print("6. Packaging production templates & working pipelines...")
dest_templates = STAGE / "templates_and_pipelines"
dest_templates.mkdir(parents=True)

# 10s Demo
t10 = dest_templates / "10s_character_demo"
t10.mkdir(parents=True)
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "demo_10s_character.html", t10 / "demo_10s_character.html")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "build_demo_10s_html.py", t10 / "build_demo_10s_html.py")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "render_demo_10s.py", t10 / "render_demo_10s.py")
shutil.copy2(dest_core / "rig.js", t10 / "rig.js")
shutil.copy2(dest_core / "props.js", t10 / "props.js")
shutil.copy2(dest_core / "gsap.min.js", t10 / "gsap.min.js")

# 20s Dialogue Video
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

# 65s Full Film
t65 = dest_templates / "65s_full_procedural_film"
t65.mkdir(parents=True)
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "build_procedural_components.py", t65 / "build_procedural_components.py")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "generate_scene_v2_ultra_detailed.py", t65 / "generate_scene_v2_ultra_detailed.py")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "render_full_film_parallel.py", t65 / "render_full_film_parallel.py")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "subtitle_chunks.json", t65 / "subtitle_chunks.json")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "word_timings.json", t65 / "word_timings.json")
shutil.copy2(dest_core / "gsap.min.js", t65 / "gsap.min.js")

# 7. Comprehensive Master README
readme_content = """# GrowKaz Stickman Studio — Complete Agent & Skills Master Bundle

Welcome to the all-in-one distribution bundle for **GrowKaz Stickman Studio**.
This package contains 100% of all skills, agent rules, reverse-engineering analysis reports, core libraries, and ready-to-run video production pipelines.

---

## 📂 Bundle Directory Overview

| Directory | Contents |
|---|---|
| **`.agents/skills/`** | All 22 specialized production skills (animation, backgrounds, camera motion, audio, captions) |
| **`skills/`** | Full root alias of all skills for agents/frameworks that read `./skills/` |
| **`builtin_skills/`** | Antigravity system skills (`automation`, `antigravity_guide`, `generative_ui`, `plugin`, etc.) |
| **`docs/`** | Deep channel analysis reports (`ANALYSIS_REPORT.md`), `AGENT_PLAYBOOK.md`, `CHARACTER_ANIMATION_GUIDE.md`, and transcripts |
| **`core_libraries/`** | `rig.js` (FK-by-rotation, 5 face shapes, lip-sync), `props.js` (~35 SVG props), and `gsap.min.js` |
| **`templates_and_pipelines/`** | Working 10s demo, 20s dialogue video, and 65s full procedural master film pipelines |
| **`AGENTS.md` / `GEMINI.md`** | Master instructions, skill execution map, and workspace rules |

---

## 🏆 The 3 Immutable Production Laws

1. **"Camera Kabhi Rukta Nahi"** (`gsap-motion`):
   - The camera NEVER stands completely still. It maintains continuous motion (slow push-in, subtle lateral tracking, or organic handheld sway) across every single frame.
   - Pacing: Visual change or focal nudge every **2.0 to 2.8 seconds**.
2. **Forward Kinematics by Rotation** (`character-animation`):
   - Never move bones by editing `x2, y2` coordinates.
   - Every bone rotates around its joint pivot (`translate -> rotate`). All child bones are nested inside parents. Limbs can never separate.
   - Supports 5 face shapes: `square` (chiseled jaw), `pointed` (sly chin), `oval`, `chubby`, and `round`.
3. **100% Procedural SVG Environments** (`procedural-backgrounds`):
   - Zero external raster images. Everything (walls, timber beams, cobblestones, windows, fireplaces, shadows, crates, chairs, tables, coins, shoes) is procedurally authored in pure SVG code.

---

## 🚀 How to Execute with Any AI Agent

1. Unzip this package in any empty workspace directory.
2. Instruct the agent:
   > *"You are the GrowKaz Stickman Studio director. Read `AGENTS.md` and `docs/AGENT_PLAYBOOK.md` first. Use `skills/character-animation` and `skills/gsap-motion` to generate high-retention 9:16 vertical videos matching the narration 100%."*
3. The agent will have access to all skills, rigs, props, and rendering scripts out of the box!
"""

with open(STAGE / "README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("8. Compressing into growkaz_agent_bundle.zip...")
if OUTPUT_ZIP.exists():
    OUTPUT_ZIP.unlink()

with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(STAGE):
        for f in files:
            full_p = Path(root) / f
            rel_p = full_p.relative_to(STAGE)
            zf.write(full_p, rel_p)

# Copy to artifacts
shutil.copy2(OUTPUT_ZIP, ARTIFACTS_ZIP)

# Clean up staging
shutil.rmtree(STAGE)

size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
print(f"SUCCESS: Comprehensive Master Bundle created at {OUTPUT_ZIP} ({size_mb:.2f} MB)")
print(f"Artifact copy saved to: {ARTIFACTS_ZIP}")

