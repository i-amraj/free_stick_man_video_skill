"""
step4_motion_engine.py
GSAP Motion Choreography & HTML Generation:
- "Camera Kabhi Rukta Nahi" unbroken camera drift (0.0s to end)
- Multiplane parallax camera coordinates
- Character pose choreography & lip-sync triggers
- Kinetic karaoke subtitle overlay
- Emits production-ready scene.html
"""

import json
from pathlib import Path
from typing import List, Dict, Any
from .step3_stage_composer import generate_procedural_background_svg, get_character_setup_js

def build_scene_html(
    beats: List[Dict[str, Any]],
    word_timings: List[Dict[str, Any]],
    characters: List[Dict[str, Any]],
    total_duration: float,
    rig_js_path: str,
    props_js_path: str,
    gsap_js_path: str,
    output_html_path: Path
) -> None:
    bg_svg = generate_procedural_background_svg("medieval_alley")
    char_setup = get_character_setup_js(characters)
    
    # Read core libraries
    with open(rig_js_path, "r", encoding="utf-8") as f:
        rig_code = f.read()
    with open(props_js_path, "r", encoding="utf-8") as f:
        props_code = f.read()
    with open(gsap_js_path, "r", encoding="utf-8") as f:
        gsap_code = f.read()
        
    words_json_str = json.dumps(word_timings)
    beats_json_str = json.dumps(beats)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>GrowKaz Stickman Scene</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body, html {{
        width: 1080px; height: 1920px;
        background: #000;
        overflow: hidden;
        font-family: 'Montserrat', sans-serif;
    }}
    #stage {{
        position: relative;
        width: 1080px; height: 1920px;
        transform-origin: 540px 1460px;
    }}
    #layer-bg {{
        position: absolute; top: 0; left: 0; width: 1080px; height: 1920px;
        transform-origin: 540px 1460px;
    }}
    #layer-actors {{
        position: absolute; top: 0; left: 0; width: 1080px; height: 1920px;
        transform-origin: 540px 1460px;
    }}
    #layer-subtitles {{
        position: absolute;
        bottom: 240px; left: 60px; width: 960px;
        text-align: center;
        pointer-events: none;
        z-index: 999;
    }}
    .sub-chunk {{
        display: inline-block;
        font-size: 52px; font-weight: 900;
        text-transform: uppercase;
        color: #FFFFFF;
        text-shadow: 0 4px 16px rgba(0,0,0,0.9), 0 2px 4px #000;
        line-height: 1.3;
    }}
    .sub-word {{
        display: inline-block;
        margin: 0 8px;
        transition: transform 0.08s ease, color 0.08s ease;
    }}
    .sub-word.active {{
        color: #FFD700;
        transform: scale(1.18);
        text-shadow: 0 0 24px rgba(255,215,0,0.8), 0 4px 12px #000;
    }}
</style>
</head>
<body>
<div id="stage">
    <svg id="layer-bg" viewBox="0 0 1080 1920">
        {bg_svg}
    </svg>
    
    <svg id="layer-actors" viewBox="0 0 1080 1920">
        <g id="props-container"></g>
        {"".join([f'<g id="{c["id"]}-container"></g>' for c in characters])}
    </svg>
    
    <div id="layer-subtitles">
        <div id="subtitle-box" class="sub-chunk"></div>
    </div>
</div>

<script>
{gsap_code}
</script>
<script>
{rig_code}
</script>
<script>
{props_code}
</script>

<script>
const TOTAL_DURATION = {total_duration};
const WORD_TIMINGS = {words_json_str};
const BEATS = {beats_json_str};

// 1. Initialize Characters
{char_setup}

// 2. Props Kit
const propsKit = new StickmanProps();
const propsSvg = document.getElementById('props-container');
propsSvg.innerHTML = `
    ${{propsKit.renderChest({{ id: 'chest', x: 540, y: 1440, isOpen: false, scale: 2.2 }})}}
    ${{propsKit.renderShoe({{ id: 'shoe', x: 540, y: 1450, isStinky: true, scale: 2.2 }})}}
`;

// 3. Camera Kabhi Rukta Nahi - Master Timeline
window.__tl = gsap.timeline({{ paused: true }});
const stage = document.getElementById('stage');
const bgLayer = document.getElementById('layer-bg');

// Continuous unbroken camera movement from 0 to TOTAL_DURATION
window.__tl.to(stage, {{
    scale: 1.42,
    x: -30,
    y: -40,
    duration: TOTAL_DURATION * 0.45,
    ease: "power1.inOut"
}}, 0);

window.__tl.to(stage, {{
    scale: 1.70, // Causal punch-in zoom on revelation
    x: 40,
    y: -80,
    duration: TOTAL_DURATION * 0.25,
    ease: "power2.out"
}}, TOTAL_DURATION * 0.45);

window.__tl.to(stage, {{
    scale: 1.48,
    x: 0,
    y: -30,
    duration: TOTAL_DURATION * 0.30,
    ease: "power1.inOut"
}}, TOTAL_DURATION * 0.70);

// Multiplane 2.5D background parallax
window.__tl.to(bgLayer, {{
    x: 18,
    y: 12,
    duration: TOTAL_DURATION,
    ease: "none"
}}, 0);

// 4. Character Action Tweens
const hero = window['hero'] || window['gary'];
if (hero) {{
    hero.pose('search');
    // Talking during speech segments
    BEATS.forEach(b => {{
        if (b.is_direct_speech) {{
            window.__tl.call(() => hero.talk(true), null, b.time_start);
            window.__tl.call(() => hero.talk(false), null, b.time_end);
        }}
    }});
}}

// 5. Deterministic Virtual Clock API
window.seekToTime = function(t) {{
    window.__tl.seek(t);
    
    // Subtitle word active check
    const subBox = document.getElementById('subtitle-box');
    const activeWord = WORD_TIMINGS.find(w => t >= w.start && t <= w.end);
    
    // Find current sentence chunk
    const currentWords = WORD_TIMINGS.filter(w => t >= w.start - 1.2 && t <= w.end + 1.2);
    if (currentWords.length > 0) {{
        let html = '';
        currentWords.slice(0, 6).forEach(w => {{
            const isActive = activeWord && activeWord.start === w.start;
            html += `<span class="sub-word ${{isActive ? 'active' : ''}}">${{w.word}}</span>`;
        }});
        subBox.innerHTML = html;
    }} else {{
        subBox.innerHTML = '';
    }}
}};
</script>
</body>
</html>
"""
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

