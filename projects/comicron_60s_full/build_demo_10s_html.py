"""
build_demo_10s_html.py
Generates demo_10s_character.html — a 10-second master demo showcasing the character-animation skill:
- Welded bone hierarchy (zero floating heads, neck collar bridge, articulated joints)
- Detailed shoes (sole, heel, laces, leather shine, perspective ground shadow)
- Expressive faces (laughing open mouth, squint eyes, laugh tears, confusion brows)
- Micro-assets (workbench, stolen shoe outline, wanted poster, tally board)
- Word-level Montserrat 900 gold subtitles (Comicron signature style)
- Continuous camera motion ("Camera Kabhi Rukta Nahi")
- Deterministic virtual clock (window.seekToTime)
"""

import json
from pathlib import Path
import sys

PROJECT = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\comicron_60s_full")
sys.path.append(str(PROJECT))
import build_procedural_components as bpc

chunks = json.load(open(PROJECT / "subtitle_chunks.json", encoding="utf-8"))
sub10 = [c for c in chunks if c["start"] < 10.0]
chunks_json = json.dumps(sub10)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080, height=1920, initial-scale=1.0">
<title>Comicron 10s Demo - Character Animation Mastery</title>
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
    font-family: 'Montserrat', sans-serif;
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
    background: radial-gradient(circle at 50% 50%, rgba(0,0,0,0) 65%, rgba(0,0,0,0.65) 100%);
    pointer-events: none; z-index: 80;
  }}
  .channel-badge {{
    position: absolute; top: 85px; left: 50%;
    transform: translateX(-50%);
    font-family: 'Montserrat', sans-serif;
    font-size: 22px; font-weight: 900;
    letter-spacing: 5px; color: rgba(255, 255, 255, 0.75);
    text-transform: uppercase; z-index: 90;
    text-shadow: 0 2px 8px rgba(0,0,0,0.85);
    white-space: nowrap;
  }}
  #caption-box {{
    position: absolute; bottom: 200px;
    left: 40px; right: 40px;
    z-index: 100; text-align: center;
    pointer-events: none;
  }}
  .caption-phrase {{
    font-family: 'Montserrat', sans-serif;
    font-size: 56px; font-weight: 900;
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
</style>
<script src="gsap.min.js"></script>
</head>
<body>

<div id="viewport">
  <div class="channel-badge">COMICRON • CHARACTER ANIMATION DEMO</div>
  <div class="vignette-overlay"></div>

  <!-- ================= SCENE 1: THE NIGHT THIEF (0.0s -> 5.2s) ================= -->
  <div id="scene1" class="scene active">
    <div id="camera1" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_workshop_defs}
        {bpc.bg_workshop_content}
        <!-- Stolen shoe outline on workbench -->
        <g transform="translate(140, 640)">
          <path d="M 0 0 C 25 -15, 60 -10, 75 10 C 65 30, 25 28, -5 20 Z" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="6 4" opacity="0.8"/>
          <text x="35" y="32" font-family="'Montserrat', sans-serif" font-weight="900" font-size="12" fill="#ef4444" text-anchor="middle">STOLEN</text>
        </g>
      </svg>

      <svg class="character-layer" viewBox="0 0 1080 1920">
        <!-- Skylight beam cone -->
        <polygon points="380,0 700,0 800,1400 280,1400" fill="rgba(255, 255, 255, 0.11)" />
        <path id="thief-rope" d="M 540 0 L 540 760" stroke="#78553a" stroke-width="8" stroke-dasharray="14 6" />

        <!-- Dangling Thief Character Rig -->
        <g id="thief-dangler" transform="translate(540, 760)">
          <!-- Ground shadow -->
          <ellipse cx="0" cy="850" rx="90" ry="24" class="shadow-ground" opacity="0.6" />
          <!-- Rope holding hands -->
          <circle cx="-16" cy="-20" r="14" class="stranger-cloak" />
          <circle cx="16" cy="-45" r="14" class="stranger-cloak" />

          <g id="thief-body-group">
            <!-- Torso & Cloak -->
            <path d="M -45 -10 C -55 80, -70 140, -60 170 C -20 185, 20 185, 60 170 C 70 140, 55 80, 45 -10 Z" class="stranger-cloak" />
            <path d="M -42 0 Q 0 15 42 0 Q 30 35 0 35 Q -30 35 -42 0 Z" class="stranger-scarf" />
            <path id="scarf-tail" d="M 15 28 Q 30 70 25 110" stroke="#15803d" stroke-width="12" stroke-linecap="round" fill="none" />

            <!-- Seamless Welded Head (Inside body group, zero gap) -->
            <g id="thief-head-group" transform="translate(0, -60)">
              <circle cx="0" cy="0" r="56" class="head-white" />
              <path d="M -42 -12 C -20 -24, 20 -24, 42 -12 C 45 4, 30 14, 0 10 C -30 14, -45 4, -42 -12 Z" fill="#0f172a" />
              <!-- Thief Eyes -->
              <ellipse cx="-18" cy="-5" rx="7" ry="5" fill="#facc15" />
              <circle cx="-16" cy="-5" r="2.5" fill="#000" />
              <ellipse cx="18" cy="-5" rx="7" ry="5" fill="#facc15" />
              <circle cx="20" cy="-5" r="2.5" fill="#000" />
              <!-- Smirking mouth -->
              <path d="M -12 25 Q 2 34 18 22" class="stroke-main" fill="none" />
            </g>

            <!-- Reaching Arm + Hand snatching the Left Shoe -->
            <g id="thief-arm" transform="translate(-40, 60)">
              <path d="M 0 0 Q -45 70 -70 140" stroke="#1e293b" stroke-width="18" stroke-linecap="round" fill="none" />
              <circle cx="-70" cy="140" r="15" fill="#1e293b" />
              <!-- Detailed Snatched Left Shoe with Laces and Sole -->
              <g id="snatched-shoe" transform="translate(-85, 140) rotate(-25)">
                <ellipse cx="25" cy="18" rx="38" ry="10" fill="#2d170a" stroke="#121824" stroke-width="4"/>
                <path d="M 0 0 C 25 -15, 60 -10, 75 10 C 65 30, 25 28, -5 20 C -15 15, -15 8, 0 0 Z" class="boot-leather" />
                <line x1="-10" y1="10" x2="-32" y2="10" stroke="#facc15" stroke-width="3.5" stroke-linecap="round"/>
                <line x1="-10" y1="18" x2="-36" y2="18" stroke="#facc15" stroke-width="3.5" stroke-linecap="round"/>
                <!-- Glow indication -->
                <circle cx="30" cy="5" r="35" fill="none" stroke="#facc15" stroke-width="2" stroke-dasharray="5 4" opacity="0.7"/>
              </g>
            </g>
          </g>
        </g>
      </svg>
    </div>
  </div>

  <!-- ================= SCENE 2: LAUGHING GUARDS & OLD CORVIN (5.2s -> 10.0s) ================= -->
  <div id="scene2" class="scene">
    <div id="camera2" class="camera-rig">
      <svg class="bg-procedural" viewBox="0 0 1080 1920">
        {bpc.bg_street_defs}
        {bpc.bg_street_content}

        <!-- Wanted Poster pinned to town wall -->
        <g id="wanted-poster-group" transform="translate(130, 1100)">
          <rect x="0" y="0" width="180" height="250" rx="8" fill="#fef3c7" stroke="#78350f" stroke-width="6"/>
          <rect x="15" y="15" width="150" height="35" fill="#991b1b" rx="4"/>
          <text x="90" y="39" text-anchor="middle" font-family="'Montserrat',sans-serif" font-weight="900" font-size="17" fill="#ffffff">WANTED</text>
          <!-- One-legged thief sketch -->
          <circle cx="90" cy="100" r="28" fill="none" stroke="#1c1917" stroke-width="4"/>
          <line x1="80" y1="96" x2="84" y2="96" stroke="#1c1917" stroke-width="4" stroke-linecap="round"/>
          <line x1="96" y1="96" x2="100" y2="96" stroke="#1c1917" stroke-width="4" stroke-linecap="round"/>
          <line x1="90" y1="128" x2="90" y2="180" stroke="#1c1917" stroke-width="5" stroke-linecap="round"/>
          <line x1="90" y1="180" x2="72" y2="215" stroke="#1c1917" stroke-width="5" stroke-linecap="round"/>
          <!-- Peg leg / missing other leg -->
          <line x1="90" y1="180" x2="106" y2="195" stroke="#dc2626" stroke-width="4" stroke-linecap="round" stroke-dasharray="4 3"/>
          <text x="90" y="235" text-anchor="middle" font-family="'Montserrat',sans-serif" font-weight="900" font-size="13" fill="#b91c1c">ONE-LEGGED 🦿</text>
          <!-- Wax seals -->
          <circle cx="20" cy="10" r="7" fill="#dc2626" stroke="#7f1d1d" stroke-width="2"/>
          <circle cx="160" cy="10" r="7" fill="#dc2626" stroke="#7f1d1d" stroke-width="2"/>
        </g>
      </svg>

      <svg class="character-layer" viewBox="0 0 1080 1920">
        <!-- Ground shadows -->
        <ellipse cx="360" cy="1760" rx="130" ry="32" class="shadow-ground" />
        <ellipse cx="720" cy="1760" rx="130" ry="32" class="shadow-ground" />
        <ellipse cx="940" cy="1760" rx="90" ry="24" class="shadow-ground" />

        <!-- ── CHIEF GUARD (WELDED ANATOMY + LAUGHING) ── -->
        <g id="chief-guard-root" transform="translate(360, 1420)">
          <!-- Legs with detailed boots -->
          <line x1="-35" y1="180" x2="-45" y2="320" class="stroke-main" />
          <line x1="35" y1="180" x2="45" y2="320" class="stroke-main" />
          <!-- Detailed Guard Boots -->
          <ellipse cx="-52" cy="335" rx="26" ry="11" fill="#0f172a" stroke="#121824" stroke-width="4"/>
          <ellipse cx="-64" cy="330" rx="12" ry="9" fill="#0f172a" stroke="#121824" stroke-width="3"/>
          <ellipse cx="52" cy="335" rx="26" ry="11" fill="#0f172a" stroke="#121824" stroke-width="4"/>
          <ellipse cx="64" cy="330" rx="12" ry="9" fill="#0f172a" stroke="#121824" stroke-width="3"/>

          <!-- Body with welded collar -->
          <g id="chief-body">
            <!-- Overlapping collar bridge: PREVENTS DETACHED HEAD -->
            <rect x="-30" y="-30" width="60" height="40" rx="10" class="guard-blue" />
            <rect x="-60" y="0" width="120" height="185" rx="55" class="guard-blue" />
            <line x1="-58" y1="95" x2="58" y2="95" stroke="#facc15" stroke-width="14" />
            <rect x="-16" y="86" width="32" height="18" rx="4" class="gold-trim" />
            <circle cx="-25" cy="45" r="9" class="gold-trim" />
            <circle cx="-25" cy="65" r="9" class="gold-trim" />

            <!-- Head Group inside Body Group -->
            <g id="chief-head-rig" transform="translate(0, -60)">
              <circle cx="0" cy="0" r="62" class="head-white" />
              <!-- Helmet -->
              <g id="chief-tophat" transform="translate(0, -52)">
                <ellipse cx="0" cy="0" rx="90" ry="16" class="guard-dark" />
                <rect x="-55" y="-120" width="110" height="120" rx="6" class="guard-blue" />
                <rect x="-55" y="-22" width="110" height="22" fill="#facc15" stroke="#121824" stroke-width="5" />
                <polygon points="-8,-120 8,-120 0,-140" class="gold-trim" />
              </g>

              <!-- Happy squint laughing eyes -->
              <path d="M -34 -8 Q -22 -24 -10 -8" class="stroke-main" stroke-width="6" fill="none" />
              <path d="M 10 -8 Q 22 -24 34 -8" class="stroke-main" stroke-width="6" fill="none" />
              <!-- Laugh tears streaming -->
              <path d="M -38 2 Q -50 20 -40 35" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" fill="none" />
              <path d="M 38 2 Q 50 20 40 35" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" fill="none" />

              <!-- Open Laughing Mouth -->
              <g id="chief-mouth" transform="translate(0, 16)">
                <path d="M -28 0 Q 0 48 28 0 Z" fill="#7f1d1d" stroke="#121824" stroke-width="5" />
                <path d="M -14 20 Q 0 10 14 20 Q 0 38 -14 20 Z" fill="#ef4444" />
                <path d="M -20 0 L 20 0 L 15 8 L -15 8 Z" fill="#ffffff" />
              </g>
            </g>

            <!-- Clasping Belly Laugh Arms -->
            <path id="chief-arm-left" d="M -55 35 Q -95 90 -30 115" class="stroke-main" stroke-width="16" fill="none" />
            <path id="chief-arm-right" d="M 55 35 Q 95 90 30 115" class="stroke-main" stroke-width="16" fill="none" />
          </g>
        </g>

        <!-- ── DEPUTY GUARD (LAUGHING SIDE-KICK) ── -->
        <g id="deputy-guard-root" transform="translate(720, 1420)">
          <line x1="-30" y1="180" x2="-40" y2="320" class="stroke-main" />
          <line x1="30" y1="180" x2="40" y2="320" class="stroke-main" />
          <ellipse cx="-48" cy="335" rx="24" ry="10" fill="#0f172a" stroke="#121824" stroke-width="4"/>
          <ellipse cx="48" cy="335" rx="24" ry="10" fill="#0f172a" stroke="#121824" stroke-width="4"/>

          <g id="deputy-body">
            <rect x="-26" y="-30" width="52" height="40" rx="10" class="guard-blue" />
            <rect x="-50" y="0" width="100" height="175" rx="45" class="guard-blue" />
            <line x1="-48" y1="90" x2="48" y2="90" stroke="#facc15" stroke-width="12" />
            <circle cx="-20" cy="45" r="8" class="gold-trim" />
            <circle cx="-20" cy="65" r="8" class="gold-trim" />

            <!-- Head Group -->
            <g id="deputy-head-rig" transform="translate(0, -56)">
              <circle cx="0" cy="0" r="56" class="head-white" />
              <g id="deputy-tophat" transform="translate(0, -48)">
                <ellipse cx="0" cy="0" rx="80" ry="14" class="guard-dark" />
                <rect x="-48" y="-105" width="96" height="105" rx="6" class="guard-blue" />
                <rect x="-48" y="-20" width="96" height="20" fill="#facc15" stroke="#121824" stroke-width="4" />
              </g>
              <!-- Laugh squint eyes & tears -->
              <path d="M -30 -6 Q -18 -20 -6 -6" class="stroke-main" stroke-width="5" fill="none" />
              <path d="M 6 -6 Q 18 -20 30 -6" class="stroke-main" stroke-width="5" fill="none" />
              <path d="M 34 2 Q 45 18 36 30" stroke="#38bdf8" stroke-width="5" stroke-linecap="round" fill="none" />
              <!-- Laugh mouth -->
              <path d="M -24 16 Q 0 46 24 16 Z" fill="#7f1d1d" stroke="#121824" stroke-width="4" />
            </g>

            <path id="deputy-arm-left" d="M -45 35 Q -80 85 -20 110" class="stroke-main" stroke-width="14" fill="none" />
            <path id="deputy-arm-right" d="M 45 35 Q 80 85 20 110" class="stroke-main" stroke-width="14" fill="none" />
          </g>
        </g>

        <!-- ── OLD CORVIN WITH CHALK TALLY SLATE (8.2s -> 10.0s) ── -->
        <g id="corvin-tally-root" transform="translate(940, 1440)" opacity="0">
          <!-- Legs & Shoes -->
          <line x1="-20" y1="160" x2="-25" y2="300" class="stroke-main" />
          <line x1="20" y1="160" x2="25" y2="300" class="stroke-main" />
          <ellipse cx="-28" cy="315" rx="22" ry="9" class="boot-leather" />
          <ellipse cx="28" cy="315" rx="22" ry="9" class="boot-leather" />

          <!-- Corvin Body -->
          <g id="corvin-body">
            <rect x="-20" y="-25" width="40" height="35" rx="8" class="corvin-shirt" />
            <path d="M -36 0 C -42 60, -42 120, -38 160 C -15 168, 15 168, 38 160 C 42 120, 42 60, 36 0 Z" class="corvin-shirt" />
            <path d="M -26 30 L 26 30 L 32 155 L -32 155 Z" class="corvin-apron" />

            <!-- Corvin Head (Puzzled / Thinking) -->
            <g id="corvin-head" transform="translate(0, -50)">
              <circle cx="0" cy="0" r="50" class="head-white" />
              <!-- Bald hair rim -->
              <path d="M -48 -5 Q -40 -35 0 -35 Q 40 -35 48 -5" fill="none" stroke="#94a3b8" stroke-width="6" stroke-linecap="round"/>
              <!-- Confused Eyebrows (one up, one down) -->
              <path d="M -26 -22 Q -16 -30 -6 -24" class="stroke-main" stroke-width="4.5" fill="none" stroke-linecap="round"/>
              <path d="M 6 -16 Q 16 -16 26 -16" class="stroke-main" stroke-width="4.5" fill="none" stroke-linecap="round"/>
              <!-- Eyes with looking pupils -->
              <circle cx="-16" cy="-6" r="5" fill="#121824"/>
              <circle cx="16" cy="-6" r="5" fill="#121824"/>
              <circle cx="-14" cy="-8" r="2" fill="#fff"/>
              <circle cx="18" cy="-8" r="2" fill="#fff"/>
              <!-- Puzzled mouth -->
              <path d="M -14 18 Q 0 14 14 20" class="stroke-main" stroke-width="4" fill="none" stroke-linecap="round"/>
              <!-- Confusion icon floating -->
              <text x="50" y="-35" font-family="'Montserrat',sans-serif" font-weight="900" font-size="44" fill="#facc15">❓</text>
            </g>

            <!-- Holding Chalk Tally Slate -->
            <g id="tally-slate" transform="translate(-80, 40)">
              <!-- Slate wooden frame -->
              <rect x="-85" y="-55" width="170" height="110" rx="8" fill="#451a03" stroke="#121824" stroke-width="5"/>
              <!-- Blackboard slate -->
              <rect x="-75" y="-45" width="150" height="90" rx="4" fill="#1e293b" stroke="#0f172a" stroke-width="3"/>
              <!-- Chalk text on slate -->
              <text x="0" y="-18" text-anchor="middle" font-family="'Montserrat',sans-serif" font-weight="900" font-size="14" fill="#38bdf8" letter-spacing="1">LEFT SHOES</text>
              <text x="0" y="8" text-anchor="middle" font-family="'Montserrat',sans-serif" font-weight="900" font-size="24" fill="#ef4444">0 ❌</text>
              <text x="0" y="32" text-anchor="middle" font-family="'Montserrat',sans-serif" font-weight="800" font-size="12" fill="#facc15">RIGHT: 300 ✓</text>
            </g>

            <!-- Arms holding the slate -->
            <path d="M -30 25 Q -65 35 -75 40" class="stroke-main" stroke-width="12" fill="none" />
            <path d="M 30 25 Q 5 50 -10 50" class="stroke-main" stroke-width="12" fill="none" />
          </g>
        </g>
      </svg>
    </div>
  </div>

  <!-- Subtitle display box -->
  <div id="caption-box"></div>
</div>

<script>
const SUBTITLE_CHUNKS = {chunks_json};

function updateSubtitles(t) {{
  const box = document.getElementById("caption-box");
  const activeChunk = SUBTITLE_CHUNKS.find(c => t >= c.start && t < c.end);
  if (!activeChunk) {{
    box.innerHTML = "";
    return;
  }}
  let html = '<div class="caption-phrase">';
  activeChunk.words.forEach(w => {{
    const isActive = (t >= w.start && t < w.end);
    html += `<span class="word-span ${{isActive ? 'active' : ''}}">${{w.word}}</span>`;
  }});
  html += '</div>';
  box.innerHTML = html;
}}

// Master GSAP Timeline across 0.0s -> 10.0s
const masterTimeline = gsap.timeline({{ paused: true }});

// ================= SCENE 1 TIMELINE (0.0s -> 5.2s) =================
// Camera 1 slow cinematic push-in
masterTimeline.to("#camera1", {{
  scale: 1.12, x: -35, y: -45,
  duration: 5.2, ease: "sine.inOut"
}}, 0);

// Thief rope descent
masterTimeline.fromTo("#thief-dangler",
  {{ y: -200 }},
  {{ y: 760, duration: 1.8, ease: "power2.out" }},
  0
);
masterTimeline.fromTo("#thief-rope",
  {{ attr: {{ d: "M 540 0 L 540 0" }} }},
  {{ attr: {{ d: "M 540 0 L 540 760" }}, duration: 1.8, ease: "power2.out" }},
  0
);

// Thief reaching arm animation & snatching shoe
masterTimeline.to("#thief-arm", {{
  rotation: 12, transformOrigin: "0 0",
  duration: 0.8, yoyo: true, repeat: 3, ease: "sine.inOut"
}}, 1.8);

// Scarf flapping in draft
masterTimeline.to("#scarf-tail", {{
  attr: {{ d: "M 15 28 Q 45 65 35 115" }},
  duration: 0.4, yoyo: true, repeat: 10, ease: "sine.inOut"
}}, 0.5);

// ================= SCENE SWITCH AT 5.2s =================
// Cut-the-curve seamless handoff: deactivate scene 1, activate scene 2
masterTimeline.call(() => {{
  document.getElementById("scene1").classList.remove("active");
  document.getElementById("scene2").classList.add("active");
}}, null, 5.2);

// ================= SCENE 2 TIMELINE (5.2s -> 10.0s) =================
// Camera 2 slow push-in & subtle pan
masterTimeline.fromTo("#camera2",
  {{ scale: 1.0, x: 0, y: 0 }},
  {{ scale: 1.09, x: -40, y: -20, duration: 4.8, ease: "sine.inOut" }},
  5.2
);

// Guards Laughing Animation: Bouncing bodies & tilting heads
masterTimeline.to("#chief-body", {{
  y: "-=18", repeat: 12, yoyo: true, duration: 0.18, ease: "power1.inOut"
}}, 5.2);
masterTimeline.to("#chief-head-rig", {{
  rotation: 6, transformOrigin: "0 40", repeat: 12, yoyo: true, duration: 0.18, ease: "power1.inOut"
}}, 5.2);

masterTimeline.to("#deputy-body", {{
  y: "-=14", repeat: 12, yoyo: true, duration: 0.20, ease: "power1.inOut"
}}, 5.3);
masterTimeline.to("#deputy-head-rig", {{
  rotation: -6, transformOrigin: "0 40", repeat: 12, yoyo: true, duration: 0.20, ease: "power1.inOut"
}}, 5.3);

// Wanted poster subtle rustle in the breeze
masterTimeline.to("#wanted-poster-group", {{
  rotation: 2, transformOrigin: "20px 10px",
  repeat: 6, yoyo: true, duration: 0.6, ease: "sine.inOut"
}}, 5.2);

// At 8.0s: Old Corvin slides into view with his Chalk Slate
masterTimeline.to("#corvin-tally-root", {{
  opacity: 1, x: 860, duration: 0.7, ease: "power2.out"
}}, 8.0);

// Old Corvin head shake in disbelief
masterTimeline.to("#corvin-head", {{
  rotation: 5, transformOrigin: "0 30",
  repeat: 4, yoyo: true, duration: 0.35, ease: "sine.inOut"
}}, 8.5);

// Deterministic seek function for renderers
window.seekToTime = function(t) {{
  if (t < 5.2) {{
    document.getElementById("scene1").classList.add("active");
    document.getElementById("scene2").classList.remove("active");
  }} else {{
    document.getElementById("scene1").classList.remove("active");
    document.getElementById("scene2").classList.add("active");
  }}
  masterTimeline.seek(t, false);
  updateSubtitles(t);
}};

// Initialize at t=0
window.seekToTime(0);
</script>
</body>
</html>
'''

output_path = PROJECT / "demo_10s_character.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated {output_path} ({len(html_content)} bytes)")

