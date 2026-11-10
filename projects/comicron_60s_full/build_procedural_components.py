import json
from pathlib import Path

PROJECT = Path(r"c:\Users\iamra\OneDrive\Desktop\stick_man\projects\comicron_60s_full")
chunks = json.load(open(PROJECT / "subtitle_chunks.json", encoding="utf-8"))

# We construct procedural SVG backgrounds for each scene:
# 1. BG_WORKSHOP_NIGHT (Scenes 1, 4, 7)
# 2. BG_MEDIEVAL_STREET_DAY (Scene 2)
# 3. BG_SHOP_WINDOW (Scene 3)
# 4. BG_HOPPING_STREET (Scene 5)
# 5. BG_WINTER_STREET (Scene 6)
# 6. BG_GRAND_BOUTIQUE (Scene 8)

bg_workshop_defs = '''
    <defs>
      <linearGradient id="wallGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#080502"/>
        <stop offset="45%" stop-color="#150f08"/>
        <stop offset="100%" stop-color="#201510"/>
      </linearGradient>
      <linearGradient id="floorGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#1a0e06"/>
        <stop offset="100%" stop-color="#4a2a0e"/>
      </linearGradient>
      <linearGradient id="ceilGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#030201"/>
        <stop offset="100%" stop-color="#0d0905"/>
      </linearGradient>
      <radialGradient id="lanternCone" cx="0.5" cy="0" r="1">
        <stop offset="0%" stop-color="#ffe87a" stop-opacity="0.9"/>
        <stop offset="18%" stop-color="#ff9500" stop-opacity="0.5"/>
        <stop offset="55%" stop-color="#cc4400" stop-opacity="0.18"/>
        <stop offset="100%" stop-color="#440000" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="emberGlow" cx="0.5" cy="0.9" r="0.8">
        <stop offset="0%" stop-color="#ff7700" stop-opacity="0.95"/>
        <stop offset="35%" stop-color="#ff3300" stop-opacity="0.7"/>
        <stop offset="100%" stop-color="#8b0000" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="fireAmbient" cx="0.85" cy="0.7" r="0.9">
        <stop offset="0%" stop-color="#ff6600" stop-opacity="0.28"/>
        <stop offset="100%" stop-color="#440000" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="moonRay" cx="0.5" cy="0" r="1.1">
        <stop offset="0%" stop-color="#c8d8f5" stop-opacity="0.9"/>
        <stop offset="40%" stop-color="#8ba8d8" stop-opacity="0.5"/>
        <stop offset="100%" stop-color="#1a2a4a" stop-opacity="0"/>
      </radialGradient>
      <linearGradient id="tableTopGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#6b3f1f"/>
        <stop offset="100%" stop-color="#3d2210"/>
      </linearGradient>
      <linearGradient id="tableSideGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#2e1508"/>
        <stop offset="100%" stop-color="#180a04"/>
      </linearGradient>
      <linearGradient id="marbleFloor" x1="0" y1="0" x2="0.5" y2="1">
        <stop offset="0%" stop-color="#2a1a0a"/>
        <stop offset="100%" stop-color="#5c3317"/>
      </linearGradient>
      <pattern id="stoneWall" x="0" y="0" width="140" height="68" patternUnits="userSpaceOnUse">
        <rect width="140" height="68" fill="#18120b"/>
        <rect x="2" y="2" width="136" height="30" rx="2" fill="#201810" stroke="#0e0906" stroke-width="1.5"/>
        <rect x="2" y="36" width="66" height="30" rx="2" fill="#1e1510" stroke="#0e0906" stroke-width="1.5"/>
        <rect x="72" y="36" width="66" height="30" rx="2" fill="#241a0e" stroke="#0e0906" stroke-width="1.5"/>
        <line x1="40" y1="2" x2="38" y2="32" stroke="#0a0705" stroke-width="0.5" opacity="0.7"/>
        <line x1="100" y1="2" x2="102" y2="32" stroke="#0a0705" stroke-width="0.4" opacity="0.5"/>
        <line x1="30" y1="36" x2="28" y2="66" stroke="#0a0705" stroke-width="0.4" opacity="0.5"/>
      </pattern>
      <pattern id="woodFloor" x="0" y="0" width="80" height="12" patternUnits="userSpaceOnUse">
        <rect width="80" height="12" fill="#3d2210"/>
        <rect x="0" y="0" width="80" height="11" fill="#422510" stroke="#2a1508" stroke-width="1"/>
        <line x1="0" y1="4" x2="80" y2="4" stroke="#311a08" stroke-width="0.5" opacity="0.4"/>
      </pattern>
      <filter id="blur2"><feGaussianBlur stdDeviation="2"/></filter>
      <filter id="blur4"><feGaussianBlur stdDeviation="4"/></filter>
      <filter id="blur10"><feGaussianBlur stdDeviation="10"/></filter>
      <filter id="blur20"><feGaussianBlur stdDeviation="20"/></filter>
      <filter id="glow">
        <feGaussianBlur stdDeviation="10" result="blur"/>
        <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
    </defs>
'''

bg_workshop_content = '''
    <!-- Ceiling -->
    <rect x="0" y="0" width="1080" height="260" fill="url(#ceilGrad)"/>
    <rect x="0" y="210" width="1080" height="32" fill="#120e08" opacity="0.95"/>
    <line x1="0" y1="60" x2="1080" y2="60" stroke="#0e0a06" stroke-width="1.5" opacity="0.5"/>
    <line x1="0" y1="120" x2="1080" y2="120" stroke="#0e0a06" stroke-width="1.5" opacity="0.5"/>

    <!-- Stone Back Wall -->
    <rect x="0" y="242" width="1080" height="1000" fill="url(#wallGrad)"/>
    <rect x="0" y="242" width="1080" height="1000" fill="url(#stoneWall)" opacity="0.6"/>

    <!-- Timber Framing -->
    <rect x="0" y="242" width="20" height="1000" fill="#120d07" opacity="0.9"/>
    <rect x="40" y="242" width="12" height="1000" fill="#1a1008" opacity="0.7"/>
    <rect x="440" y="242" width="16" height="600" fill="#1a1008" opacity="0.6"/>
    <rect x="1058" y="242" width="22" height="1000" fill="#120d07" opacity="0.9"/>
    <rect x="0" y="600" width="1080" height="22" fill="#150f07" opacity="0.85"/>
    <polygon points="0,620 180,760 180,782 0,642" fill="#120d06" opacity="0.8"/>

    <!-- Arched Window with Moonlight -->
    <path d="M110,185 Q110,100 220,100 Q330,100 330,185 L330,490 L110,490 Z" fill="#28190e" stroke="#0e0906" stroke-width="8"/>
    <path d="M120,195 Q120,110 220,110 Q320,110 320,195 L320,480 L120,480 Z" fill="url(#moonRay)"/>
    <line x1="220" y1="110" x2="220" y2="480" stroke="#28190e" stroke-width="10"/>
    <line x1="120" y1="310" x2="320" y2="310" stroke="#28190e" stroke-width="10"/>
    <rect x="100" y="480" width="240" height="22" rx="4" fill="#2e1e10"/>
    <polygon points="110,490 330,490 580,1920 -120,1920" fill="url(#moonRay)" opacity="0.14" filter="url(#blur4)"/>
    <circle cx="220" cy="80" r="55" fill="#c8d8f5" opacity="0.5" filter="url(#blur10)"/>

    <!-- Stone Fireplace with Flames -->
    <path d="M700,870 Q700,800 820,800 Q940,800 940,870 L940,1130 L700,1130 Z" fill="#2a1a0c" stroke="#150e07" stroke-width="6"/>
    <rect x="680" y="790" width="280" height="28" rx="4" fill="#3a2415"/>
    <rect x="664" y="770" width="312" height="24" rx="3" fill="#44301a"/>
    <path d="M720,878 Q720,840 820,840 Q920,840 920,878 L920,1120 L720,1120 Z" fill="#0a0704"/>
    <ellipse cx="820" cy="1095" rx="130" ry="28" fill="url(#emberGlow)" filter="url(#blur4)"/>
    <path id="flame-shop" d="M760,1095 Q768,1040 785,1055 Q793,1010 820,1030 Q840,990 848,1048 Q865,1025 872,1080 Q855,1058 843,1085 Q820,1050 800,1082 Q778,1058 760,1095Z" fill="#ff7700" opacity="0.92" filter="url(#glow)"/>
    <path id="flame-inner" d="M790,1092 Q796,1052 810,1065 Q820,1035 832,1058 Q845,1038 848,1078 Q835,1062 820,1080 Q806,1065 790,1092Z" fill="#ffdd00" opacity="0.85"/>
    <rect x="0" y="600" width="1080" height="1320" fill="url(#fireAmbient)"/>

    <!-- Perspective Floor -->
    <polygon points="0,1920 1080,1920 870,1242 210,1242" fill="url(#marbleFloor)"/>
    <polygon points="0,1920 1080,1920 870,1242 210,1242" fill="url(#woodFloor)" opacity="0.65"/>
    <line x1="0" y1="1600" x2="1080" y2="1600" stroke="#1a0d05" stroke-width="3" opacity="0.45"/>
    <line x1="0" y1="1420" x2="1080" y2="1420" stroke="#1a0d05" stroke-width="2.5" opacity="0.4"/>
    <line x1="540" y1="1242" x2="0" y2="1920" stroke="#120a04" stroke-width="2.5" opacity="0.4"/>
    <line x1="540" y1="1242" x2="540" y2="1920" stroke="#120a04" stroke-width="2" opacity="0.3"/>
    <line x1="540" y1="1242" x2="1080" y2="1920" stroke="#120a04" stroke-width="2.5" opacity="0.4"/>
    <rect x="0" y="1230" width="1080" height="16" fill="#180f07" opacity="0.8"/>

    <!-- Hanging Lantern -->
    <line x1="540" y1="0" x2="540" y2="195" stroke="#5a4210" stroke-width="5" opacity="0.9"/>
    <rect x="514" y="212" width="52" height="80" rx="6" fill="#8b6914" stroke="#5a4209" stroke-width="4"/>
    <rect x="520" y="218" width="16" height="68" rx="3" fill="#ffe87a" opacity="0.88" filter="url(#blur2)"/>
    <rect x="540" y="218" width="12" height="68" rx="3" fill="#ffdd55" opacity="0.75" filter="url(#blur2)"/>
    <polygon points="420,308 660,308 940,1920 140,1920" fill="url(#lanternCone)" opacity="0.4"/>

    <!-- Bookshelves on Left Wall -->
    <rect x="52" y="474" width="310" height="18" rx="3" fill="#3d2210" stroke="#2a1508" stroke-width="2"/>
    <rect x="66" y="420" width="32" height="54" rx="2" fill="#8b2020" stroke="#5a1010" stroke-width="1.5"/>
    <rect x="102" y="430" width="28" height="44" rx="2" fill="#1a4a2a" stroke="#0e3018" stroke-width="1.5"/>
    <rect x="134" y="435" width="26" height="39" rx="2" fill="#3a2a7a" stroke="#26198a" stroke-width="1.5" transform="rotate(-4,147,455)"/>
    <rect x="210" y="435" width="22" height="28" rx="8" fill="#1a3a1a" opacity="0.92"/>
    <ellipse cx="221" cy="453" rx="9" ry="10" fill="#00ff88" opacity="0.35" filter="url(#glow)"/>

    <rect x="52" y="668" width="310" height="18" rx="3" fill="#3d2210" stroke="#2a1508" stroke-width="2"/>
    <rect x="72" y="630" width="10" height="38" rx="2" fill="#6b4a1a" stroke="#3a2008" stroke-width="1.5"/>
    <rect x="62" y="624" width="30" height="14" rx="3" fill="#5a5a5a" stroke="#2a2a2a" stroke-width="1.5"/>
    <rect x="230" y="635" width="16" height="30" rx="2" fill="#f5e6c8" stroke="#c8b490" stroke-width="1.5"/>
    <path id="candle-flame" d="M235,618 Q232,606 238,600 Q244,606 241,618 Z" fill="#ff9900" opacity="0.9" filter="url(#glow)"/>

    <!-- Workbench Table -->
    <polygon points="80,1500 1000,1500 960,1428 120,1428" fill="url(#tableTopGrad)"/>
    <rect x="80" y="1500" width="920" height="45" fill="url(#tableSideGrad)"/>
    <rect x="100" y="1545" width="38" height="280" rx="4" fill="#281408"/>
    <rect x="942" y="1545" width="38" height="280" rx="4" fill="#281408"/>
    <line x1="200" y1="1428" x2="180" y2="1500" stroke="#5a3015" stroke-width="1.2" opacity="0.35"/>
    <line x1="560" y1="1428" x2="540" y2="1500" stroke="#5a3015" stroke-width="1.2" opacity="0.35"/>
    <line x1="880" y1="1428" x2="860" y2="1500" stroke="#5a3015" stroke-width="1" opacity="0.3"/>

    <!-- Cobbler Table Props -->
    <g transform="translate(650, 1400) rotate(-8)">
      <ellipse cx="0" cy="20" rx="58" ry="13" fill="#1a0e06" opacity="0.6"/>
      <path d="M-58,10 Q-52,-28 -8,-30 Q22,-32 50,-16 Q60,0 55,10 Z" fill="#78350f" stroke="#3a1a06" stroke-width="2.5"/>
      <path d="M-58,10 Q-58,-6 -32,-10 Q-10,-13 10,-6 Q-10,5 -32,8 Z" fill="#8b4515"/>
    </g>
    <rect x="420" y="1400" width="8" height="28" rx="2" fill="#7b5a1a"/>
    <path d="M220,1415 Q260,1408 310,1418 Q320,1430 300,1440 Q255,1448 215,1435 Z" fill="#5a3010" opacity="0.85"/>
'''

# 2. Medieval Street Background (Scene 2 & Scene 5 base)
bg_street_defs = '''
    <defs>
      <linearGradient id="skyGradDay" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#1e3a8a"/>
        <stop offset="30%" stop-color="#3b82f6"/>
        <stop offset="65%" stop-color="#93c5fd"/>
        <stop offset="100%" stop-color="#fef08a"/>
      </linearGradient>
      <linearGradient id="roofGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#7f1d1d"/>
        <stop offset="100%" stop-color="#991b1b"/>
      </linearGradient>
      <linearGradient id="housePlaster" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#f1f5f9"/>
        <stop offset="100%" stop-color="#cbd5e1"/>
      </linearGradient>
      <pattern id="streetCobble" x="0" y="0" width="60" height="40" patternUnits="userSpaceOnUse">
        <rect width="60" height="40" fill="#475569"/>
        <rect x="2" y="2" width="26" height="16" rx="3" fill="#64748b" stroke="#334155" stroke-width="1.5"/>
        <rect x="32" y="2" width="26" height="16" rx="3" fill="#526071" stroke="#334155" stroke-width="1.5"/>
        <rect x="2" y="22" width="16" height="16" rx="3" fill="#596879" stroke="#334155" stroke-width="1.5"/>
        <rect x="22" y="22" width="22" height="16" rx="3" fill="#64748b" stroke="#334155" stroke-width="1.5"/>
        <rect x="48" y="22" width="10" height="16" rx="3" fill="#526071" stroke="#334155" stroke-width="1.5"/>
      </pattern>
      <radialGradient id="sunGlow" cx="0.5" cy="0.5" r="0.5">
        <stop offset="0%" stop-color="#fffbeb" stop-opacity="0.8"/>
        <stop offset="40%" stop-color="#fef08a" stop-opacity="0.3"/>
        <stop offset="100%" stop-color="#fef08a" stop-opacity="0"/>
      </radialGradient>
    </defs>
'''

bg_street_content = '''
    <!-- Sunny Sky -->
    <rect x="0" y="0" width="1080" height="1200" fill="url(#skyGradDay)"/>
    <circle cx="820" cy="220" r="140" fill="url(#sunGlow)"/>
    <circle cx="820" cy="220" r="45" fill="#fffef0"/>

    <!-- Distant Castle & Village Silhouettes -->
    <polygon points="120,700 160,540 200,700" fill="#475569" opacity="0.35"/>
    <polygon points="170,720 220,510 270,720" fill="#475569" opacity="0.4"/>
    <rect x="185" y="470" width="70" height="180" fill="#475569" opacity="0.4"/>
    <polygon points="180,470 220,380 260,470" fill="#334155" opacity="0.45"/>
    <polygon points="780,720 840,490 900,720" fill="#475569" opacity="0.35"/>

    <!-- Left Medieval Timber House -->
    <polygon points="-40,1400 380,1400 350,560 -40,520" fill="url(#housePlaster)"/>
    <polygon points="-50,530 180,240 370,570" fill="url(#roofGrad)" stroke="#450a0a" stroke-width="6"/>
    <!-- Timber Beams (Left House) -->
    <rect x="340" y="560" width="24" height="840" fill="#2d1a0e"/>
    <rect x="160" y="560" width="20" height="840" fill="#2d1a0e"/>
    <line x1="-40" y1="920" x2="360" y2="920" stroke="#2d1a0e" stroke-width="20"/>
    <line x1="-40" y1="1160" x2="360" y2="1160" stroke="#2d1a0e" stroke-width="18"/>
    <!-- Cross Braces -->
    <line x1="0" y1="560" x2="160" y2="920" stroke="#2d1a0e" stroke-width="14"/>
    <line x1="160" y1="560" x2="0" y2="920" stroke="#2d1a0e" stroke-width="14"/>
    <line x1="180" y1="560" x2="340" y2="920" stroke="#2d1a0e" stroke-width="14"/>
    <line x1="340" y1="560" x2="180" y2="920" stroke="#2d1a0e" stroke-width="14"/>
    <!-- Upper Window -->
    <rect x="50" y="660" width="80" height="110" rx="4" fill="#0f172a" stroke="#2d1a0e" stroke-width="8"/>
    <line x1="90" y1="660" x2="90" y2="770" stroke="#2d1a0e" stroke-width="5"/>
    <line x1="50" y1="715" x2="130" y2="715" stroke="#2d1a0e" stroke-width="5"/>
    <!-- Flower Box -->
    <rect x="42" y="770" width="96" height="24" rx="3" fill="#854d0e"/>
    <circle cx="60" cy="766" r="8" fill="#ef4444"/>
    <circle cx="75" cy="764" r="9" fill="#facc15"/>
    <circle cx="95" cy="766" r="8" fill="#ec4899"/>
    <circle cx="115" cy="764" r="8" fill="#3b82f6"/>
    <!-- Arched Wooden Door -->
    <path d="M60,1160 Q60,1050 140,1050 Q220,1050 220,1160 L220,1400 L60,1400 Z" fill="#3b2011" stroke="#1c0f08" stroke-width="8"/>
    <circle cx="85" cy="1240" r="6" fill="#facc15"/>

    <!-- Right Medieval House / Tavern -->
    <polygon points="720,1400 1120,1400 1120,480 730,580" fill="#fef3c7"/>
    <polygon points="710,590 920,290 1130,490" fill="#991b1b" stroke="#450a0a" stroke-width="6"/>
    <!-- Timber Beams (Right) -->
    <rect x="730" y="580" width="22" height="820" fill="#2d1a0e"/>
    <line x1="730" y1="940" x2="1120" y2="940" stroke="#2d1a0e" stroke-width="20"/>
    <line x1="730" y1="600" x2="940" y2="940" stroke="#2d1a0e" stroke-width="14"/>
    <line x1="940" y1="600" x2="730" y2="940" stroke="#2d1a0e" stroke-width="14"/>
    <!-- Hanging Tavern Sign -->
    <line x1="720" y1="780" x2="640" y2="780" stroke="#1e293b" stroke-width="8"/>
    <line x1="640" y1="780" x2="720" y2="720" stroke="#1e293b" stroke-width="6"/>
    <rect x="620" y="795" width="85" height="100" rx="8" fill="#78350f" stroke="#3b1d08" stroke-width="6"/>
    <text x="662" y="845" font-family="'Montserrat', sans-serif" font-weight="900" font-size="28" fill="#facc15" text-anchor="middle">ALE</text>
    <path d="M648,860 L678,860 L674,882 L652,882 Z" fill="#fef08a"/>

    <!-- Street Cobblestone Perspective Floor -->
    <polygon points="0,1920 1080,1920 820,1260 260,1260" fill="url(#streetCobble)"/>
    <line x1="260" y1="1260" x2="820" y2="1260" stroke="#1e293b" stroke-width="8"/>
    <line x1="0" y1="1920" x2="260" y2="1260" stroke="#1e293b" stroke-width="5"/>
    <line x1="1080" y1="1920" x2="820" y2="1260" stroke="#1e293b" stroke-width="5"/>
    <line x1="0" y1="1620" x2="1080" y2="1620" stroke="#334155" stroke-width="3" opacity="0.6"/>
    <line x1="0" y1="1440" x2="1080" y2="1440" stroke="#334155" stroke-width="2" opacity="0.5"/>

    <!-- Street Barrels & Props -->
    <!-- Notice Board: WANTED ONE-LEGGED THIEF -->
    <g transform="translate(190, 880)">
      <rect x="0" y="0" width="130" height="150" rx="6" fill="#854d0e" stroke="#3b1d08" stroke-width="4"/>
      <rect x="10" y="10" width="110" height="130" fill="#fef3c7" stroke="#b45309" stroke-width="2"/>
      <text x="65" y="32" font-family="'Montserrat', sans-serif" font-weight="900" font-size="14" fill="#991b1b" text-anchor="middle">WANTED</text>
      <text x="65" y="48" font-family="'Montserrat', sans-serif" font-weight="800" font-size="10" fill="#1e293b" text-anchor="middle">ONE-LEGGED THIEF</text>
      <!-- One-legged stickman sketch -->
      <circle cx="65" cy="72" r="12" fill="none" stroke="#1e293b" stroke-width="3"/>
      <line x1="65" y1="84" x2="65" y2="112" stroke="#1e293b" stroke-width="3"/>
      <line x1="65" y1="92" x2="48" y2="105" stroke="#1e293b" stroke-width="3"/>
      <line x1="65" y1="92" x2="82" y2="105" stroke="#1e293b" stroke-width="3"/>
      <!-- Only one leg! -->
      <line x1="65" y1="112" x2="65" y2="132" stroke="#1e293b" stroke-width="4"/>
      <ellipse cx="68" cy="132" rx="7" ry="4" fill="#78350f"/>
    </g>

    <g transform="translate(820, 1340)">
      <ellipse cx="0" cy="50" rx="35" ry="14" fill="rgba(15,23,42,0.4)"/>
      <rect x="-30" y="-35" width="60" height="80" rx="16" fill="#78350f" stroke="#3b1d08" stroke-width="4"/>
      <line x1="-30" y1="-10" x2="30" y2="-10" stroke="#1e293b" stroke-width="5"/>
      <line x1="-30" y1="20" x2="30" y2="20" stroke="#1e293b" stroke-width="5"/>
    </g>
    <g transform="translate(875, 1370)">
      <ellipse cx="0" cy="40" rx="28" ry="12" fill="rgba(15,23,42,0.4)"/>
      <rect x="-24" y="-30" width="48" height="65" rx="12" fill="#854d0e" stroke="#3b1d08" stroke-width="4"/>
      <line x1="-24" y1="-8" x2="24" y2="-8" stroke="#1e293b" stroke-width="4"/>
      <line x1="-24" y1="16" x2="24" y2="16" stroke="#1e293b" stroke-width="4"/>
    </g>
'''

# 3. Shop Window Background (Scene 3)
bg_window_defs = '''
    <defs>
      <linearGradient id="shopWood" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#451a03"/>
        <stop offset="50%" stop-color="#78350f"/>
        <stop offset="100%" stop-color="#2d1203"/>
      </linearGradient>
      <linearGradient id="glassGlow" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#fef08a" stop-opacity="0.85"/>
        <stop offset="45%" stop-color="#fef9c3" stop-opacity="0.6"/>
        <stop offset="85%" stop-color="#fed7aa" stop-opacity="0.75"/>
      </linearGradient>
      <linearGradient id="glassSheen" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#ffffff" stop-opacity="0.4"/>
        <stop offset="25%" stop-color="#ffffff" stop-opacity="0.05"/>
        <stop offset="50%" stop-color="#ffffff" stop-opacity="0.25"/>
        <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
      </linearGradient>
      <pattern id="stoneFacade" x="0" y="0" width="120" height="60" patternUnits="userSpaceOnUse">
        <rect width="120" height="60" fill="#334155"/>
        <rect x="2" y="2" width="116" height="26" rx="3" fill="#475569" stroke="#1e293b" stroke-width="1.5"/>
        <rect x="2" y="32" width="56" height="26" rx="3" fill="#3f4e62" stroke="#1e293b" stroke-width="1.5"/>
        <rect x="62" y="32" width="56" height="26" rx="3" fill="#4a5b71" stroke="#1e293b" stroke-width="1.5"/>
      </pattern>
    </defs>
'''

bg_window_content = '''
    <!-- Stone Facade Wall -->
    <rect x="0" y="0" width="1080" height="1920" fill="url(#stoneFacade)"/>

    <!-- Shop Front Timber Cornice & Header -->
    <rect x="0" y="180" width="1080" height="150" fill="url(#shopWood)"/>
    <rect x="0" y="160" width="1080" height="30" fill="#2d1203"/>
    <rect x="0" y="320" width="1080" height="20" fill="#2d1203"/>

    <!-- Shop Signboard Carved Header -->
    <rect x="80" y="195" width="920" height="115" rx="10" fill="#1e1b18" stroke="#ca8a04" stroke-width="6"/>
    <text x="540" y="250" font-family="'Montserrat', sans-serif" font-weight="900" font-size="44" fill="#facc15" text-anchor="middle" letter-spacing="4">CORVIN'S BOOTERY</text>
    <text x="540" y="288" font-family="'Montserrat', sans-serif" font-weight="800" font-size="22" fill="#cbd5e1" text-anchor="middle" letter-spacing="3">FINE HANDCRAFTED FOOTWEAR • EST. 1842</text>

    <!-- Side Timber Pilasters -->
    <rect x="40" y="330" width="70" height="1150" fill="url(#shopWood)" stroke="#1e0c02" stroke-width="4"/>
    <rect x="970" y="330" width="70" height="1150" fill="url(#shopWood)" stroke="#1e0c02" stroke-width="4"/>

    <!-- Grand Multi-Pane Display Window -->
    <rect x="110" y="340" width="860" height="1080" fill="url(#glassGlow)" stroke="#3b1d08" stroke-width="12"/>
    <!-- Window Shelves inside Shop -->
    <rect x="110" y="680" width="860" height="24" fill="#5c2e0b"/>
    <rect x="110" y="1000" width="860" height="24" fill="#5c2e0b"/>

    <!-- Right Shoes on Display Shelves Inside Window -->
    <g transform="translate(240, 660)">
      <ellipse cx="0" cy="18" rx="42" ry="10" fill="rgba(15,23,42,0.4)"/>
      <path d="M-40,8 Q-35,-18 -5,-20 Q15,-22 35,-12 Q42,0 38,8 Z" fill="#78350f" stroke="#3b1d08" stroke-width="2"/>
    </g>
    <g transform="translate(480, 660)">
      <ellipse cx="0" cy="18" rx="42" ry="10" fill="rgba(15,23,42,0.4)"/>
      <path d="M-40,8 Q-35,-18 -5,-20 Q15,-22 35,-12 Q42,0 38,8 Z" fill="#991b1b" stroke="#3b1d08" stroke-width="2"/>
    </g>
    <g transform="translate(740, 660)">
      <ellipse cx="0" cy="18" rx="42" ry="10" fill="rgba(15,23,42,0.4)"/>
      <path d="M-40,8 Q-35,-18 -5,-20 Q15,-22 35,-12 Q42,0 38,8 Z" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
    </g>
    <!-- Single lone right boot on lower shelf -->
    <g transform="translate(280, 980)">
      <ellipse cx="0" cy="18" rx="45" ry="10" fill="rgba(15,23,42,0.4)"/>
      <path d="M-45,8 Q-40,-24 -5,-25 Q18,-26 40,-14 Q48,0 42,8 Z" fill="#b45309" stroke="#451a03" stroke-width="2"/>
    </g>

    <!-- Window Timber Mullions (Grid Bars) -->
    <line x1="396" y1="340" x2="396" y2="1420" stroke="#3b1d08" stroke-width="14"/>
    <line x1="682" y1="340" x2="682" y2="1420" stroke="#3b1d08" stroke-width="14"/>
    <!-- Diagonal Glass Sheen Reflection -->
    <polygon points="110,340 380,340 180,1420 110,1420" fill="url(#glassSheen)"/>
    <polygon points="460,340 680,340 500,1420 280,1420" fill="url(#glassSheen)" opacity="0.6"/>

    <!-- Bottom Stallboard / Window Sill -->
    <rect x="0" y="1420" width="1080" height="70" fill="url(#shopWood)" stroke="#1e0c02" stroke-width="6"/>
    <!-- Cobblestone Pavement below sill -->
    <polygon points="0,1920 1080,1920 1080,1490 0,1490" fill="url(#stoneFacade)"/>
    <line x1="0" y1="1650" x2="1080" y2="1650" stroke="#1e293b" stroke-width="4"/>
    <line x1="0" y1="1800" x2="1080" y2="1800" stroke="#1e293b" stroke-width="4"/>
'''

# 4. Winter Street Background (Scene 6)
bg_winter_defs = '''
    <defs>
      <linearGradient id="winterSky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#020617"/>
        <stop offset="40%" stop-color="#0f172a"/>
        <stop offset="80%" stop-color="#1e293b"/>
        <stop offset="100%" stop-color="#334155"/>
      </linearGradient>
      <linearGradient id="snowGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#e2e8f0"/>
        <stop offset="60%" stop-color="#f8fafc"/>
        <stop offset="100%" stop-color="#cbd5e1"/>
      </linearGradient>
      <radialGradient id="frostGlow" cx="0.5" cy="0.5" r="0.8">
        <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.2"/>
        <stop offset="100%" stop-color="#020617" stop-opacity="0.8"/>
      </radialGradient>
    </defs>
'''

bg_winter_content = '''
    <!-- Cold Dark Winter Sky -->
    <rect x="0" y="0" width="1080" height="1920" fill="url(#winterSky)"/>

    <!-- Frosty Moon through blizzard -->
    <circle cx="540" cy="300" r="100" fill="#e0f2fe" opacity="0.3" filter="url(#blur20)"/>
    <circle cx="540" cy="300" r="40" fill="#f8fafc" opacity="0.7"/>

    <!-- Silhouetted Winter Buildings with Snow Roofs -->
    <polygon points="-40,1400 360,1400 340,620 -40,580" fill="#0f172a"/>
    <polygon points="-50,590 160,340 350,630" fill="#1e293b"/>
    <!-- Thick Snow on Roof -->
    <path d="M -60 590 Q 0 540 160 330 Q 320 540 360 630 Q 320 610 260 625 Q 160 580 80 610 Z" fill="url(#snowGrad)"/>

    <polygon points="720,1400 1120,1400 1120,540 730,640" fill="#0f172a"/>
    <polygon points="710,650 930,380 1130,550" fill="#1e293b"/>
    <path d="M 700 650 Q 820 560 930 370 Q 1040 500 1140 550 Q 1060 530 960 560 Q 840 570 700 650 Z" fill="url(#snowGrad)"/>

    <!-- Bare Gnarly Winter Trees -->
    <path d="M 220 1400 L 235 900 Q 240 820 280 750 M 235 850 Q 180 800 140 730 M 235 800 Q 210 740 190 680 M 280 750 Q 320 700 350 640" stroke="#1e293b" stroke-width="12" stroke-linecap="round" fill="none"/>
    <path d="M 860 1400 L 845 880 Q 840 790 790 720 M 845 830 Q 900 780 940 710 M 790 720 Q 750 670 730 600" stroke="#1e293b" stroke-width="12" stroke-linecap="round" fill="none"/>

    <!-- Deep Snow Ground -->
    <polygon points="0,1920 1080,1920 1080,1280 0,1280" fill="url(#snowGrad)"/>
    <!-- Shelves of useless right shoes covered in cobwebs behind Corvin -->
    <g transform="translate(180, 1020)">
      <rect x="0" y="0" width="720" height="18" rx="3" fill="#334155" stroke="#1e293b" stroke-width="2"/>
      <rect x="0" y="80" width="720" height="18" rx="3" fill="#334155" stroke="#1e293b" stroke-width="2"/>
      <!-- Rows of single shoes on shelf -->
      <path d="M 40 -4 Q 55 -24 75 -24 Q 90 -24 100 -12 L 105 -4 Z" fill="#64748b" opacity="0.8"/>
      <path d="M 140 -4 Q 155 -24 175 -24 Q 190 -24 200 -12 L 205 -4 Z" fill="#64748b" opacity="0.8"/>
      <path d="M 240 -4 Q 255 -24 275 -24 Q 290 -24 300 -12 L 305 -4 Z" fill="#64748b" opacity="0.8"/>
      <path d="M 440 -4 Q 455 -24 475 -24 Q 490 -24 500 -12 L 505 -4 Z" fill="#64748b" opacity="0.8"/>
      <path d="M 540 -4 Q 555 -24 575 -24 Q 590 -24 600 -12 L 605 -4 Z" fill="#64748b" opacity="0.8"/>
      <!-- Cobwebs -->
      <path d="M 0 0 Q 35 35 70 0 M 10 0 Q 35 20 60 0 M 35 0 L 35 25" stroke="#94a3b8" stroke-width="1.5" fill="none" opacity="0.6"/>
      <path d="M 650 0 Q 685 35 720 0 M 660 0 Q 685 20 710 0 M 685 0 L 685 25" stroke="#94a3b8" stroke-width="1.5" fill="none" opacity="0.6"/>
    </g>

    <!-- Soft Snow Mounds -->
    <path d="M 0 1340 Q 240 1260 540 1310 Q 840 1260 1080 1330 L 1080 1920 L 0 1920 Z" fill="#f8fafc"/>
    <path d="M 0 1460 Q 360 1390 720 1440 Q 920 1410 1080 1450 L 1080 1920 L 0 1920 Z" fill="#ffffff"/>

    <!-- Shivering Corvin's footprints in snow -->
    <ellipse cx="440" cy="1720" rx="22" ry="9" fill="#94a3b8" opacity="0.6"/>
    <ellipse cx="500" cy="1740" rx="22" ry="9" fill="#94a3b8" opacity="0.6"/>
    <ellipse cx="460" cy="1760" rx="22" ry="9" fill="#94a3b8" opacity="0.6"/>

    <!-- Frost Vignette Edge -->
    <rect x="0" y="0" width="1080" height="1920" fill="url(#frostGlow)" pointer-events="none"/>
'''

# 5. Grand Luxury Boutique Background (Scene 8)
bg_boutique_defs = '''
    <defs>
      <linearGradient id="boutiqueWall" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#18181b"/>
        <stop offset="40%" stop-color="#27272a"/>
        <stop offset="100%" stop-color="#3f3f46"/>
      </linearGradient>
      <linearGradient id="velvetRed" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#4c0519"/>
        <stop offset="60%" stop-color="#881337"/>
        <stop offset="100%" stop-color="#9f1239"/>
      </linearGradient>
      <linearGradient id="goldLuster" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#ca8a04"/>
        <stop offset="35%" stop-color="#fde047"/>
        <stop offset="70%" stop-color="#eab308"/>
        <stop offset="100%" stop-color="#a16207"/>
      </linearGradient>
      <linearGradient id="marbleTile" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#09090b"/>
        <stop offset="100%" stop-color="#18181b"/>
      </linearGradient>
      <pattern id="boutiqueCheckers" x="0" y="0" width="120" height="60" patternUnits="userSpaceOnUse">
        <rect width="120" height="60" fill="#09090b"/>
        <polygon points="0,0 60,0 0,60" fill="#27272a"/>
        <polygon points="60,0 120,0 120,60 60,60" fill="#27272a"/>
        <line x1="0" y1="0" x2="120" y2="60" stroke="#ca8a04" stroke-width="0.8" opacity="0.4"/>
      </pattern>
      <radialGradient id="chandelierGlow" cx="0.5" cy="0.5" r="0.5">
        <stop offset="0%" stop-color="#fef08a" stop-opacity="0.9"/>
        <stop offset="45%" stop-color="#facc15" stop-opacity="0.4"/>
        <stop offset="100%" stop-color="#ca8a04" stop-opacity="0"/>
      </radialGradient>
    </defs>
'''

bg_boutique_content = '''
    <!-- Back Wall: Royal Boutique Interior -->
    <rect x="0" y="0" width="1080" height="1350" fill="url(#boutiqueWall)"/>

    <!-- High Neoclassical Crown Molding & Gold Cornice -->
    <rect x="0" y="140" width="1080" height="32" fill="url(#goldLuster)"/>
    <rect x="0" y="172" width="1080" height="12" fill="#713f12"/>

    <!-- Left Arched Vitrine (Luxury Display Case) -->
    <path d="M100,260 Q100,180 240,180 Q380,180 380,260 L380,1180 L100,1180 Z" fill="url(#velvetRed)" stroke="url(#goldLuster)" stroke-width="14"/>
    <rect x="120" y="520" width="240" height="16" rx="4" fill="url(#goldLuster)"/>
    <rect x="120" y="800" width="240" height="16" rx="4" fill="url(#goldLuster)"/>

    <!-- Shoes in Left Vitrine -->
    <g transform="translate(240, 500)">
      <ellipse cx="0" cy="14" rx="38" ry="8" fill="rgba(0,0,0,0.5)"/>
      <path d="M-35,6 Q-30,-16 -5,-18 Q15,-20 32,-10 Q38,0 35,6 Z" fill="#0f172a" stroke="url(#goldLuster)" stroke-width="2"/>
      <!-- Matching left boot -->
      <path d="M-15,6 Q-10,-14 15,-16 Q32,-18 48,-8 Q54,2 50,6 Z" fill="#0f172a" stroke="url(#goldLuster)" stroke-width="2"/>
      <!-- Golden Price Tag -->
      <rect x="-25" y="16" width="65" height="18" rx="4" fill="#facc15" stroke="#713f12" stroke-width="1.5"/>
      <text x="7" y="29" font-family="'Montserrat', sans-serif" font-weight="900" font-size="11" fill="#78350f" text-anchor="middle">100 GOLD</text>
    </g>
    <g transform="translate(240, 780)">
      <ellipse cx="0" cy="14" rx="38" ry="8" fill="rgba(0,0,0,0.5)"/>
      <path d="M-35,6 Q-30,-16 -5,-18 Q15,-20 32,-10 Q38,0 35,6 Z" fill="#78350f" stroke="url(#goldLuster)" stroke-width="2"/>
      <path d="M-15,6 Q-10,-14 15,-16 Q32,-18 48,-8 Q54,2 50,6 Z" fill="#78350f" stroke="url(#goldLuster)" stroke-width="2"/>
      <rect x="-25" y="16" width="65" height="18" rx="4" fill="#facc15" stroke="#713f12" stroke-width="1.5"/>
      <text x="7" y="29" font-family="'Montserrat', sans-serif" font-weight="900" font-size="11" fill="#78350f" text-anchor="middle">100 GOLD</text>
    </g>

    <!-- Right Arched Vitrine -->
    <path d="M700,260 Q700,180 840,180 Q980,180 980,260 L980,1180 L700,1180 Z" fill="url(#velvetRed)" stroke="url(#goldLuster)" stroke-width="14"/>
    <rect x="720" y="520" width="240" height="16" rx="4" fill="url(#goldLuster)"/>
    <rect x="720" y="800" width="240" height="16" rx="4" fill="url(#goldLuster)"/>

    <!-- Shoes in Right Vitrine -->
    <g transform="translate(840, 500)">
      <ellipse cx="0" cy="14" rx="38" ry="8" fill="rgba(0,0,0,0.5)"/>
      <path d="M-35,6 Q-30,-16 -5,-18 Q15,-20 32,-10 Q38,0 35,6 Z" fill="#991b1b" stroke="url(#goldLuster)" stroke-width="2"/>
    </g>
    <g transform="translate(840, 780)">
      <ellipse cx="0" cy="14" rx="38" ry="8" fill="rgba(0,0,0,0.5)"/>
      <path d="M-35,6 Q-30,-16 -5,-18 Q15,-20 32,-10 Q38,0 35,6 Z" fill="#15803d" stroke="url(#goldLuster)" stroke-width="2"/>
    </g>

    <!-- Grand Marble Columns (Left & Right) -->
    <rect x="18" y="180" width="54" height="1160" fill="#f4f4f5" stroke="#71717a" stroke-width="4"/>
    <rect x="10" y="170" width="70" height="25" rx="3" fill="url(#goldLuster)"/>
    <rect x="10" y="1320" width="70" height="30" rx="3" fill="url(#goldLuster)"/>

    <rect x="1008" y="180" width="54" height="1160" fill="#f4f4f5" stroke="#71717a" stroke-width="4"/>
    <rect x="1000" y="170" width="70" height="25" rx="3" fill="url(#goldLuster)"/>
    <rect x="1000" y="1320" width="70" height="30" rx="3" fill="url(#goldLuster)"/>

    <!-- Magnificent Crystal Chandelier (Ceiling Center) -->
    <line x1="540" y1="0" x2="540" y2="120" stroke="url(#goldLuster)" stroke-width="6"/>
    <ellipse cx="540" cy="220" rx="200" ry="120" fill="url(#chandelierGlow)"/>
    <!-- Chandelier Tier 1 -->
    <ellipse cx="540" cy="140" rx="90" ry="22" fill="none" stroke="url(#goldLuster)" stroke-width="6"/>
    <ellipse cx="540" cy="180" rx="140" ry="30" fill="none" stroke="url(#goldLuster)" stroke-width="8"/>
    <!-- Chandelier Hanging Crystals -->
    <line x1="420" y1="180" x2="420" y2="225" stroke="#ffffff" stroke-width="4" stroke-dasharray="6 3"/>
    <line x1="460" y1="190" x2="460" y2="245" stroke="#ffffff" stroke-width="4" stroke-dasharray="6 3"/>
    <line x1="500" y1="195" x2="500" y2="260" stroke="#ffffff" stroke-width="4" stroke-dasharray="6 3"/>
    <line x1="540" y1="195" x2="540" y2="270" stroke="#ffffff" stroke-width="5" stroke-dasharray="6 3"/>
    <line x1="580" y1="195" x2="580" y2="260" stroke="#ffffff" stroke-width="4" stroke-dasharray="6 3"/>
    <line x1="620" y1="190" x2="620" y2="245" stroke="#ffffff" stroke-width="4" stroke-dasharray="6 3"/>
    <line x1="660" y1="180" x2="660" y2="225" stroke="#ffffff" stroke-width="4" stroke-dasharray="6 3"/>

    <!-- Polished Marble Checkerboard Floor in Perspective -->
    <polygon points="0,1920 1080,1920 880,1260 200,1260" fill="url(#boutiqueCheckers)"/>
    <polygon points="0,1920 1080,1920 880,1260 200,1260" fill="url(#marbleTile)" opacity="0.4"/>
    <line x1="0" y1="1260" x2="1080" y2="1260" stroke="url(#goldLuster)" stroke-width="6"/>
    <line x1="0" y1="1580" x2="1080" y2="1580" stroke="#71717a" stroke-width="2" opacity="0.6"/>

    <!-- Velvet Pedestal Tables in Midground -->
    <g transform="translate(180, 1340)">
      <polygon points="0,0 80,0 65,120 15,120" fill="url(#goldLuster)"/>
      <ellipse cx="40" cy="0" rx="55" ry="16" fill="url(#velvetRed)" stroke="url(#goldLuster)" stroke-width="5"/>
    </g>
    <g transform="translate(820, 1340)">
      <polygon points="0,0 80,0 65,120 15,120" fill="url(#goldLuster)"/>
      <ellipse cx="40" cy="0" rx="55" ry="16" fill="url(#velvetRed)" stroke="url(#goldLuster)" stroke-width="5"/>
    </g>

    <!-- Master Counter (Dark Mahogany with Gold Trim) -->
    <polygon points="120,1460 960,1460 920,1380 160,1380" fill="#2d1203" stroke="url(#goldLuster)" stroke-width="6"/>
    <rect x="120" y="1460" width="840" height="42" fill="#1e0c02"/>
'''

print("All procedural SVG templates defined successfully!")

