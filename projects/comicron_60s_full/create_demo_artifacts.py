import os
from PIL import Image
from pathlib import Path

PROJECT = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\comicron_60s_full")
FRAMES = PROJECT / "frames_demo10"
ARTIFACTS = Path(r"C:\Users\iamra\.gemini\antigravity\brain\c9b9d424-5a3c-4adf-aabc-2078a51c8ad6")

# Sample frames:
# 1. t=1.0s (frame 30) - Thief descending rope
# 2. t=3.5s (frame 105) - Thief snatching the left shoe off workbench
# 3. t=6.5s (frame 195) - Guards laughing with open mouths, tears, wanted poster
# 4. t=9.2s (frame 276) - Old Corvin with 300 Right / 0 Left slate + Question mark

indices = [30, 105, 195, 276]
times = [1.0, 3.5, 6.5, 9.2]
labels = ["1.0s: Thief Rope Descent", "3.5s: Snatched Left Shoe", "6.5s: Laughing Guards & Wanted Poster", "9.2s: Old Corvin Chalk Tally Slate"]

images = []
for idx in indices:
    fpath = FRAMES / f"frame_{idx:05d}.png"
    im = Image.open(fpath)
    # Resize for contact sheet (width: 540, height: 960)
    im_small = im.resize((540, 960), Image.Resampling.LANCZOS)
    images.append(im_small)

# Create 2x2 grid (1080 x 1920)
grid = Image.new("RGB", (1080, 1920), (10, 15, 25))
grid.paste(images[0], (0, 0))
grid.paste(images[1], (540, 0))
grid.paste(images[2], (0, 960))
grid.paste(images[3], (540, 960))

out_grid = ARTIFACTS / "demo_10s_character_contact_sheet.jpg"
grid.save(out_grid, quality=90)
print(f"Contact sheet saved to {out_grid}")

# Also copy single snapshot of Scene 1 and Scene 2
Image.open(FRAMES / f"frame_{105:05d}.png").save(ARTIFACTS / "demo_10s_scene1_thief_3.5s.jpg", quality=90)
Image.open(FRAMES / f"frame_{195:05d}.png").save(ARTIFACTS / "demo_10s_scene2_guards_6.5s.jpg", quality=90)
Image.open(FRAMES / f"frame_{276:05d}.png").save(ARTIFACTS / "demo_10s_scene2_corvin_9.2s.jpg", quality=90)

# Copy video to artifacts directory as well
import shutil
shutil.copy2(PROJECT / "demo_10s_character_master.mp4", ARTIFACTS / "demo_10s_character_master.mp4")
print("Artifacts generated successfully!")

