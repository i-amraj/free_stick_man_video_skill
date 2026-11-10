---
name: new-video
description: >-
  Project scaffolding and kick-off workflow for new video production ("nayi video ki shuruaat").
  Use this skill whenever starting a new video project, creating storyboards, structuring 3-second scene beats,
  generating voiceover scripts with word-level timing, setting up project directory trees,
  or preparing the scene asset manifest.
---

# New Video Scaffolding & Kickoff (`new-video`)

Every great video begins with strong architectural foundations. `new-video` automates project scaffolding, storyboard planning, script beat breakdowns, and asset checklists.

---

## 1. Quickstart Scaffolding Command

To initialize a new video in your workspace:
```bash
python scripts/scaffold_video.py --title "The Secret Algorithm Behind TikTok" --type short --format 9:16
```

This creates the standard project tree:
```text
my_video_project/
├── project.json              # Video metadata, aspect ratio, fps, audio config
├── script.md                 # Word-for-word voiceover narration with beat markers
├── storyboard.md             # 3-second scene breakdown with character poses & camera
├── audio/
│   ├── voiceover.mp3         # Master narration audio
│   └── music.mp3             # Background track
├── sfx/                      # Sound effect cues (whooshes, pops, impacts)
├── scenes/
│   ├── scene_01.html         # Scene 1: The Hook (0.0s – 3.2s)
│   ├── scene_02.html         # Scene 2: The Agitation (3.2s – 7.0s)
│   └── ...                   # Subsequent scene files
└── output/                   # Rendered MP4s and contact sheets
```

---

## 2. The 4-Phase Short Video Structure

| Phase | Time Window | Goal | Retention Rule |
|-------|-------------|------|----------------|
| **1. The Hook** | 0.0s – 2.8s | Stop the scroll immediately | High-contrast visual + shocking claim or mystery premise |
| **2. The Stakes** | 2.8s – 8.0s | Explain WHY this matters | Show stickman facing dilemma, danger, or mystery clue |
| **3. The Evidence** | 8.0s – 45.0s | Deliver fast, punchy revelations | New visual change / camera drift every 2.5 seconds |
| **4. The Climax / Loop** | 45.0s – 60.0s | Final payoff + seamless loop | Last sentence connects directly back to the first hook line |

---

## 3. Storyboard Template (`storyboard.md`)

```markdown
# Storyboard: [Video Title]
- **Target Duration**: 45 seconds (15 scenes)
- **Format**: Vertical 1080x1920 (9:16) @ 30fps
- **Style Profile**: `growkaz_mystery`

---

### Scene 1 (0.0s – 2.8s) — The Mystery Hook
- **Voiceover**: "In 2014, a secret vault was found under the desert..."
- **Camera**: Fast push-in from wide (`scale: 1.0 -> 1.15`)
- **Stickman Pose**: `shocked` (hands on head, mouth wide)
- **Environment**: 3D Mystery Room with single spotlight pointing to locked door
- **SFX**: `sfx/sub_boom.mp3` on word "secret"

### Scene 2 (2.8s – 6.5s) — The Evidence Card
- **Voiceover**: "Nobody was allowed inside, except for three men."
- **Camera**: Continuous lateral pan to left (`x: 0 -> -40px`)
- **Stickman Pose**: `pointing_up` (pointing at glowing evidence card)
- **Prop**: 3 silhouette mugshots on frosted glass card
- **SFX**: `sfx/whoosh.mp3` transition + `sfx/pop.mp3` on card reveal
```

---

## 4. Production Checklist (Before Coding Scenes)

- [ ] Script finalized and approved for flow and loopability.
- [ ] Voiceover rendered and word timestamps generated.
- [ ] Storyboard scene cuts matched to natural pauses in voiceover.
- [ ] Master style profile locked in `video-styles`.

