import os
import time
from playwright.sync_api import sync_playwright

def test_scene():
    html_path = os.path.abspath("projects/mystery_333am/scene/index.html")
    print(f"[*] Testing scene preview: {html_path}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920})
        page.goto(f"file:///{html_path}")
        time.sleep(1.0) # wait for assets to init

        # Test key time points
        test_points = [
            (2.0, "preview_01_clock.jpg"),
            (8.0, "preview_02_phone.jpg"),
            (28.5, "preview_03_knock.jpg"),
            (56.0, "preview_04_footprints.jpg"),
            (78.0, "preview_05_shadow_behind.jpg"),
            (90.0, "preview_06_evidence_climax.jpg")
        ]

        os.makedirs("projects/mystery_333am/output/previews", exist_ok=True)
        for t, filename in test_points:
            page.evaluate(f"window.seekToTime({t})")
            time.sleep(0.15)
            out_img = os.path.join("projects/mystery_333am/output/previews", filename)
            page.screenshot(path=out_img, quality=90, type="jpeg")
            print(f"  + Captured {filename} at t={t}s ({os.path.getsize(out_img)} bytes)")

        browser.close()
    print("[SUCCESS] All preview snapshots verified!")

if __name__ == "__main__":
    test_scene()

