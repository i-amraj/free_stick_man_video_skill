import os
import shutil
import zipfile
from pathlib import Path

ROOT = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man")
STAGE = ROOT / "bundle_staging"
OUTPUT_ZIP = ROOT / "growkaz_agent_bundle.zip"
ARTIFACTS_ZIP = Path(r"C:\Users\iamra\.gemini\antigravity\brain\c9b9d424-5a3c-4adf-aabc-2078a51c8ad6\growkaz_agent_bundle.zip")

print("Cleaning staging directory...")
if STAGE.exists():
    shutil.rmtree(STAGE, ignore_errors=True)
STAGE.mkdir(parents=True, exist_ok=True)

# Locations of all skills to gather
dest_agents_skills = STAGE / ".agents" / "skills"
dest_skills = STAGE / "skills"
dest_agents_skills.mkdir(parents=True, exist_ok=True)
dest_skills.mkdir(parents=True, exist_ok=True)

skill_sources = [
    # 1. stick_man workspace skills (22 skills)
    (ROOT / ".agents" / "skills", "workspace"),
    # 2. GSAP deep-dive skills
    (Path(r"C:\Users\iamra\.gemini\antigravity\skills\gsap-skills-repo\skills"), "gsap"),
    # 3. Facts video skills (ai-video-generation, manim, b-roll, youtube-agent, etc.)
    (Path(r"c:\Users\iamra\OneDrive\Desktop\facts\.agents\skills"), "facts"),
    # 4. UI/UX pro max modular skills
    (Path(r"c:\Users\iamra\OneDrive\Desktop\raj_project\.skills\ui-ux-pro-max-skill\.claude\skills"), "ui_ux_modular"),
    # 5. Other user skills
    (Path(r"C:\Users\iamra\.gemini\antigravity\skills"), "antigravity_user"),
    # 6. Builtin skills
    (Path(r"C:\Users\iamra\.gemini\antigravity\builtin\skills"), "builtin"),
]

copied_skills = set()

def copy_skill_folder(src_folder: Path, skill_name: str):
    if not (src_folder / "SKILL.md").exists():
        return False
    # Target in .agents/skills
    target1 = dest_agents_skills / skill_name
    # Target in skills/
    target2 = dest_skills / skill_name
    
    if skill_name in copied_skills:
        print(f"  [Skipping duplicate] {skill_name}")
        return True
    
    print(f"  [Adding Skill] {skill_name} from {src_folder}")
    shutil.copytree(src_folder, target1, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))
    shutil.copytree(src_folder, target2, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))
    copied_skills.add(skill_name)
    return True

print("\n--- GATHERING ALL SKILLS ACROSS ALL SOURCES ---")
for source_dir, label in skill_sources:
    if not source_dir.exists():
        print(f"Directory not found: {source_dir}")
        continue
    print(f"\nScanning {label} directory: {source_dir}")
    for item in source_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            copy_skill_folder(item, item.name)

print(f"\nTotal unique skills packaged into .agents/skills and skills/: {len(copied_skills)}")

# Also package builtin skills into their own dedicated directory as well
dest_builtin = STAGE / "builtin_skills"
builtin_src = Path(r"C:\Users\iamra\.gemini\antigravity\builtin\skills")
if builtin_src.exists():
    shutil.copytree(builtin_src, dest_builtin, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git*"))

# Also copy AGENTS.md, GEMINI.md, HARNESS.md, and harness.py into standard agent root dirs
print("\n--- PACKAGING AGENT WORKSPACE INSTRUCTIONS ---")
shutil.copy2(ROOT / "AGENTS.md", STAGE / "AGENTS.md")
shutil.copy2(ROOT / "GEMINI.md", STAGE / "GEMINI.md")
shutil.copy2(ROOT / "HARNESS.md", STAGE / "HARNESS.md")
shutil.copy2(ROOT / "harness.py", STAGE / "harness.py")
if (ROOT / "harness").exists():
    shutil.copytree(ROOT / "harness", STAGE / "harness", dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

# Also package for Claude Code (.claude), Cursor (.cursor), and Windsurf
claude_dir = STAGE / ".claude"
cursor_dir = STAGE / ".cursor"
claude_dir.mkdir(parents=True, exist_ok=True)
cursor_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / "AGENTS.md", claude_dir / "CLAUDE.md")
shutil.copy2(ROOT / "AGENTS.md", cursor_dir / "rules")

# 4. Package docs and analysis reports
print("\n--- PACKAGING DOCS & ANALYSIS REPORTS ---")
dest_docs = STAGE / "docs"
dest_docs.mkdir(parents=True, exist_ok=True)

docs_src = ROOT / "projects" / "comicron_60s_full" / "docs"
if docs_src.exists():
    for f in docs_src.glob("*.md"):
        shutil.copy2(f, dest_docs / f.name)

shutil.copy2(ROOT / "AGENTS.md", dest_docs / "AGENTS.md")
shutil.copy2(ROOT / "GEMINI.md", dest_docs / "GEMINI.md")

analysis_src = ROOT / "projects" / "channel_analysis"
if analysis_src.exists():
    dest_analysis = dest_docs / "channel_analysis_data"
    dest_analysis.mkdir(parents=True, exist_ok=True)
    for ext in ["*.json", "*.py"]:
        for f in analysis_src.glob(ext):
            shutil.copy2(f, dest_analysis / f.name)
    if (analysis_src / "transcripts").exists():
        shutil.copytree(analysis_src / "transcripts", dest_analysis / "transcripts", dirs_exist_ok=True)

# 5. Core Libraries
print("\n--- PACKAGING CORE LIBRARIES ---")
dest_core = STAGE / "core_libraries"
dest_core.mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / ".agents" / "skills" / "character-animation" / "assets" / "rig.js", dest_core / "rig.js")
shutil.copy2(ROOT / ".agents" / "skills" / "character-animation" / "assets" / "props.js", dest_core / "props.js")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "gsap.min.js", dest_core / "gsap.min.js")

# 6. Production Templates & Pipelines
print("\n--- PACKAGING WORKING PIPELINES ---")
dest_templates = STAGE / "templates_and_pipelines"
dest_templates.mkdir(parents=True, exist_ok=True)

# 10s Demo
t10 = dest_templates / "10s_character_demo"
t10.mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "demo_10s_character.html", t10 / "demo_10s_character.html")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "build_demo_10s_html.py", t10 / "build_demo_10s_html.py")
shutil.copy2(ROOT / "projects" / "comicron_60s_full" / "render_demo_10s.py", t10 / "render_demo_10s.py")

# 20s Dialogue Video
t20 = dest_templates / "20s_dialogue_video"
t20.mkdir(parents=True, exist_ok=True)
for item in (ROOT / "projects" / "video_20s_dialogue").glob("*"):
    if item.is_file() and not item.name.endswith(".mp4"):
        shutil.copy2(item, t20 / item.name)

# 65s Full Procedural Film
t65 = dest_templates / "65s_full_procedural_film"
t65.mkdir(parents=True, exist_ok=True)
for fname in ["index.html", "render_master.py", "generate_audio.py", "align_timestamps.py", "master_film.json"]:
    p = ROOT / "projects" / "comicron_60s_full" / fname
    if p.exists():
        shutil.copy2(p, t65 / fname)

# 7. Comprehensive Master README.md
readme_content = f"""# GrowKaz Stickman Studio — All-In-One Master Agent Bundle

Welcome to the **GrowKaz Stickman Studio** complete AI agent bundle.
This archive contains **EVERY SINGLE SKILL** ({len(copied_skills)} skills), full FK character rig with custom face shapes, ~35 pure SVG props, procedural backgrounds engine, continuous camera motion doctrines, and tested end-to-end video pipelines.

---

## 🌟 What Is Included in This Archive

### 1. Skills (Total: {len(copied_skills)} Complete Skills)
All skills are packaged in both `.agents/skills/` AND top-level `skills/` for universal compatibility with Antigravity, Claude Code, Cursor, Windsurf, Roo Code, and Gemini CLI.

#### A. Core 2D Stickman & Video Production Skills
1. **character-animation** — FK by rotation rig (`rig.js`), 5 face styles (square, pointed, oval, chubby, round), ~35 SVG props (`props.js`), viseme lip-sync (`hero.talk()`), walk/run/dance cycles, ground contact.
2. **procedural-backgrounds** — 100% SVG code-only sets (medieval rooms, boutique shops, cobblestone alleys, winter streetlamps).
3. **gsap-motion** — "Camera Kabhi Rukta Nahi" continuous camera motion law, velocity-matched seams, punch zooms, handheld micro-drift.
4. **make-2d-video** — Multi-scene 2D production orchestrator, character staging, and timeline composition.
5. **new-video** — Scaffolding, 3-second beat breakdown, script-to-storyboard generation.
6. **video-styles** — Aesthetic lock-in ("look lock"), 7px stroke rule, 4 color palettes (`growkaz_mystery`).
7. **video-sound** — Voiceover synthesis, whoosh/pop SFX taxonomy, auto-ducking BGM (-14 LUFS broadcast standard).
8. **render-video** — Headless frame-accurate capture via deterministic virtual clock (`window.seekToTime(t)`), 5-gate automated QC.
9. **captions-overlay** — Kinetic karaoke typography, gold highlight `#FFD700`, 9:16 safe zones.

#### B. Seam & Cinematic Motion Skills
10. **motion-doctrine** — The vector law, carrier elements, causal motion, stillness before climax.
11. **cut-the-curve** — 5 velocity-matched transitions (zoom-through, waterfall, rack-focus blur).
12. **seam-craft** — Zero white-flash guard, stage-ground compositing, seamless scene handoffs.
13. **oversized-cursor** — Eye-carrier cursor, off-screen entry, click-ignition sequences.

#### C. Viral, Shorts & Editing Skills
14. **faceless-shorts** — Nafay3D 21-hook formula, neon split-screen layouts, 9:16 viral shorts.
15. **ai-video-editor** — Auto silence cutting, jumpcut punch-ins, B-roll overlays.
16. **changelog-video** — Branded markdown-to-video workflow.
17. **remotion-video** — Programmatic React motion graphics.
18. **remotion-to-hyperframes** — Code migration & frame verification.
19. **hyperframes** & **hyperframes-cli** — Deterministic HTML video renderer & CLI.
20. **threejs-scenes** — 3D stylized sets (Mystery Noir, Tech Vault, Minimalist Studio) composited with 2D.
21. **ui-ux-pro-max** — Full UI/UX intelligence, evidence cards, fonts, and charts.

#### D. Specialized Deep-Dive Animation & UI Skills
22. **gsap-core**, **gsap-timeline**, **gsap-scrolltrigger**, **gsap-plugins**, **gsap-react**, **gsap-frameworks**, **gsap-performance**, **gsap-utils** — The entire official GSAP mastery suite.
23. **banner-design**, **brand**, **design**, **design-system**, **slides**, **ui-styling** — Modular design intelligence.
24. **ai-video-generation**, **manim-animation**, **short-video-pipeline**, **b-roll-animator**, **visual-analyzer**, **youtube-agent**, **fact-storyboard-writer** — Facts & educational video animation skills.
25. **auto-job-applicator**, **permissioned-github**, **native_swarm**, **swarm_monitor**, **automation**, **generative_ui**, **plugin**, **antigravity_guide** — Workflow automation & agent orchestration.

---

## 2. Core Libraries (`core_libraries/`)
- `rig.js` — The official Forward Kinematics 2D Stickman rig with customizable head shapes, facial hair, clothing, visemes, and poses.
- `props.js` — ~35 pure SVG props (chest, coins, stinky shoe, crate, table, chair, sword, torch, magnifier, etc.).
- `gsap.min.js` — Bundled GreenSock Animation Platform library.

---

## 3. Working Pipelines & Templates (`templates_and_pipelines/`)
- `10s_character_demo/` — Working demo showcasing walking, running, crouching, jumping, and dancing.
- `20s_dialogue_video/` — Complete working 20-second project with Gary & Thief talking, lip-sync, shock reveals, custom faces, and continuous camera motion.
- `65s_full_procedural_film/` — The complete 8-scene procedural film pipeline.

---

## 4. Documentation & Intelligence (`docs/`)
- `ANALYSIS_REPORT.md` — Deep reverse-engineering of Comicron's viral style, motion curves, retention drivers, and audio architecture.
- `AGENT_PLAYBOOK.md` — Step-by-step instructions for an AI agent to build a new video from scratch.
- `CHARACTER_ANIMATION_GUIDE.md` — Rigging, angles, visemes, and animation guidelines.
- `STYLE_GUIDE.md` — Color palettes, font pairings, stroke weights, and safe zones.
- `AGENTS.md` & `GEMINI.md` — Complete workspace rules and instructions.

---

## 🚀 How to Use With Any AI Agent

1. Extract this zip archive into your project directory.
2. The rules in `AGENTS.md` (or `CLAUDE.md`, `.cursor/rules`) will automatically guide your AI agent.
3. Your agent will recognize all {len(copied_skills)} skills in `.agents/skills/` and `skills/`.
4. Prompt your agent:
   > *"Read AGENTS.md and use make-2d-video and character-animation to create a video based on my script."*
"""

with open(STAGE / "README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

# 8. Create the ZIP archive
print("\n--- CREATING MASTER ZIP ARCHIVE ---")
if OUTPUT_ZIP.exists():
    OUTPUT_ZIP.unlink()

with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
    for root, dirs, files in os.walk(STAGE):
        for file in files:
            full_path = Path(root) / file
            rel_path = full_path.relative_to(STAGE)
            zipf.write(full_path, rel_path)

print(f"Zip created successfully: {OUTPUT_ZIP} ({OUTPUT_ZIP.stat().st_size / (1024*1024):.2f} MB)")

# Copy to artifacts directory as well
shutil.copy2(OUTPUT_ZIP, ARTIFACTS_ZIP)
print(f"Copied to artifacts: {ARTIFACTS_ZIP}")

# Verify contents
with zipfile.ZipFile(OUTPUT_ZIP, "r") as z:
    file_list = z.namelist()
    print(f"Total files in master zip: {len(file_list)}")
    skill_mds = [f for f in file_list if f.endswith("SKILL.md") and f.startswith("skills/")]
    print(f"Skills verified in skills/: {len(skill_mds)}")
    for s in skill_mds:
        print("  -", s)

print("\n--- ALL DONE SUCCESSFULLY! ---")

