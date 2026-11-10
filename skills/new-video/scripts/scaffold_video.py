"""
Video Project Scaffolder — new-video
Initializes complete project directories, storyboard.md, and project.json
"""

import os
import sys
import argparse
import json

def scaffold_project(title, output_dir=".", video_type="short", aspect="9:16"):
    print(f"[*] Initializing New Video Project: '{title}'")
    
    # Subdirectories
    dirs = ["audio", "sfx", "scenes", "output"]
    for d in dirs:
        p = os.path.join(output_dir, d)
        os.makedirs(p, exist_ok=True)
        print(f"  + Created: {d}/")

    # project.json
    project_meta = {
        "title": title,
        "type": video_type,
        "aspect_ratio": aspect,
        "resolution": [1080, 1920] if aspect == "9:16" else [1920, 1080],
        "fps": 30,
        "style": "growkaz_mystery"
    }
    with open(os.path.join(output_dir, "project.json"), "w", encoding="utf-8") as f:
        json.dump(project_meta, f, indent=2)
    print("  + Generated: project.json")

    # storyboard.md
    storyboard_text = f"""# Storyboard: {title}
- **Format**: {aspect} @ 30fps
- **Style Profile**: `growkaz_mystery`

---

### Scene 1 (0.0s – 3.0s) — Hook
- **Voiceover**: "[Hook voiceover sentence]"
- **Camera**: Push-in (`scale: 1.0 -> 1.12`)
- **Stickman Pose**: `idle_neutral` -> `shocked`
- **SFX**: `whoosh_entry.mp3`
"""
    with open(os.path.join(output_dir, "storyboard.md"), "w", encoding="utf-8") as f:
        f.write(storyboard_text)
    print("  + Generated: storyboard.md")

    print("[*] Video project scaffolded successfully!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default="Untitled Video", help="Title of the video")
    parser.add_argument("--dir", default=".", help="Target directory")
    parser.add_argument("--type", default="short", choices=["short", "longform"])
    parser.add_argument("--format", default="9:16", choices=["9:16", "16:9"])
    args = parser.parse_args()

    scaffold_project(args.title, args.dir, args.type, args.format)

