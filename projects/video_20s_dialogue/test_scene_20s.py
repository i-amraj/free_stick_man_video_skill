import asyncio
import os
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

PROJ = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\video_20s_dialogue")
HTML = PROJ / "scene_20s.html"
OUT_DIR = PROJ / "test_snaps"
OUT_DIR.mkdir(exist_ok=True)

async def test_snaps():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.goto(f"file:///{HTML.as_posix()}", wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(1000)
        
        # Test 4 key timestamps
        # 1. t=2.5s: Gary walking in
        # 2. t=7.5s: Gary pointing and speaking dialogue 1
        # 3. t=13.0s: Stinky shoe popped up, Gary in shock dialogue 2
        # 4. t=17.5s: Thief dancing disco, Gary facepalm
        timestamps = [2.5, 7.5, 13.0, 17.5]
        snaps = []
        for t in timestamps:
            await page.evaluate(f"window.seekToTime({t}); void 0;")
            await page.wait_for_timeout(40)
            p = OUT_DIR / f"snap_{t:.1f}s.png"
            await page.screenshot(path=str(p))
            print(f"Captured {p}")
            snaps.append(p)
            
        await browser.close()
        
    # Build 2x2 contact sheet
    images = [Image.open(s).resize((540, 960), Image.Resampling.LANCZOS) for s in snaps]
    grid = Image.new("RGB", (1080, 1920), (7, 9, 19))
    grid.paste(images[0], (0, 0))
    grid.paste(images[1], (540, 0))
    grid.paste(images[2], (0, 960))
    grid.paste(images[3], (540, 960))
    
    grid_out = PROJ / "scene_20s_contact_sheet.jpg"
    grid.save(grid_out, quality=90)
    print("Saved contact sheet:", grid_out)
    
    # Copy to artifacts
    artifacts_dir = Path(r"C:\Users\iamra\.gemini\antigravity\brain\c9b9d424-5a3c-4adf-aabc-2078a51c8ad6")
    grid.save(artifacts_dir / "scene_20s_contact_sheet.jpg", quality=90)

if __name__ == "__main__":
    asyncio.run(test_snaps())
