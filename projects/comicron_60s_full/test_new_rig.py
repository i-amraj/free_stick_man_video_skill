import asyncio
from playwright.async_api import async_playwright
import os
from PIL import Image

async def capture_demo_snapshots():
    proj = r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\comicron_60s_full"
    html_path = os.path.join(proj, "demo.html")
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    out_dir = os.path.join(proj, "snapshots_new_rig")
    os.makedirs(out_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-gpu"])
        page = await browser.new_page(viewport={"width": 540, "height": 960})
        await page.goto(file_url, wait_until="domcontentloaded", timeout=15000)
        await page.wait_for_timeout(1000)
        
        # Capture frames at key beats:
        # t=1.5s (hero walking in)
        # t=3.5s (hero waving and talking to pal)
        # t=6.5s (hero sitting on chair with chest & coins)
        # t=9.5s (party & disco dancing!)
        timestamps = [1.5, 3.5, 6.5, 9.5]
        snaps = []
        for t in timestamps:
            await page.evaluate(f"window.__tl.seek({t}); void 0;")
            await page.wait_for_timeout(30)
            snap_path = os.path.join(out_dir, f"snap_{t:.1f}s.png")
            await page.screenshot(path=snap_path)
            print(f"Captured {snap_path}")
            snaps.append(snap_path)
            
        await browser.close()
        
    # Build 2x2 grid
    images = [Image.open(s) for s in snaps]
    grid = Image.new("RGB", (1080, 1920), (11, 16, 32))
    grid.paste(images[0], (0, 0))
    grid.paste(images[1], (540, 0))
    grid.paste(images[2], (0, 960))
    grid.paste(images[3], (540, 960))
    
    grid_out = os.path.join(proj, "new_rig_contact_sheet.jpg")
    grid.save(grid_out, quality=90)
    print("Saved grid contact sheet:", grid_out)
    
    # Copy to artifacts
    artifacts_dir = r"C:\Users\iamra\.gemini\antigravity\brain\c9b9d424-5a3c-4adf-aabc-2078a51c8ad6"
    grid.save(os.path.join(artifacts_dir, "new_rig_contact_sheet.jpg"), quality=90)

if __name__ == "__main__":
    asyncio.run(capture_demo_snapshots())
