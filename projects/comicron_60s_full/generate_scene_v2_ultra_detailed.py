"""
generate_scene_v2_ultra_detailed.py
Builds the ultra-detailed 100% script-matched scene.html with:
- 100% Procedural SVG backgrounds (zero image files)
- Welded character joints & anatomy (no detached heads or limbs)
- Script-to-screen fidelity:
  - Wanted One-Legged Thief poster (Scene 2)
  - Tally board '300 RIGHT SHOES' + Question Marks (Scene 3)
  - 5 hiding guards + Zzz sleeping bubbles (Scene 4)
  - True one-legged hopping kids + chalk hopscotch (Scene 5)
  - Corvin's empty pockets pulled out + freezing breath (Scene 6)
  - 'FOR FIREWOOD' crate + tears of relief (Scene 7)
  - Infographic cards [0$ + 0$ = 100$] & [5 coins -> 300 pairs -> 30,000 gold] (Scene 8)
- Exact Montserrat 900 gold karaoke subtitles
"""
import json
from pathlib import Path

PROJECT = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\comicron_60s_full")
chunks = json.load(open(PROJECT / "subtitle_chunks.json", encoding="utf-8"))

import sys
sys.path.append(str(PROJECT))
import build_procedural_components as bpc

html_code = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
<title>Comicron 60s - 100% Script-Faithful Procedural Film</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
  body {{
    background: #000;
    width: 1080px; height: 1920px;
    overflow: hidden;
    display: flex; justify-content: center; align-items: center;
  }}
  #viewport {{
    width: 1080px; height: 1920px;
    position: relative; overflow: hidden;
    background: #0d0a06;
  }}
  .scene {{
    position: absolute; top: 0; left: 0;
    width: 1080px; height: 1920px;
    display: none !important; opacity: 0;
    transform-origin: center center;
  }}
  .scene.active {{
    display: block !important; opacity: 1 !important;
  }}
  .camera-rig {{
    width: 100%; height: 100%;
    position: absolute; top: 0; left: 0;
    transform-origin: 540px 960px;
  }}
  svg.bg-procedural {{
    position: absolute; top: 0; left: 0;
    width: 1080px; height: 1920px;
    pointer-events: none; z-index: 10;
  }}
  .vignette-overlay {{
    position: absolute; top: 0; left: 0;
    width: 100%; height: 100%;
    background: radial-gradient(circle at 50% 50%, rgba(0,0,0,0) 68%, rgba(0,0,0,0.58) 100%);
    pointer-events: none; z-index: 80;
  }}
  .channel-badge {{
    position: absolute; top: 85px; left: 50%;
    transform: translateX(-50%);
    font-family: 'Montserrat', sans-serif;
    font-size: 24px; font-weight: 900;
    letter-spacing: 5px; color: rgba(255, 255, 255, 0.70);
    text-transform: uppercase; z-index: 90;
    text-shadow: 0 2px 8px rgba(0,0,0,0.85);
    white-space: nowrap;
  }}
  #caption-box {{
    position: absolute; bottom: 220px;
    left: 40px; right: 40px;
    z-index: 100; text-align: center;
    pointer-events: none;
  }}
  .caption-phrase {{
    font-family: 'Montserrat', sans-serif;
    font-size: 54px; font-weight: 900;
    color: #ffffff; text-transform: uppercase;
    letter-spacing: 1.5px; line-height: 1.25;
    text-shadow: 
      0 4px 14px rgba(0,0,0,0.95), 0 2px 4px #000,
      -2px -2px 0 #000,  2px -2px 0 #000,
      -2px  2px 0 #000,  2px  2px 0 #000;
    display: flex; flex-wrap: wrap;
    justify-content: center; align-items: center;
    gap: 8px 16px;
  }}
  .word-span {{
    display: inline-block; margin: 0 8px;
    transition: transform 0.08s ease, color 0.08s ease;
    white-space: nowrap;
  }}
  .word-span.active {{
    color: #FFD700; transform: scale(1.18);
    text-shadow: 
      0 0 25px rgba(255, 215, 0, 0.8),
      0 4px 14px rgba(0,0,0,0.95),
      -2px -2px 0 #000, 2px -2px 0 #000,
      -2px  2px 0 #000, 2px  2px 0 #000;
  }}
  svg.character-layer {{
    position: absolute; top: 0; left: 0;
    width: 1080px; height: 1920px;
    pointer-events: none; z-index: 70;
  }}
  .stroke-main {{ stroke: #121824; stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; }}
  .head-white {{ fill: #ffffff; stroke: #121824; stroke-width: 7; }}
  .guard-blue {{ fill: #2563eb; stroke: #121824; stroke-width: 7; }}
  .guard-dark {{ fill: #1d4ed8; stroke: #121824; stroke-width: 7; }}
  .gold-trim {{ fill: #facc15; stroke: #121824; stroke-width: 6; }}
  .corvin-apron {{ fill: #854d0e; stroke: #121824; stroke-width: 7; }}
  .corvin-shirt {{ fill: #cbd5e1; stroke: #121824; stroke-width: 7; }}
  .stranger-cloak {{ fill: #1e293b; stroke: #121824; stroke-width: 7; }}
  .stranger-scarf {{ fill: #15803d; stroke: #121824; stroke-width: 6; }}
  .boot-leather {{ fill: #78350f; stroke: #121824; stroke-width: 6; }}
  .shadow-ground {{ fill: rgba(10, 15, 25, 0.6); }}

  /* Infographic Cards in Climax */
  .info-card {{
    position: absolute; z-index: 75;
    background: rgba(15, 23, 42, 0.95);
    border: 5px solid #facc15;
    border-radius: 24px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.8), 0 0 30px rgba(250, 204, 21, 0.3);
    padding: 24px 32px;
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    opacity: 0; transform: scale(0.85);
    pointer-events: none;
  }}
</style>
<script src="gsap.min.js"></script>
</head>
<body>

<div id="viewport">
  <div class="channel-badge">COMICRON • THE LEFT SHOE MYSTERY</div>
  <div class="vignette-overlay"></div>

  <!-- ================= SCENE 1: THE NIGHT THIEF (0.0s -> 5.25s) ================= -->
  <div id="scene1" class="scene active">
    <div id="camera1" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_workshop_defs}
        {bpc.bg_workshop_content}
        <!-- Shelf with dashed red stolen shoe outlines -->
        <g transform="translate(140, 640)">
          <path d="M 0 0 C 25 -15, 60 -10, 75 10 C 65 30, 25 28, -5 20 Z" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="6 4" opacity="0.8"/>
          <text x="35" y="32" font-family="'Montserrat', sans-serif" font-weight="900" font-size="12" fill="#ef4444" text-anchor="middle">STOLEN</text>
        </g>
      </svg>
      <svg class="character-layer" viewBox="0 0 1080 1920">
        <polygon points="380,0 700,0 800,1400 280,1400" fill="rgba(255, 255, 255, 0.11)" />
        <path id="thief-rope" d="M 540 0 L 540 760" stroke="#78553a" stroke-width="8" stroke-dasharray="14 6" />

        <g id="thief-dangler" transform="translate(540, 760)">
          <ellipse cx="0" cy="850" rx="90" ry="24" class="shadow-ground" opacity="0.6" />
          <circle cx="-16" cy="-20" r="14" class="stranger-cloak" />
          <circle cx="16" cy="-45" r="14" class="stranger-cloak" />

          <g id="thief-body-group">
            <path d="M -45 -10 C -55 80, -70 140, -60 170 C -20 185, 20 185, 60 170 C 70 140, 55 80, 45 -10 Z" class="stranger-cloak" />
            <path d="M -42 0 Q 0 15 42 0 Q 30 35 0 35 Q -30 35 -42 0 Z" class="stranger-scarf" />
            <path id="scarf-tail" d="M 15 28 Q 30 70 25 110" stroke="#15803d" stroke-width="12" stroke-linecap="round" fill="none" />

            <!-- Seamless welded head -->
            <g id="thief-head-group" transform="translate(0, -60)">
              <circle cx="0" cy="0" r="56" class="head-white" />
              <path d="M -42 -12 C -20 -24, 20 -24, 42 -12 C 45 4, 30 14, 0 10 C -30 14, -45 4, -42 -12 Z" fill="#0f172a" />
              <ellipse cx="-18" cy="-5" rx="7" ry="5" fill="#facc15" />
              <circle cx="-16" cy="-5" r="2.5" fill="#000" />
              <ellipse cx="18" cy="-5" rx="7" ry="5" fill="#facc15" />
              <circle cx="20" cy="-5" r="2.5" fill="#000" />
              <path d="M -12 25 Q 2 34 18 22" class="stroke-main" fill="none" />
            </g>

            <g id="thief-arm" transform="translate(-40, 60)">
              <path d="M 0 0 Q -45 70 -70 140" stroke="#1e293b" stroke-width="18" stroke-linecap="round" fill="none" />
              <circle cx="-70" cy="140" r="15" fill="#1e293b" />
              <g id="snatched-shoe" transform="translate(-85, 140) rotate(-25)">
                <path d="M 0 0 C 25 -15, 60 -10, 75 10 C 65 30, 25 28, -5 20 C -15 15, -15 8, 0 0 Z" class="boot-leather" />
                <line x1="-15" y1="10" x2="-35" y2="10" stroke="#facc15" stroke-width="3" stroke-linecap="round"/>
                <line x1="-15" y1="20" x2="-40" y2="20" stroke="#facc15" stroke-width="3" stroke-linecap="round"/>
              </g>
            </g>
          </g>
        </g>
      </svg>
    </div>
  </div>

  <!-- ================= SCENE 2: LAUGHING GUARDS (5.25s -> 8.2s) ================= -->
  <div id="scene2" class="scene">
    <div id="camera2" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_street_defs}
        {bpc.bg_street_content}
      </svg>
      <svg class="character-layer" viewBox="0 0 1080 1920">
        <ellipse cx="360" cy="1760" rx="130" ry="32" class="shadow-ground" />
        <ellipse cx="720" cy="1760" rx="130" ry="32" class="shadow-ground" />

        <!-- CHIEF GUARD with welded neck and laugh tears -->
        <g id="chief-guard-root" transform="translate(360, 1420)">
          <line x1="-35" y1="180" x2="-45" y2="335" class="stroke-main" />
          <line x1="35" y1="180" x2="45" y2="335" class="stroke-main" />
          <ellipse cx="-52" cy="335" rx="20" ry="9" fill="#121824" />
          <ellipse cx="52" cy="335" rx="20" ry="9" fill="#121824" />

          <g id="chief-body">
            <!-- Overlapping neck collar to prevent head gap -->
            <rect x="-30" y="-30" width="60" height="40" rx="10" class="guard-blue" />
            <rect x="-60" y="0" width="120" height="185" rx="55" class="guard-blue" />
            <line x1="-58" y1="95" x2="58" y2="95" stroke="#facc15" stroke-width="14" />
            <rect x="-16" y="86" width="32" height="18" rx="4" class="gold-trim" />
            <circle cx="-25" cy="45" r="9" class="gold-trim" />
            <circle cx="-25" cy="65" r="9" class="gold-trim" />

            <g id="chief-head-rig" transform="translate(0, -60)">
              <circle cx="0" cy="0" r="62" class="head-white" />
              <g id="chief-tophat" transform="translate(0, -52)">
                <ellipse cx="0" cy="0" rx="90" ry="16" class="guard-dark" />
                <rect x="-55" y="-120" width="110" height="120" rx="6" class="guard-blue" />
                <rect x="-55" y="-22" width="110" height="22" fill="#facc15" stroke="#121824" stroke-width="5" />
                <polygon points="-8,-120 8,-120 0,-140" class="gold-trim" />
              </g>

              <!-- Happy squint eyes -->
              <path d="M -34 -8 Q -22 -24 -10 -8" class="stroke-main" stroke-width="6" fill="none" />
              <path d="M 10 -8 Q 22 -24 34 -8" class="stroke-main" stroke-width="6" fill="none" />
              <!-- Laugh tears streaming -->
              <path d="M -38 2 Q -50 20 -40 35" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" fill="none" />
              <path d="M 38 2 Q 50 20 40 35" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" fill="none" />

              <g id="chief-mouth" transform="translate(0, 16)">
                <path d="M -28 0 Q 0 48 28 0 Z" fill="#7f1d1d" stroke="#121824" stroke-width="5" />
                <path d="M -14 20 Q 0 10 14 20 Q 0 38 -14 20 Z" fill="#ef4444" />
                <path d="M -20 0 L 20 0 L 15 8 L -15 8 Z" fill="#ffffff" />
              </g>
            </g>

            <path id="chief-arm-left" d="M -55 35 Q -95 90 -30 115" class="stroke-main" stroke-width="16" fill="none" />
            <path id="chief-arm-right" d="M 55 35 Q 95 90 30 115" class="stroke-main" stroke-width="16" fill="none" />
          </g>
        </g>

        <!-- DEPUTY GUARD -->
        <g id="deputy-guard-root" transform="translate(720, 1435)">
          <line x1="-30" y1="170" x2="-40" y2="320" class="stroke-main" />
          <line x1="30" y1="170" x2="40" y2="320" class="stroke-main" />
          <ellipse cx="-45" cy="320" rx="18" ry="8" fill="#121824" />
          <ellipse cx="45" cy="320" rx="18" ry="8" fill="#121824" />

          <g id="deputy-body">
            <rect x="-25" y="-28" width="50" height="38" rx="8" class="guard-blue" />
            <rect x="-55" y="0" width="110" height="175" rx="50" class="guard-blue" />
            <line x1="-53" y1="90" x2="53" y2="90" stroke="#facc15" stroke-width="12" />
            <rect x="-14" y="82" width="28" height="16" rx="3" class="gold-trim" />

            <g id="deputy-head-rig" transform="translate(0, -56)">
              <circle cx="0" cy="0" r="58" class="head-white" />
              <g id="deputy-fedora" transform="translate(0, -48)">
                <ellipse cx="0" cy="0" rx="84" ry="15" class="guard-dark" />
                <path d="M -50 -5 Q -40 -65 0 -68 Q 40 -65 50 -5 Z" class="guard-blue" />
                <rect x="-50" y="-18" width="100" height="18" fill="#facc15" stroke="#121824" stroke-width="4" />
              </g>

              <path d="M -30 -6 Q -18 -20 -8 -6" class="stroke-main" stroke-width="6" fill="none" />
              <path d="M 8 -6 Q 18 -20 30 -6" class="stroke-main" stroke-width="6" fill="none" />
              <path d="M -34 4 Q -44 18 -36 30" stroke="#38bdf8" stroke-width="5" stroke-linecap="round" fill="none" />

              <g id="deputy-mouth" transform="translate(0, 16)">
                <path d="M -24 0 Q 0 42 24 0 Z" fill="#7f1d1d" stroke="#121824" stroke-width="5" />
                <path d="M -12 18 Q 0 8 12 18 Q 0 34 -12 18 Z" fill="#ef4444" />
              </g>
            </g>

            <path id="deputy-arm-left" d="M -50 35 Q -80 80 -25 105" class="stroke-main" stroke-width="15" fill="none" />
            <path id="deputy-arm-right" d="M 50 35 Q 90 70 65 140" class="stroke-main" stroke-width="15" fill="none" />
          </g>
        </g>
      </svg>
    </div>
  </div>

  <!-- ================= SCENE 3: CORVIN'S WINDOW SIGN (8.2s -> 18.0s) ================= -->
  <div id="scene3" class="scene">
    <div id="camera3" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_window_defs}
        {bpc.bg_window_content}
      </svg>
      <svg class="character-layer" viewBox="0 0 1080 1920">
        <g id="corvin-scene3" transform="translate(360, 1200)">
          <ellipse cx="0" cy="510" rx="120" ry="30" class="shadow-ground" />
          <line x1="-30" y1="210" x2="-35" y2="500" class="stroke-main" stroke-width="8" />
          <line x1="30" y1="210" x2="35" y2="500" class="stroke-main" stroke-width="8" />
          <ellipse cx="-40" cy="500" rx="22" ry="9" fill="#121824" />
          <ellipse cx="40" cy="500" rx="22" ry="9" fill="#121824" />

          <g id="corvin-body3">
            <rect x="-30" y="-30" width="60" height="40" rx="10" class="corvin-shirt" />
            <rect x="-60" y="0" width="120" height="215" rx="50" class="corvin-shirt" />
            <path d="M -50 50 L 50 50 L 55 205 L -55 205 Z" class="corvin-apron" />
            <rect x="-28" y="115" width="56" height="42" rx="6" fill="#713f12" stroke="#121824" stroke-width="5" />

            <!-- Corvin Head with spectacles -->
            <g id="corvin-head3" transform="translate(0, -64)">
              <circle cx="0" cy="0" r="64" class="head-white" />
              <path d="M -62 -10 C -72 -35, -45 -55, -40 -40" class="stroke-main" stroke-width="8" stroke-linecap="round" fill="none" />
              <path d="M 62 -10 C 72 -35, 45 -55, 40 -40" class="stroke-main" stroke-width="8" stroke-linecap="round" fill="none" />
              <circle cx="-20" cy="-6" r="15" fill="none" stroke="#b45309" stroke-width="5" />
              <circle cx="20" cy="-6" r="15" fill="none" stroke="#b45309" stroke-width="5" />
              <line x1="-5" y1="-6" x2="5" y2="-6" stroke="#b45309" stroke-width="5" />
              <path id="corvin-mouth3" d="M -16 28 Q 0 16 16 28" class="stroke-main" fill="none" />

              <!-- Confused question marks hovering -->
              <g id="confused-marks" transform="translate(45, -50)">
                <text x="0" y="0" font-family="'Montserrat', sans-serif" font-weight="900" font-size="42" fill="#facc15">?</text>
                <text x="25" y="-20" font-family="'Montserrat', sans-serif" font-weight="900" font-size="32" fill="#38bdf8">?</text>
              </g>
            </g>

            <path id="corvin-arm-scratch" d="M -55 40 Q -105 10 -45 -45" class="stroke-main" stroke-width="16" fill="none" />

            <!-- Corvin holding Tally Slate: '300 RIGHT SHOES' -->
            <g id="corvin-tally-slate" transform="translate(70, 70)">
              <rect x="-10" y="-10" width="130" height="90" rx="8" fill="#1e293b" stroke="#713f12" stroke-width="5"/>
              <text x="55" y="16" font-family="'Montserrat', sans-serif" font-weight="900" font-size="13" fill="#facc15" text-anchor="middle">COUNT:</text>
              <text x="55" y="38" font-family="'Montserrat', sans-serif" font-weight="900" font-size="20" fill="#ffffff" text-anchor="middle">300 RIGHT</text>
              <text x="55" y="62" font-family="'Montserrat', sans-serif" font-weight="800" font-size="14" fill="#ef4444" text-anchor="middle">0 LEFT ❌</text>
            </g>
          </g>
        </g>

        <!-- Hanging Window Sign: ONE RIGHT SHOE 50% OFF -->
        <g id="hanging-window-sign" transform="translate(740, 720)">
          <line x1="-130" y1="-160" x2="-130" y2="0" stroke="#475569" stroke-width="7" stroke-dasharray="10 8" />
          <line x1="130" y1="-160" x2="130" y2="0" stroke="#475569" stroke-width="7" stroke-dasharray="10 8" />
          <rect x="-175" y="0" width="350" height="230" rx="18" fill="#fef08a" stroke="#854d0e" stroke-width="10" />
          <rect x="-160" y="14" width="320" height="202" rx="12" fill="none" stroke="#ca8a04" stroke-width="4" stroke-dasharray="12 6" />
          <text x="0" y="60" font-family="'Montserrat', sans-serif" font-weight="900" font-size="34" fill="#991b1b" text-anchor="middle">ONE RIGHT SHOE</text>
          <text x="0" y="125" font-family="'Montserrat', sans-serif" font-weight="900" font-size="52" fill="#b91c1c" text-anchor="middle">50% OFF</text>
          <text x="0" y="180" font-family="'Montserrat', sans-serif" font-weight="800" font-size="28" fill="#15803d" text-anchor="middle">HALF PRICE!</text>
        </g>
      </svg>
    </div>
  </div>

  <!-- ================= SCENE 4: 10 GUARDS STAKEOUT (18.0s -> 24.5s) ================= -->
  <div id="scene4" class="scene">
    <div id="camera4" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_workshop_defs}
        {bpc.bg_workshop_content}
        <!-- Additional hiding guards in background -->
        <!-- Guard 3 peeking from behind left shelf -->
        <g transform="translate(140, 440)">
          <circle cx="0" cy="0" r="38" class="head-white" />
          <path d="M -38 -10 C -38 -45, 38 -45, 38 -10 Z" fill="#64748b" stroke="#121824" stroke-width="4" />
          <circle cx="-10" cy="2" r="4.5" fill="#000" />
          <circle cx="10" cy="2" r="4.5" fill="#000" />
        </g>
        <!-- Guard 4 under workbench -->
        <g transform="translate(480, 1620)">
          <circle cx="0" cy="0" r="35" class="head-white" />
          <path d="M -35 -10 C -35 -45, 35 -45, 35 -10 Z" fill="#64748b" stroke="#121824" stroke-width="4" />
          <circle cx="-10" cy="2" r="4" fill="#000" />
          <circle cx="10" cy="2" r="4" fill="#000" />
          <line x1="35" y1="-20" x2="60" y2="-80" stroke="#cbd5e1" stroke-width="6"/>
          <polygon points="60,-80 50,-100 70,-100" fill="#facc15"/>
        </g>
      </svg>
      <svg class="character-layer" viewBox="0 0 1080 1920">
        <!-- Guard 1 -->
        <g id="stakeout-guard1" transform="translate(300, 1360)">
          <ellipse cx="0" cy="190" rx="95" ry="26" class="shadow-ground" />
          <rect x="-55" y="0" width="110" height="150" rx="42" class="guard-blue" />
          <g transform="translate(0, -52)">
            <circle cx="0" cy="0" r="56" class="head-white" />
            <path d="M -56 -10 C -56 -68, 56 -68, 56 -10 Z" fill="#64748b" stroke="#121824" stroke-width="6" />
            <line x1="-56" y1="-10" x2="56" y2="-10" stroke="#facc15" stroke-width="8" />
            <ellipse id="eye-guard1-l" cx="-16" cy="5" rx="6" ry="6" fill="#000" />
            <ellipse id="eye-guard1-r" cx="16" cy="5" rx="6" ry="6" fill="#000" />
            <ellipse id="mouth-guard1" cx="0" cy="28" rx="9" ry="14" fill="#7f1d1d" stroke="#121824" stroke-width="4" />
          </g>
          <line x1="60" y1="-140" x2="60" y2="190" stroke="#cbd5e1" stroke-width="8" />
          <polygon points="60,-180 45,-140 75,-140" fill="#facc15" stroke="#121824" stroke-width="5" />
          <!-- Floating Zzz sleeping bubble -->
          <g id="guard1-zzz" transform="translate(60, -110)">
            <text x="0" y="0" font-family="'Montserrat', sans-serif" font-weight="900" font-size="34" fill="#facc15">Z</text>
            <text x="18" y="-18" font-family="'Montserrat', sans-serif" font-weight="900" font-size="26" fill="#93c5fd">z</text>
            <text x="32" y="-32" font-family="'Montserrat', sans-serif" font-weight="900" font-size="20" fill="#93c5fd">z</text>
          </g>
        </g>

        <!-- Guard 2 -->
        <g id="stakeout-guard2" transform="translate(740, 1380)">
          <ellipse cx="0" cy="190" rx="95" ry="26" class="shadow-ground" />
          <rect x="-55" y="0" width="110" height="150" rx="42" class="guard-blue" />
          <g transform="translate(0, -52)">
            <circle cx="0" cy="0" r="56" class="head-white" />
            <path d="M -56 -10 C -56 -68, 56 -68, 56 -10 Z" fill="#64748b" stroke="#121824" stroke-width="6" />
            <line x1="-56" y1="-10" x2="56" y2="-10" stroke="#facc15" stroke-width="8" />
            <ellipse id="eye-guard2-l" cx="-16" cy="5" rx="6" ry="6" fill="#000" />
            <ellipse id="eye-guard2-r" cx="16" cy="5" rx="6" ry="6" fill="#000" />
            <ellipse id="mouth-guard2" cx="0" cy="28" rx="9" ry="14" fill="#7f1d1d" stroke="#121824" stroke-width="4" />
          </g>
        </g>

        <!-- Vanishing Boots with green magic smoke -->
        <g id="vanishing-boots-cluster" transform="translate(520, 800)">
          <g id="ghost-boot">
            <path d="M -45 0 C -25 -32, 25 -28, 50 10 C 40 32, -10 28, -50 16 Z" fill="#22c55e" stroke="#15803d" stroke-width="6" />
          </g>
          <circle id="smoke1" cx="-30" cy="-25" r="35" fill="rgba(74, 222, 128, 0.7)" />
          <circle id="smoke2" cx="25" cy="-40" r="45" fill="rgba(34, 197, 94, 0.7)" />
          <circle id="smoke3" cx="10" cy="20" r="30" fill="rgba(74, 222, 128, 0.6)" />
          <polygon id="sparkle1" points="0,-45 6,-28 22,-28 9,-18 14,0 0,-11 -14,0 -9,-18 -22,-28 -6,-28" fill="#facc15" />
          <polygon id="sparkle2" points="55,10 58,22 68,22 60,30 63,42 55,34 47,42 50,30 42,22 52,22" fill="#facc15" />
        </g>
      </svg>
    </div>
  </div>

  <!-- ================= SCENE 5: THE HOPPING SHOP (24.5s -> 29.0s) ================= -->
  <div id="scene5" class="scene">
    <div id="camera5" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_street_defs}
        {bpc.bg_street_content}
        <!-- Festive Garlands & Flags across buildings -->
        <path d="M0,420 Q270,520 540,460 Q810,520 1080,420" stroke="#78350f" stroke-width="4" fill="none"/>
        <polygon points="120,450 150,510 180,455" fill="#ef4444"/>
        <polygon points="260,470 290,530 320,475" fill="#facc15"/>
        <polygon points="400,480 430,540 460,482" fill="#3b82f6"/>
        <polygon points="620,482 650,540 680,480" fill="#22c55e"/>
        <polygon points="760,475 790,530 820,470" fill="#a855f7"/>

        <!-- Chalk Hopscotch on street cobblestones -->
        <g transform="translate(340, 1680) rotate(-15)">
          <rect x="0" y="0" width="70" height="70" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="6 3"/>
          <text x="35" y="48" font-family="'Montserrat', sans-serif" font-weight="900" font-size="34" fill="#ffffff" text-anchor="middle">1</text>
          <rect x="0" y="-80" width="70" height="70" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="6 3"/>
          <text x="35" y="-32" font-family="'Montserrat', sans-serif" font-weight="900" font-size="34" fill="#ffffff" text-anchor="middle">2</text>
          <rect x="-40" y="-160" width="70" height="70" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="6 3"/>
          <text x="-5" y="-112" font-family="'Montserrat', sans-serif" font-weight="900" font-size="34" fill="#ffffff" text-anchor="middle">3</text>
          <rect x="40" y="-160" width="70" height="70" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="6 3"/>
          <text x="75" y="-112" font-family="'Montserrat', sans-serif" font-weight="900" font-size="34" fill="#ffffff" text-anchor="middle">4</text>
        </g>
      </svg>
      <svg class="character-layer" viewBox="0 0 1080 1920">
        <g id="hopping-shop-banner" transform="translate(540, 480)">
          <rect x="-260" y="-60" width="520" height="120" rx="22" fill="#fef08a" stroke="#854d0e" stroke-width="9" />
          <text x="0" y="16" font-family="'Montserrat', sans-serif" font-weight="900" font-size="40" fill="#991b1b" text-anchor="middle">THE HOPPING SHOP 🦘</text>
        </g>

        <!-- Kid 1: True one-legged hopping pose (other leg bent up) -->
        <g id="hopping-kid1" transform="translate(260, 1420)">
          <ellipse id="kid1-shadow" cx="0" cy="340" rx="65" ry="18" class="shadow-ground" />
          <g id="kid1-body-rig">
            <!-- Straight leg touching ground -->
            <line x1="0" y1="145" x2="0" y2="330" class="stroke-main" stroke-width="8" />
            <ellipse cx="10" cy="330" rx="20" ry="9" fill="#121824" />
            <!-- Bent leg tucked high up (hopping on one leg!) -->
            <path d="M 15 145 L 60 180 L 25 210" class="stroke-main" stroke-width="10" fill="none" />
            <ellipse cx="25" cy="210" rx="14" ry="7" fill="#121824"/>

            <rect x="-44" y="0" width="88" height="150" rx="40" fill="#ef4444" stroke="#121824" stroke-width="7" />

            <g transform="translate(0, -52)">
              <circle cx="0" cy="0" r="52" class="head-white" />
              <path d="M -52 -10 C -52 -58, 48 -58, 48 -10 Z" fill="#3b82f6" stroke="#121824" stroke-width="6" />
              <circle cx="-14" cy="-4" r="5.5" fill="#000" />
              <circle cx="18" cy="-4" r="5.5" fill="#000" />
              <path d="M -12 16 Q 2 34 16 16 Z" fill="#7f1d1d" stroke="#121824" stroke-width="4" />
            </g>

            <path id="kid1-arms" d="M -42 30 Q -85 -10 -65 -45 M 42 30 Q 85 -10 65 -45" class="stroke-main" stroke-width="14" stroke-linecap="round" fill="none" />
          </g>
        </g>

        <!-- Kid 2: Also hopping on one foot -->
        <g id="hopping-kid2" transform="translate(740, 1440)">
          <ellipse id="kid2-shadow" cx="0" cy="340" rx="65" ry="18" class="shadow-ground" />
          <g id="kid2-body-rig">
            <line x1="0" y1="140" x2="0" y2="330" class="stroke-main" stroke-width="8" />
            <ellipse cx="-10" cy="330" rx="20" ry="9" fill="#121824" />
            <path d="M -15 140 L -60 180 L -25 210" class="stroke-main" stroke-width="10" fill="none" />
            <ellipse cx="-25" cy="210" rx="14" ry="7" fill="#121824"/>

            <rect x="-40" y="0" width="80" height="140" rx="36" fill="#eab308" stroke="#121824" stroke-width="7" />

            <g transform="translate(0, -50)">
              <circle cx="0" cy="0" r="48" class="head-white" />
              <circle cx="-12" cy="-4" r="5" fill="#000" />
              <circle cx="14" cy="-4" r="5" fill="#000" />
              <path d="M -10 14 Q 1 26 12 14 Z" fill="#7f1d1d" stroke="#121824" stroke-width="4" />
            </g>

            <path id="kid2-arms" d="M -38 25 Q -75 60 -45 95 M 38 25 Q 75 -20 55 -55" class="stroke-main" stroke-width="13" stroke-linecap="round" fill="none" />
          </g>
        </g>
      </svg>
    </div>
  </div>

  <!-- ================= SCENE 6: WINTER DESPAIR (29.0s -> 33.2s) ================= -->
  <div id="scene6" class="scene">
    <div id="camera6" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_winter_defs}
        {bpc.bg_winter_content}
      </svg>
      <svg class="character-layer" viewBox="0 0 1080 1920">
        <g id="snow-layer">
          <circle cx="180" cy="300" r="7" fill="#ffffff" opacity="0.85" />
          <circle cx="450" cy="220" r="9" fill="#ffffff" opacity="0.95" />
          <circle cx="780" cy="380" r="6" fill="#ffffff" opacity="0.75" />
          <circle cx="920" cy="180" r="8" fill="#ffffff" opacity="0.85" />
          <circle cx="280" cy="700" r="9" fill="#ffffff" opacity="0.9" />
          <circle cx="620" cy="620" r="7" fill="#ffffff" opacity="0.8" />
          <circle cx="840" cy="840" r="10" fill="#ffffff" opacity="0.95" />
        </g>

        <!-- Broke Corvin shivering with empty white pockets hanging out -->
        <g id="broke-corvin" transform="translate(480, 1380)">
          <ellipse cx="0" cy="380" rx="130" ry="32" class="shadow-ground" />
          <rect x="-45" y="240" width="90" height="22" rx="4" fill="#5c2e0b" stroke="#121824" stroke-width="6" />
          <line x1="-35" y1="262" x2="-50" y2="370" stroke="#5c2e0b" stroke-width="8" />
          <line x1="35" y1="262" x2="50" y2="370" stroke="#5c2e0b" stroke-width="8" />

          <g id="shivering-corvin">
            <path d="M -35 210 L -45 285 L -50 370" class="stroke-main" stroke-width="8" fill="none" />
            <path d="M 35 210 L 45 285 L 50 370" class="stroke-main" stroke-width="8" fill="none" />

            <path d="M -55 40 Q -70 145 -45 220 L 45 220 Q 70 145 55 40 Z" fill="#64748b" stroke="#121824" stroke-width="7" />
            <rect x="-35" y="95" width="70" height="90" fill="#475569" stroke="#121824" stroke-width="4" stroke-dasharray="6 4" />

            <!-- Pockets pulled inside out (white flaps dangling = BROKE!) -->
            <path d="M -50 150 Q -75 165 -65 195 Q -55 195 -48 165 Z" fill="#ffffff" stroke="#121824" stroke-width="3"/>
            <path d="M 50 150 Q 75 165 65 195 Q 55 195 48 165 Z" fill="#ffffff" stroke="#121824" stroke-width="3"/>

            <g id="corvin-droop-head" transform="translate(0, -25) rotate(18)">
              <circle cx="0" cy="0" r="62" class="head-white" />
              <circle cx="-18" cy="4" r="13" fill="none" stroke="#b45309" stroke-width="4" />
              <circle cx="18" cy="4" r="13" fill="none" stroke="#b45309" stroke-width="4" />
              <circle cx="0" cy="12" r="8" fill="#93c5fd" />
              <path d="M -15 28 Q 0 16 15 28" class="stroke-main" fill="none" />
              <!-- Cold shivering breath puff -->
              <path id="breath-puff" d="M 15 32 Q 40 38 60 25 Q 75 15 65 35 Q 50 50 30 40 Z" fill="rgba(255,255,255,0.75)" />
            </g>

            <path d="M -50 65 Q 0 130 50 65" class="stroke-main" stroke-width="16" fill="none" />
          </g>
        </g>
      </svg>
    </div>
  </div>

  <!-- ================= SCENE 7: THE STRANGER'S OFFER (33.2s -> 41.7s) ================= -->
  <div id="scene7" class="scene">
    <div id="camera7" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_workshop_defs}
        {bpc.bg_workshop_content}
        <!-- Firewood Crate prop on counter: 'FOR FIREWOOD' -->
        <g transform="translate(710, 1370)">
          <rect x="0" y="0" width="130" height="95" rx="6" fill="#78350f" stroke="#3b1d08" stroke-width="4"/>
          <line x1="0" y1="32" x2="130" y2="32" stroke="#3b1d08" stroke-width="3"/>
          <line x1="0" y1="64" x2="130" y2="64" stroke="#3b1d08" stroke-width="3"/>
          <!-- Wooden Logs sticking out -->
          <ellipse cx="30" cy="-6" rx="14" ry="10" fill="#a16207" stroke="#451a03" stroke-width="2"/>
          <ellipse cx="65" cy="-10" rx="14" ry="10" fill="#a16207" stroke="#451a03" stroke-width="2"/>
          <ellipse cx="100" cy="-6" rx="14" ry="10" fill="#a16207" stroke="#451a03" stroke-width="2"/>
          <rect x="15" y="100" width="100" height="28" rx="4" fill="#fef08a" stroke="#854d0e" stroke-width="2"/>
          <text x="65" y="119" font-family="'Montserrat', sans-serif" font-weight="900" font-size="12" fill="#991b1b" text-anchor="middle">FOR FIREWOOD 🪵</text>
        </g>
      </svg>
      <svg class="character-layer" viewBox="0 0 1080 1920">
        <!-- Corvin (Left, weeping happy tears of relief) -->
        <g id="relieved-corvin" transform="translate(280, 1380)">
          <ellipse cx="0" cy="380" rx="110" ry="28" class="shadow-ground" />
          <line x1="-25" y1="180" x2="-30" y2="370" class="stroke-main" stroke-width="8" />
          <line x1="25" y1="180" x2="30" y2="370" class="stroke-main" stroke-width="8" />
          <ellipse cx="-35" cy="370" rx="20" ry="9" fill="#121824" />
          <ellipse cx="35" cy="370" rx="20" ry="9" fill="#121824" />

          <rect x="-55" y="0" width="110" height="190" rx="45" class="corvin-shirt" />
          <g transform="translate(0, -60)">
            <circle cx="0" cy="0" r="60" class="head-white" />
            <path id="corvin-tear-l" d="M -20 8 Q -26 35 -20 55" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" fill="none" />
            <path id="corvin-tear-r" d="M 20 8 Q 26 35 20 55" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" fill="none" />
            <path d="M -16 26 Q 0 42 16 26" class="stroke-main" fill="none" />
          </g>
          <!-- Hands clasped together in gratitude -->
          <circle cx="0" cy="90" r="22" fill="#ffffff" stroke="#121824" stroke-width="6" />
        </g>

        <!-- Quiet Stranger (Right) -->
        <g id="quiet-stranger-scene7" transform="translate(780, 1320)">
          <ellipse cx="0" cy="440" rx="125" ry="32" class="shadow-ground" />
          <line x1="-30" y1="220" x2="-35" y2="430" class="stroke-main" stroke-width="8" />
          <line x1="30" y1="220" x2="35" y2="430" class="stroke-main" stroke-width="8" />
          <ellipse cx="-40" cy="430" rx="22" ry="9" fill="#121824" />
          <ellipse cx="40" cy="430" rx="22" ry="9" fill="#121824" />

          <g id="stranger-body-deal">
            <path d="M -60 0 C -75 130, -70 200, -55 230 L 55 230 C 70 200, 75 130, 60 0 Z" class="stranger-cloak" />
            <path d="M -50 10 Q 0 25 50 10 Q 35 50 0 50 Q -35 50 -50 10 Z" class="stranger-scarf" />

            <g transform="translate(0, -66)">
              <circle cx="0" cy="0" r="64" class="head-white" />
              <path d="M -64 -10 C -64 -80, 64 -80, 64 -10 Z" fill="#0f172a" stroke="#121824" stroke-width="7" />
              <line x1="-30" y1="-5" x2="-12" y2="-5" class="stroke-main" stroke-width="6" />
              <circle cx="-21" cy="-1" r="4" fill="#000" />
              <line x1="12" y1="-5" x2="30" y2="-5" class="stroke-main" stroke-width="6" />
              <circle cx="21" cy="-1" r="4" fill="#000" />
              <path d="M -10 24 Q 4 28 18 18" class="stroke-main" fill="none" />
            </g>

            <path id="stranger-arm-coins" d="M -50 50 Q -80 120 -150 170" class="stroke-main" stroke-width="16" fill="none" />
          </g>
        </g>

        <!-- 5 Gleaming Gold Coins resting directly on wooden table surface -->
        <g id="five-coins" transform="translate(560, 1515)">
          <ellipse cx="-65" cy="0" rx="26" ry="12" class="gold-trim" />
          <ellipse cx="-32" cy="-6" rx="26" ry="12" class="gold-trim" />
          <ellipse cx="2" cy="0" rx="26" ry="12" class="gold-trim" />
          <ellipse cx="36" cy="-6" rx="26" ry="12" class="gold-trim" />
          <ellipse cx="70" cy="0" rx="26" ry="12" class="gold-trim" />
          <polygon id="coin-sparkle" points="2,-28 6,-18 16,-18 9,-10 12,0 2,-6 -6,0 -3,-10 -10,-18 0,-18" fill="#ffffff" />
        </g>
      </svg>
    </div>
  </div>

  <!-- ================= SCENE 8: THE GRAND SHOE BOUTIQUE (41.7s -> 66.0s) ================= -->
  <div id="scene8" class="scene">
    <div id="camera8" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_boutique_defs}
        {bpc.bg_boutique_content}
      </svg>

      <!-- Infographic Card 1: 1 Shoe = Worthless, Matched Pair = 100$ (Active at 50s-56s) -->
      <div id="info-card-puzzle" class="info-card" style="top: 360px; left: 60px; right: 60px;">
        <div style="font-size: 26px; font-weight: 900; color: #facc15; letter-spacing: 2px; margin-bottom: 14px;">THE SECRET FORMULA</div>
        <div style="display: flex; justify-content: space-around; align-items: center; font-size: 24px; font-weight: 900;">
          <div style="color: #ef4444;">1 LONE SHOE<br><span style="font-size: 34px;">0$ ❌</span></div>
          <div style="font-size: 40px; color: #94a3b8;">+</div>
          <div style="color: #ef4444;">1 LONE SHOE<br><span style="font-size: 34px;">0$ ❌</span></div>
          <div style="font-size: 40px; color: #facc15;">➔</div>
          <div style="color: #22c55e;">MATCHED PAIR<br><span style="font-size: 34px;">100$ ⭐</span></div>
        </div>
      </div>

      <!-- Infographic Card 2: 5 Coins for 300 Pairs (Active at 57.5s-64s) -->
      <div id="info-card-wealth" class="info-card" style="top: 380px; left: 80px; right: 80px;">
        <div style="font-size: 24px; font-weight: 900; color: #38bdf8; letter-spacing: 2px; margin-bottom: 10px;">MASTERSTROKE DEPOSIT</div>
        <div style="font-size: 44px; font-weight: 900; color: #facc15;">5 COINS ➔ 300 PAIRS</div>
        <div style="font-size: 28px; font-weight: 900; color: #22c55e; margin-top: 8px;">= 30,000 GOLD COINS! 💰</div>
      </div>

      <svg class="character-layer" viewBox="0 0 1080 1920">
        <!-- Floating Gold Sparkles -->
        <g id="boutique-sparkles">
          <polygon points="200,450 205,465 220,465 208,475 212,490 200,480 188,490 192,475 180,465 195,465" fill="#facc15" opacity="0.9" />
          <polygon points="880,380 884,395 898,395 887,404 891,418 880,409 869,418 873,404 862,395 876,395" fill="#facc15" opacity="0.9" />
          <polygon points="540,280 545,295 560,295 548,305 552,320 540,310 528,320 532,305 520,295 535,295" fill="#facc15" opacity="0.95" />
        </g>

        <!-- THE QUIET STRANGER (Standing proud behind counter as the Master Cobbler) -->
        <g id="master-stranger" transform="translate(540, 1200)">
          <g id="master-stranger-body">
            <rect x="-70" y="0" width="140" height="225" rx="55" fill="#0f172a" stroke="#121824" stroke-width="7" />
            <path d="M -45 20 L 0 100 L 45 20 L 55 195 L -55 195 Z" fill="#b45309" stroke="#121824" stroke-width="5" />
            <polygon points="-9,25 9,25 14,90 0,115 -14,90" fill="#15803d" stroke="#121824" stroke-width="4" />
            <path d="M -35 115 Q 0 142 30 120" stroke="#facc15" stroke-width="7" fill="none" />

            <g id="master-stranger-head" transform="translate(0, -68)">
              <circle cx="0" cy="0" r="68" class="head-white" />
              <g transform="translate(0, -60)">
                <ellipse cx="0" cy="0" rx="100" ry="18" fill="#0f172a" stroke="#121824" stroke-width="7" />
                <rect x="-60" y="-120" width="120" height="120" rx="6" fill="#1e293b" stroke="#121824" stroke-width="7" />
                <rect x="-60" y="-22" width="120" height="22" fill="#facc15" stroke="#121824" stroke-width="5" />
                <rect x="-15" y="-27" width="30" height="32" rx="4" fill="#ffffff" stroke="#121824" stroke-width="4" />
              </g>

              <circle id="wink-eye-l" cx="-24" cy="0" r="6.5" fill="#000" />
              <path id="wink-eye-r" d="M 12 0 Q 25 -14 38 0" class="stroke-main" stroke-width="7" fill="none" />
              <!-- Sparkling star on winking eye -->
              <polygon points="38,-10 40,-3 47,-3 41,2 43,9 38,5 33,9 35,2 29,-3 36,-3" fill="#facc15"/>
              <path d="M -22 28 Q 4 52 30 24" class="stroke-main" stroke-width="7" fill="none" />
            </g>

            <path id="master-arm-l" d="M -65 45 Q -105 100 -50 135" class="stroke-main" stroke-width="18" fill="none" />
            <path id="master-arm-r" d="M 65 45 Q 105 100 50 135" class="stroke-main" stroke-width="18" fill="none" />
          </g>
        </g>

        <!-- Golden Stacks of Wealth resting on mahogany counter -->
        <g id="coin-stacks-left" transform="translate(240, 1420)">
          <ellipse cx="-30" cy="10" rx="28" ry="11" class="gold-trim" />
          <ellipse cx="-30" cy="0" rx="28" ry="11" class="gold-trim" />
          <ellipse cx="-30" cy="-10" rx="28" ry="11" class="gold-trim" />
          <ellipse cx="-30" cy="-20" rx="28" ry="11" class="gold-trim" />
          
          <ellipse cx="25" cy="10" rx="30" ry="11" class="gold-trim" />
          <ellipse cx="25" cy="-1" rx="30" ry="11" class="gold-trim" />
          <ellipse cx="25" cy="-12" rx="30" ry="11" class="gold-trim" />
          <ellipse cx="25" cy="-23" rx="30" ry="11" class="gold-trim" />
          <ellipse cx="25" cy="-34" rx="30" ry="11" class="gold-trim" />
        </g>

        <!-- Matching Display Shoes (Complete Pair!) on Red Velvet Cushion -->
        <g id="matching-pair-display" transform="translate(760, 1420)">
          <ellipse cx="0" cy="18" rx="85" ry="24" fill="#991b1b" stroke="#7f1d1d" stroke-width="5" />
          <path d="M -55 -5 C -30 -25, 0 -20, 15 5 C 5 22, -30 20, -60 12 Z" class="boot-leather" />
          <path d="M -5 0 C 20 -20, 50 -15, 65 10 C 55 27, 20 25, -10 17 Z" class="boot-leather" />
        </g>
      </svg>
    </div>
  </div>

  <!-- ================= DYNAMIC WORD-BY-WORD SUBTITLES ================= -->
  <div id="caption-box">
    <div id="caption-phrase" class="caption-phrase"></div>
  </div>
</div>

<script>
const SUBTITLE_CHUNKS = {json.dumps(chunks, indent=2)};

const captionPhraseEl = document.getElementById("caption-phrase");
const scenes = [
  {{ el: document.getElementById("scene1"), start: 0.0, end: 5.25 }},
  {{ el: document.getElementById("scene2"), start: 5.25, end: 8.2 }},
  {{ el: document.getElementById("scene3"), start: 8.2, end: 18.0 }},
  {{ el: document.getElementById("scene4"), start: 18.0, end: 24.5 }},
  {{ el: document.getElementById("scene5"), start: 24.5, end: 29.0 }},
  {{ el: document.getElementById("scene6"), start: 29.0, end: 33.2 }},
  {{ el: document.getElementById("scene7"), start: 33.2, end: 41.7 }},
  {{ el: document.getElementById("scene8"), start: 41.7, end: 66.0 }}
];

const masterTimeline = gsap.timeline({{ paused: true }});

// Scene 1: Thief
masterTimeline.fromTo("#camera1", {{ scale: 1.05, y: 0 }}, {{ scale: 1.18, y: -40, duration: 5.25, ease: "sine.inOut" }}, 0);
masterTimeline.to("#thief-dangler", {{ rotation: 4, duration: 2.5, yoyo: true, repeat: 1, ease: "sine.inOut" }}, 0);
masterTimeline.to("#snatched-shoe", {{ y: -30, rotation: -10, duration: 1.8, ease: "power2.out" }}, 2.0);

// Scene 2: Guards Laughing
masterTimeline.fromTo("#camera2", {{ scale: 1.06, x: -20 }}, {{ scale: 1.15, x: 20, duration: 3.0, ease: "sine.inOut" }}, 5.25);
masterTimeline.to("#chief-body", {{ y: -16, duration: 0.22, yoyo: true, repeat: 12, ease: "power1.inOut" }}, 5.25);
masterTimeline.to("#chief-mouth", {{ scaleY: 1.35, duration: 0.22, yoyo: true, repeat: 12, transformOrigin: "0 0" }}, 5.25);
masterTimeline.to("#deputy-body", {{ y: -14, duration: 0.25, yoyo: true, repeat: 11, ease: "power1.inOut" }}, 5.35);
masterTimeline.to("#deputy-mouth", {{ scaleY: 1.3, duration: 0.25, yoyo: true, repeat: 11, transformOrigin: "0 0" }}, 5.35);

// Scene 3: Corvin Counting & Sign
masterTimeline.fromTo("#camera3", {{ scale: 1.04, y: 0 }}, {{ scale: 1.20, y: -60, duration: 9.8, ease: "power1.inOut" }}, 8.2);
masterTimeline.to("#hanging-window-sign", {{ rotation: -5, duration: 2.2, yoyo: true, repeat: 4, ease: "sine.inOut", transformOrigin: "0 -160" }}, 8.2);
masterTimeline.to("#corvin-body3", {{ y: -10, duration: 1.8, yoyo: true, repeat: 4, ease: "sine.inOut" }}, 8.5);
masterTimeline.fromTo("#confused-marks", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1.2, duration: 1.2, ease: "back.out" }}, 9.5);

// Scene 4: Stakeout & Vanishing Boot
masterTimeline.fromTo("#camera4", {{ scale: 1.05, y: -20 }}, {{ scale: 1.16, y: -45, duration: 6.5, ease: "sine.inOut" }}, 18.0);
masterTimeline.to(["#eye-guard1-l", "#eye-guard1-r", "#eye-guard2-l", "#eye-guard2-r"], {{ x: -6, duration: 0.8, yoyo: true, repeat: 5, ease: "power1.inOut" }}, 18.2);
masterTimeline.fromTo("#guard1-zzz", {{ opacity: 0, y: 15 }}, {{ opacity: 1, y: -25, duration: 1.5, repeat: 2, ease: "power1.out" }}, 19.5);
masterTimeline.to("#vanishing-boots-cluster", {{ scale: 1.4, opacity: 0, duration: 1.6, ease: "power2.out" }}, 22.2);

// Scene 5: Hopping Kids
masterTimeline.fromTo("#camera5", {{ scale: 1.05, x: 30 }}, {{ scale: 1.14, x: -30, duration: 4.5, ease: "sine.inOut" }}, 24.5);
masterTimeline.to("#hopping-kid1", {{ x: "+=320", duration: 4.2, ease: "none" }}, 24.6);
masterTimeline.to("#kid1-body-rig", {{ y: -75, duration: 0.35, yoyo: true, repeat: 11, ease: "power2.out" }}, 24.6);
masterTimeline.to("#hopping-kid2", {{ x: "+=280", duration: 4.2, ease: "none" }}, 24.7);
masterTimeline.to("#kid2-body-rig", {{ y: -70, duration: 0.38, yoyo: true, repeat: 10, ease: "power2.out" }}, 24.7);

// Scene 6: Winter Broke Corvin
masterTimeline.fromTo("#camera6", {{ scale: 1.04, y: 0 }}, {{ scale: 1.16, y: -30, duration: 4.2, ease: "power1.inOut" }}, 29.0);
masterTimeline.to("#shivering-corvin", {{ x: 4, duration: 0.08, yoyo: true, repeat: 45, ease: "none" }}, 29.0);
masterTimeline.to("#snow-layer", {{ y: 250, duration: 4.2, ease: "none" }}, 29.0);
masterTimeline.fromTo("#breath-puff", {{ opacity: 0.2, scale: 0.7 }}, {{ opacity: 0.9, scale: 1.3, duration: 0.8, yoyo: true, repeat: 4 }}, 29.2);

// Scene 7: 5 Coins Deal
masterTimeline.fromTo("#camera7", {{ scale: 1.05, y: -20 }}, {{ scale: 1.18, y: -50, duration: 8.5, ease: "sine.inOut" }}, 33.2);
masterTimeline.from("#quiet-stranger-scene7", {{ x: 180, opacity: 0, duration: 1.8, ease: "power2.out" }}, 33.4);
masterTimeline.from("#five-coins", {{ y: -80, opacity: 0, duration: 1.0, ease: "bounce.out" }}, 36.6);

// Scene 8: Grand Boutique Climax & Infographics
masterTimeline.fromTo("#camera8", {{ scale: 1.06, y: 0 }}, {{ scale: 1.25, y: -65, duration: 23.8, ease: "sine.inOut" }}, 41.7);
masterTimeline.to("#boutique-sparkles", {{ y: -60, duration: 4.0, yoyo: true, repeat: 5, ease: "sine.inOut" }}, 41.7);
masterTimeline.to("#master-stranger-body", {{ y: -12, duration: 2.2, yoyo: true, repeat: 9, ease: "sine.inOut" }}, 42.0);

// Infographic Card 1: 1 shoe = worthless (50.2s -> 56.5s)
masterTimeline.fromTo("#info-card-puzzle", {{ opacity: 0, scale: 0.8, y: 30 }}, {{ opacity: 1, scale: 1.0, y: 0, duration: 0.7, ease: "back.out" }}, 50.2);
masterTimeline.to("#info-card-puzzle", {{ opacity: 0, scale: 0.9, y: -20, duration: 0.5, ease: "power2.in" }}, 56.5);

// Infographic Card 2: 5 coins -> 300 pairs (57.5s -> 64.5s)
masterTimeline.fromTo("#info-card-wealth", {{ opacity: 0, scale: 0.8, y: 30 }}, {{ opacity: 1, scale: 1.0, y: 0, duration: 0.7, ease: "back.out" }}, 57.5);
masterTimeline.to("#info-card-wealth", {{ opacity: 0, scale: 0.9, y: -20, duration: 0.5, ease: "power2.in" }}, 64.5);

let activeChunkIndex = -1;

function updateSubtitles(t) {{
  let currentChunkIdx = -1;
  for (let i = 0; i < SUBTITLE_CHUNKS.length; i++) {{
    if (t >= SUBTITLE_CHUNKS[i].start && t <= SUBTITLE_CHUNKS[i].end) {{
      currentChunkIdx = i;
      break;
    }}
  }}

  if (currentChunkIdx !== activeChunkIndex) {{
    activeChunkIndex = currentChunkIdx;
    if (currentChunkIdx === -1) {{
      captionPhraseEl.innerHTML = "";
    }} else {{
      const chunk = SUBTITLE_CHUNKS[currentChunkIdx];
      captionPhraseEl.innerHTML = chunk.words.map((w, idx) => {{
        return `<span class="word-span" id="w_${{idx}}" data-start="${{w.start}}" data-end="${{w.end}}">${{w.word}}</span>`;
      }}).join("");
    }}
  }}

  if (activeChunkIndex !== -1) {{
    const spans = captionPhraseEl.getElementsByClassName("word-span");
    for (let s of spans) {{
      const start = parseFloat(s.getAttribute("data-start"));
      const end = parseFloat(s.getAttribute("data-end"));
      if (t >= start && t < end) {{
        s.classList.add("active");
      }} else {{
        s.classList.remove("active");
      }}
    }}
  }}
}}

function updateSceneVisibility(t) {{
  for (let s of scenes) {{
    if (t >= s.start && t < s.end) {{
      s.el.classList.add("active");
    }} else {{
      s.el.classList.remove("active");
    }}
  }}
}}

window.seekToTime = function(t) {{
  masterTimeline.time(t);
  updateSceneVisibility(t);
  updateSubtitles(t);
}};

window.seekToTime(0.0);
</script>
</body>
</html>
'''

with open(PROJECT / "scene.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"ULTRA-DETAILED scene.html successfully generated ({len(html_code)} bytes)!")

