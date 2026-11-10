import asyncio
from playwright.async_api import async_playwright
import os

async def capture_snapshots():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, "demo_character_bones_10s.html")
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    out_dir = os.path.join(script_dir, "snapshots_bones")
    os.makedirs(out_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 540, "height": 960})
        await page.goto(file_url)
        await page.wait_for_timeout(500)
        
        # Test time points: 1.0s (walking in), 2.5s (idle standing), 4.2s (talking/waving), 6.0s (shocked/hands on head), 8.5s (walking out)
        timestamps = [1.0, 2.5, 4.2, 6.0, 8.5]
        for t in timestamps:
            await page.evaluate(f"masterTimeline.seek({t});")
            snap_path = os.path.join(out_dir, f"snap_{t:.1f}s.png")
            await page.screenshot(path=snap_path)
            print(f"Captured {snap_path}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_snapshots())

