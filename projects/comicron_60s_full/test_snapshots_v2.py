import asyncio
import os
from playwright.async_api import async_playwright

async def capture_snapshots():
    os.makedirs('projects/comicron_60s_full/test_snapshots_v2', exist_ok=True)
    
    test_times = [
        (2.0, "scene1_thief"),
        (6.5, "scene2_guards_wanted_poster"),
        (11.5, "scene3_corvin_tally_slate"),
        (20.0, "scene4_stakeout_guards_zzz"),
        (27.0, "scene5_hopping_kids_hopscotch"),
        (30.5, "scene6_corvin_empty_pockets"),
        (37.0, "scene7_firewood_deal"),
        (52.5, "scene8_secret_formula_card"),
        (59.5, "scene8_wealth_deposit_card")
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
            out_file = f"projects/comicron_60s_full/test_snapshots_v2/{name}_{t:.1f}s.jpg"
            await page.screenshot(path=out_file, type="jpeg", quality=90)
            print(f"Captured {out_file}")
            
        await browser.close()
    print("All enhanced snapshots captured!")

if __name__ == "__main__":
    asyncio.run(capture_snapshots())

