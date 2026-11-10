"""
3D Human Character Dance Capture & Multi-Angle Verification Script
"""
from playwright.sync_api import sync_playwright
import os, time, shutil
from PIL import Image

base_dir = os.path.abspath("projects/mystery_333am")
html_file = os.path.join(base_dir, "realistic_3d_dance_party.html")
out_dir = os.path.join(base_dir, "output", "previews")
artifact_dir = "C:/Users/iamra/.gemini/antigravity/brain/c9b9d424-5a3c-4adf-aabc-2078a51c8ad6"
contact_sheet = os.path.join(base_dir, "output", "real_3d_dance_contact_sheet.jpg")

os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--allow-file-access-from-files", "--disable-web-security"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 768})
    page.goto(f"file:///{html_file}")
    
    print("[*] Waiting for 3D model and 99 bones to load...")
    page.wait_for_function("window.danceReady === true", timeout=25000)
    print("[*] 3D Model ready! Testing dance moves...")

    # 1. Hip-Hop Drop
    time.sleep(1.8)
    p1 = os.path.join(out_dir, "real_3d_dance_01_hiphop.jpg")
    page.screenshot(path=p1, quality=92)
    print("[OK] Captured Hip-Hop Drop")

    # 2. Chest Pop (Beat 2)
    page.evaluate("switchDance('hiphop')")
    time.sleep(0.5)
    p2 = os.path.join(out_dir, "real_3d_dance_02_chestpop.jpg")
    page.screenshot(path=p2, quality=92)
    print("[OK] Captured Center Chest Pop & Fingers Spread")

    # 3. Saturday Disco (Travolta Point)
    page.evaluate("switchDance('disco')")
    time.sleep(0.9)
    p3 = os.path.join(out_dir, "real_3d_dance_03_disco.jpg")
    page.screenshot(path=p3, quality=92)
    print("[OK] Captured Saturday Disco High Point")

    # 4. Liquid 3D Wave
    page.evaluate("switchDance('wave')")
    time.sleep(1.2)
    p4 = os.path.join(out_dir, "real_3d_dance_04_wave.jpg")
    page.screenshot(path=p4, quality=92)
    print("[OK] Captured Liquid 3D Wave")

    browser.close()

# Copy to artifacts directory
for f in ["real_3d_dance_01_hiphop.jpg", "real_3d_dance_02_chestpop.jpg", "real_3d_dance_03_disco.jpg", "real_3d_dance_04_wave.jpg"]:
    src = os.path.join(out_dir, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(artifact_dir, f))

# Build 4-up Contact Sheet
thumbs = [p1, p2, p3, p4]
thumb_w, thumb_h = 320, 192
sheet = Image.new("RGB", (thumb_w * 2, thumb_h * 2), (4, 7, 20))
for idx, tpath in enumerate(thumbs):
    if os.path.exists(tpath):
        img = Image.open(tpath).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = (idx % 2) * thumb_w
        y = (idx // 2) * thumb_h
        sheet.paste(img, (x, y))

sheet.save(contact_sheet, quality=92)
if os.path.exists(artifact_dir):
    shutil.copy2(contact_sheet, os.path.join(artifact_dir, "real_3d_dance_contact_sheet.jpg"))

print("[SUCCESS] All 3D Human Dance Snapshots & Contact Sheet Generated!")

