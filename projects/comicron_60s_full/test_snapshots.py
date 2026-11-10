import asyncio
import os
from playwright.async_api import async_playwright

async def capture_snapshots():
    os.makedirs('projects/comicron_60s_full/test_snapshots', exist_ok=True)
    
    test_times = [
        (2.0, "scene1_thief"),
        (6.5, "scene2_guards_laughing"),
        (11.5, "scene3_corvin_sign"),
        (19.5, "scene4_stakeout"),
        (27.0, "scene5_hopping_kids"),
        (30.5, "scene6_winter_despair"),
        (37.0, "scene7_stranger_coins"),
        (52.0, "scene8_grand_boutique")
    ]
    
    html_path = os.path.abspath('projects/comicron_60s_full/scene.html').replace('\\', '/')
    url = f"file:///{html_path}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.goto(url)
        await page.wait_for_timeout(1000)
        
        for t, name in test_times:
            await page.evaluate(f"window.seekToTime({t})")
            await page.wait_for_timeout(100)
            out_file = f"projects/comicron_60s_full/test_snapshots/{name}_{t:.1f}s.jpg"
            await page.screenshot(path=out_file, type="jpeg", quality=90)
            print(f"Captured {out_file}")
            
        await browser.close()
    print("All snapshots captured!")

if __name__ == "__main__":
    asyncio.run(capture_snapshots())

