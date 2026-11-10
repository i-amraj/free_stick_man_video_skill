import os
import time
from playwright.sync_api import sync_playwright
from PIL import Image

videos = [
    {
        'id': '8eeoDztahuM',
        'url': 'https://www.youtube.com/shorts/8eeoDztahuM',
        'name': 'thief_shoes'
    },
    {
        'id': 'V5qnOWYIL7Y',
        'url': 'https://www.youtube.com/shorts/V5qnOWYIL7Y',
        'name': 'guard_vault'
    },
    {
        'id': 'N_R7ZHTDNVo',
        'url': 'https://www.youtube.com/shorts/N_R7ZHTDNVo',
        'name': 'king_pyramid'
    }
]

timestamps = [0.5, 3.0, 6.0, 9.0, 12.0, 15.0, 18.0, 22.0, 26.0, 30.0, 35.0, 40.0, 45.0, 50.0, 55.0, 60.0]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for v_info in videos:
        vid = v_info['id']
        url = v_info['url']
        out_dir = f"projects/channel_analysis/frames/{vid}"
        os.makedirs(out_dir, exist_ok=True)
        print(f"\n==========================================")
        print(f"Extracting frames for {vid} ({v_info['name']})...")
        
        page = browser.new_page(viewport={'width': 1080, 'height': 1920})
        page.goto(url, wait_until='networkidle')
        time.sleep(2)
        
        # Pause video and hide YouTube UI controls
        page.evaluate('''() => {
            const v = document.querySelector('video');
            if (v) v.pause();
            // Hide YouTube UI controls
            const selectors = [
                '#actions',
                '#overlay',
                'ytd-reel-player-header-renderer',
                '.ytp-chrome-bottom',
                '.ytp-gradient-bottom',
                '.ytp-gradient-top',
                'ytd-shorts-player-controls',
                '#like-button',
                '#dislike-button',
                '#comments-button'
            ];
            selectors.forEach(s => {
                document.querySelectorAll(s).forEach(el => el.style.display = 'none');
            });
        }''')
        
        duration = page.evaluate("() => document.querySelector('video') ? document.querySelector('video').duration : 60")
        print(f"Detected video duration: {duration:.1f}s")
        
        video_elem = page.locator('video').first
        
        valid_ts = [t for t in timestamps if t < duration - 1.0]
        
        for t in valid_ts:
            page.evaluate(f"() => {{ const v = document.querySelector('video'); if (v) v.currentTime = {t}; }}")
            time.sleep(0.4) # let frame render
            frame_path = f"{out_dir}/frame_{t:04.1f}s.jpg"
            video_elem.screenshot(path=frame_path)
            print(f"  Captured frame at {t:04.1f}s -> {frame_path}")
            
        page.close()
        
    browser.close()

print("\nAll frames successfully extracted!")

