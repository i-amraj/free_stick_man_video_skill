# 🎬 Free Stickman 2D Video Animation & Production Skills
### Programmatic 2D Stickman Engine for AI Agents & Developers

Welcome to **`free_stick_man_video_skill`** — an end-to-end, code-only programmatic 2D video animation and stickman production framework inspired by high-retention storytelling channels like Comicron and GrowKaz.

Designed for AI Coding Agents (**Antigravity, Claude Code, Cursor, Windsurf, Roo Code, Gemini CLI**) and human creators.

---

## ⚡ Automated Production Harness (`HARNESS.md`)

This repository includes a fully automated **Production Harness** (`harness.py` & `harness/`) that guides any AI agent or developer through creating a complete, high-retention 2D stickman video from raw script to broadcast-ready MP4.

```bash
# 1. Run Automated Harness Verification (Tests all 5 gates)
python harness.py --test

# 2. Produce a complete video from any script in one command
python harness.py --script "Detective Gary investigates a dark medieval alley. A sneaky thief jumps from the shadows with a stolen gold coin! Gary points his magnifying glass and shocks the thief." --output my_video.mp4

# 3. Run reference 20s dialogue demo
python harness.py --demo
```

For complete step-by-step specifications, read [`HARNESS.md`](./HARNESS.md).

---

## 🚀 Key Features

- 🦴 **Forward Kinematics (FK) Stickman Rig (`rig.js`)**:
  - Angle-based child joint rotation (`translate(joint) -> rotate(angle)`) — **zero detached limbs**.
  - **5 Distinct Head Shapes**: `'square'` (detective jaw), `'pointed'` (sharp sly chin), `'oval'`, `'chubby'`, `'round'`.
  - **Facial Hair & Expressions**: Beards, mustache, stubble, viseme lip-sync (`AA`, `EE`, `OO`, `MBP`, `FV`).
  - **Clothing & Outerwear**: Double-breasted trench coats, lapels, ties, crowns, hats, sneakers.
  - **Pre-rigged Cycles**: Walking, running, crouching, jumping, disco dance, shock reactions, and facepalms.

- 📦 **~35 Pure Hand-Crafted SVG Props (`props.js`)**:
  - Treasure chests (animated opening lids), gold coins, stinky shoes with toxic smoke clouds, wooden crates, barrels, tables, chairs, swords, shields, torches, magnifiers, banknotes, and evidence boards.

- 🏰 **100% Procedural SVG Backgrounds (`procedural-backgrounds`)**:
  - Medieval stone dungeons, warm timber interiors, cobblestone street alleys with glowing streetlamps, winter boutique store windows. **Zero image files required**.

- 🎥 **"Camera Kabhi Rukta Nahi" Continuous Motion Law (`gsap-motion`)**:
  - Unbroken cinematic camera drifts across every second of footage.
  - Causal punch-in zooms (1.35x to 1.75x) on shocking plot reveals.
  - Multiplane 2.5D parallax layering (`#layer-bg`, `#layer-mid`, `#layer-actors`).

- 🎙️ **Automated Audio Engineering (`video-sound`)**:
  - Broadcast-standard auto-ducking (-14 LUFS).
  - Word-level subtitle karaoke highlighting (`#FFD700`).

- ⚡ **Headless Virtual Clock Capture (`render-video`)**:
  - Deterministic frame capture via Playwright `window.seekToTime(t)` and FFmpeg assembly. Zero dropped frames or audio desync.

---

## 📂 Repository Architecture

```text
free_stick_man_video_skill/
├── .agents/skills/              # 22+ Core Video Production & Motion Skills
├── skills/                      # Top-level skills alias for all agents
├── projects/
│   ├── video_20s_dialogue/      # Working 20s Dialogue Film (Gary & Thief)
│   ├── comicron_60s_full/       # 65s Full 8-Scene Procedural Film
│   └── mystery_333am/           # Dance & Mystery 3:33 AM Project
├── growkaz_agent_bundle.zip     # Master Standalone Bundle with 59 skills
├── AGENTS.md                    # Universal Agent Instructions & Doctrines
├── GEMINI.md                    # Workspace Creative Law
├── build_complete_skills_bundle.py
└── README.md
```

---

## 🛠️ Complete Skill Registry

### 1. Core 2D Stickman & Video Production Skills
| Skill | Directory | Purpose |
|---|---|---|
| `character-animation` | `.agents/skills/character-animation/` | FK stickman rig, 5 head shapes, props, visemes, cycles |
| `procedural-backgrounds` | `.agents/skills/procedural-backgrounds/` | 100% SVG code-only sets and architectural environments |
| `gsap-motion` | `.agents/skills/gsap-motion/` | "Camera Kabhi Rukta Nahi" continuous camera motion & zooms |
| `make-2d-video` | `.agents/skills/make-2d-video/` | Production pipeline orchestrator & scene composer |
| `new-video` | `.agents/skills/new-video/` | Scaffolding, 3-second beat breakdown, script-to-storyboard |
| `video-styles` | `.agents/skills/video-styles/` | Aesthetic look lock, locked 7px stickman stroke, 4 palettes |
| `video-sound` | `.agents/skills/video-sound/` | VO synthesis, whoosh/impact SFX, auto-ducking (-14 LUFS) |
| `render-video` | `.agents/skills/render-video/` | Deterministic virtual clock rendering & 5-gate QC |
| `captions-overlay` | `.agents/skills/captions-overlay/` | Word-level karaoke captions, gold highlight, safe zones |

### 2. Cinematic Seam & Motion Skills
| Skill | Directory | Purpose |
|---|---|---|
| `motion-doctrine` | `.agents/skills/motion-doctrine/` | Vector law, carrier elements, causal motion |
| `cut-the-curve` | `.agents/skills/cut-the-curve/` | 5 velocity-matched transitions (zoom-through, waterfall) |
| `seam-craft` | `.agents/skills/seam-craft/` | White-flash guard, timeline stage-ground compositing |
| `oversized-cursor` | `.agents/skills/oversized-cursor/` | Eye-carrier cursor, off-screen entry, click triggers |

### 3. Extended Production Skills
- `faceless-shorts` — Nafay3D 21-hook formula, neon split-screen layouts for 9:16 vertical shorts.
- `ai-video-editor` — Automated silence removal, jumpcut punch-ins, B-roll overlays.
- `threejs-scenes` — 3D stylized sets (Mystery Noir, Tech Vault) composited with 2D actors.
- `ui-ux-pro-max` — UI evidence cards, HUD overlays, charts, and typography intelligence.
- `remotion-video` & `hyperframes` — Programmatic frame rendering and verification.

---

## 🏃 Quick Start: How to Use With Any AI Agent

1. **Clone this repository**:
   ```bash
   git clone https://github.com/i-amraj/free_stick_man_video_skill.git
   cd free_stick_man_video_skill
   ```
2. **Open in your favorite AI IDE** (Antigravity, Cursor, Windsurf, Claude Code, or Roo Code).
3. The agent will automatically detect and load `AGENTS.md` and all skills in `.agents/skills/`.
4. **Prompt your agent**:
   ```text
   Read AGENTS.md and use character-animation and make-2d-video to generate a 20-second stickman video with Detective Gary and a mysterious thief based on my script.
   ```

---

## 📜 License
MIT License. Free to use for personal and commercial video production.

