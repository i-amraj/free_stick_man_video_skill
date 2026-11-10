---
name: procedural-backgrounds
description: >-
  Complete reference for building photorealistic-looking 2D/3D backgrounds and
  all scene assets ENTIRELY from SVG + CSS + Canvas code — no image files.
  Covers medieval rooms, cobblestone streets, wooden interiors, grand boutiques,
  furniture, props, lighting, atmospheric effects, and depth layering.
  Use this skill whenever a scene background or prop must be generated
  procedurally (e.g. medieval shop, cobblestone alley, winter street, grand hall,
  fireplace, bookshelves, tables, phones, signs, coins).
---

# Procedural Backgrounds & Assets (`procedural-backgrounds`)

> [!IMPORTANT]
> **Golden Rule**: ZERO external image files. Every pixel — sky, floor, walls,
> furniture, props, light — is drawn with SVG elements, CSS gradients, or
> Canvas 2D commands. This skill is the ONLY source of truth for how to
> build photorealistic-looking environments from code alone.

---

## 1. Architecture — Layer Stack

Every scene uses a **5-layer stack** inside a 1080×1920 SVG or `<div>` viewport:

```
Layer Z-Index  Name              Contents
─────────────────────────────────────────────────────
  0  (bottom)  SKY / FAR BG      Sky gradient, distant buildings (blurred/desaturated)
  1            MID ENVIRONMENT   Walls, floor, main architectural elements
  2            ATMOSPHERE        Fog overlay, light shafts, dust motes, smoke
  3            FURNITURE / PROPS Workbench, shelves, signs, tables, coins, shoes
  4  (top)     FOREGROUND VIGNETTE Dark vignette around edges for cinema depth
```

Characters (SVG `<g>` groups) sit on a **separate DOM layer at z-index 10**,
composited over the procedural background at z-index 0–4.

---

## 2. The Master SVG Template

```html
<!-- 1080×1920 vertical scene wrapper -->
<svg id="bg" xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 1080 1920" width="1080" height="1920"
     style="position:absolute;top:0;left:0;z-index:0;">
  <defs>
    <!-- All filters, gradients, patterns declared here -->
  </defs>

  <!-- Layer 0: Sky / Far Background -->
  <g id="layer-sky">...</g>

  <!-- Layer 1: Walls / Floor / Architecture -->
  <g id="layer-arch">...</g>

  <!-- Layer 2: Atmosphere (fog, light shafts, particles) -->
  <g id="layer-atmo">...</g>

  <!-- Layer 3: Furniture & Props -->
  <g id="layer-props">...</g>

  <!-- Layer 4: Edge Vignette -->
  <g id="layer-vignette">...</g>
</svg>
```

---

## 3. Core Techniques

### 3.1 Perspective Floor (Cobblestone / Wood Planks)

**Principle**: Use SVG `<polygon>` with a vanishing point to fake 3D perspective.
Vanishing point for 9:16 vertical video = `(540, 1150)` (center-ish, slightly above mid).

```svg
<!-- Perspective wooden floor — planks converging to VP(540,1150) -->
<defs>
  <linearGradient id="floorGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#2a1a0e"/>   <!-- far = dark -->
    <stop offset="100%" stop-color="#5c3317"/>  <!-- near = bright -->
  </linearGradient>
  <pattern id="woodGrain" x="0" y="0" width="40" height="8" patternUnits="userSpaceOnUse" patternTransform="skewX(-5)">
    <rect width="40" height="8" fill="none"/>
    <line x1="0" y1="2" x2="40" y2="2" stroke="#3d2210" stroke-width="0.4" opacity="0.6"/>
    <line x1="0" y1="5" x2="40" y2="5" stroke="#6b3f1f" stroke-width="0.2" opacity="0.3"/>
  </pattern>
</defs>

<!-- Floor base -->
<polygon points="0,1920 1080,1920 820,1150 260,1150"
         fill="url(#floorGrad)" />
<!-- Wood grain overlay on floor -->
<polygon points="0,1920 1080,1920 820,1150 260,1150"
         fill="url(#woodGrain)" opacity="0.5"/>

<!-- Individual perspective planks (horizontal lines converging to VP) -->
<!-- Plank separators: draw lines from left-edge to right-edge, all aimed at VP(540,1150) -->
<line x1="0" y1="1500" x2="1080" y2="1500" stroke="#1a0d06" stroke-width="2" opacity="0.4"/>
<line x1="0" y1="1680" x2="1080" y2="1680" stroke="#1a0d06" stroke-width="3" opacity="0.5"/>
<!-- Longitudinal plank dividers: draw from VP toward bottom corners -->
<line x1="540" y1="1150" x2="0" y2="1920"   stroke="#1a0d06" stroke-width="2" opacity="0.3"/>
<line x1="540" y1="1150" x2="270" y2="1920"  stroke="#1a0d06" stroke-width="1.5" opacity="0.25"/>
<line x1="540" y1="1150" x2="540" y2="1920"  stroke="#1a0d06" stroke-width="1.5" opacity="0.25"/>
<line x1="540" y1="1150" x2="810" y2="1920"  stroke="#1a0d06" stroke-width="1.5" opacity="0.25"/>
<line x1="540" y1="1150" x2="1080" y2="1920" stroke="#1a0d06" stroke-width="2" opacity="0.3"/>
```

**Cobblestone variant** — replace planks with irregular rounded rects:
```svg
<defs>
  <pattern id="cobbles" x="0" y="0" width="80" height="60" patternUnits="userSpaceOnUse">
    <rect width="80" height="60" fill="#3a3028"/>
    <rect x="2" y="2" width="34" height="26" rx="4" fill="#4a3d33" stroke="#2a2219" stroke-width="1.5"/>
    <rect x="42" y="2" width="36" height="26" rx="4" fill="#463a30" stroke="#2a2219" stroke-width="1.5"/>
    <rect x="2" y="32" width="22" height="24" rx="4" fill="#4e4238" stroke="#2a2219" stroke-width="1.5"/>
    <rect x="28" y="32" width="28" height="24" rx="4" fill="#42362c" stroke="#2a2219" stroke-width="1.5"/>
    <rect x="60" y="32" width="18" height="24" rx="4" fill="#4a3e34" stroke="#2a2219" stroke-width="1.5"/>
  </pattern>
</defs>
<polygon points="0,1920 1080,1920 820,1150 260,1150"
         fill="url(#cobbles)"
         transform="perspective(900) rotateX(35deg)"/>
<!-- Fade cobbles at distance (near VP) with gradient overlay -->
<polygon points="260,1150 820,1150 900,1300 180,1300"
         fill="url(#floorGrad)" opacity="0.6"/>
```

---

### 3.2 Walls (Stone / Timber / Plaster)

**Back wall** (rectangle filling top ~60% of viewport):
```svg
<defs>
  <linearGradient id="wallGrad" x1="0.5" y1="0" x2="0.5" y2="1">
    <stop offset="0%"   stop-color="#0d0a06"/>  <!-- top = very dark -->
    <stop offset="60%"  stop-color="#1f1510"/>  <!-- mid = dark warm -->
    <stop offset="100%" stop-color="#2e1e14"/>  <!-- base = slightly lighter -->
  </linearGradient>
  <!-- Stone block pattern -->
  <pattern id="stoneWall" x="0" y="0" width="120" height="60" patternUnits="userSpaceOnUse">
    <rect width="120" height="60" fill="#1e1612"/>
    <!-- Row 1: 2 blocks offset -->
    <rect x="1"  y="1"  width="118" height="27" rx="2" fill="#24190f" stroke="#120d08" stroke-width="1.5"/>
    <!-- Row 2: offset blocks -->
    <rect x="1"  y="32" width="58"  height="27" rx="2" fill="#201510" stroke="#120d08" stroke-width="1.5"/>
    <rect x="61" y="32" width="58"  height="27" rx="2" fill="#261b11" stroke="#120d08" stroke-width="1.5"/>
    <!-- Random crack details -->
    <line x1="30"  y1="1"  x2="28"  y2="28" stroke="#0e0a06" stroke-width="0.5" opacity="0.6"/>
    <line x1="80"  y1="32" x2="82"  y2="59" stroke="#0e0a06" stroke-width="0.5" opacity="0.4"/>
  </pattern>
</defs>

<!-- Back wall -->
<rect x="0" y="0" width="1080" height="1200" fill="url(#wallGrad)"/>
<!-- Stone texture overlay -->
<rect x="0" y="0" width="1080" height="1200" fill="url(#stoneWall)" opacity="0.55"/>
```

**Timber frame** — decorative dark beams criss-crossing the wall:
```svg
<!-- Horizontal beam -->
<rect x="0" y="380" width="1080" height="28" rx="4" fill="#1a0e07" opacity="0.85"/>
<!-- Diagonal support brace (left) -->
<polygon points="0,380 160,520 160,548 0,408" fill="#150c05" opacity="0.8"/>
<!-- Diagonal support brace (right) -->
<polygon points="1080,380 920,520 920,548 1080,408" fill="#150c05" opacity="0.8"/>
<!-- Vertical post (left) -->
<rect x="40" y="0" width="22" height="1920" fill="#1a0e07" opacity="0.75"/>
<!-- Vertical post (right) -->
<rect x="1018" y="0" width="22" height="1920" fill="#1a0e07" opacity="0.75"/>
<!-- Center post -->
<rect x="529" y="0" width="22" height="600" fill="#1a0e07" opacity="0.6"/>
```

---

### 3.3 Windows

```svg
<!-- Arched window with moonlight glow -->
<defs>
  <radialGradient id="moonlight" cx="0.5" cy="0" r="0.9">
    <stop offset="0%"   stop-color="#c8d8f5" stop-opacity="0.95"/>
    <stop offset="50%"  stop-color="#8ba8d8" stop-opacity="0.5"/>
    <stop offset="100%" stop-color="#1a2a4a" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="windowClip">
    <path d="M220,80 Q220,20 320,20 Q420,20 420,80 L420,340 L220,340 Z"/>
  </clipPath>
</defs>

<!-- Window frame (stone surround) -->
<path d="M210,70 Q210,10 320,10 Q430,10 430,70 L430,350 L210,350 Z"
      fill="#2a1f14" stroke="#141008" stroke-width="6"/>
<!-- Window glass (moonlight) -->
<path d="M220,80 Q220,20 320,20 Q420,20 420,80 L420,340 L220,340 Z"
      fill="url(#moonlight)"/>
<!-- Window cross-bar -->
<line x1="320" y1="20" x2="320" y2="340" stroke="#2a1f14" stroke-width="8"/>
<line x1="220" y1="200" x2="420" y2="200" stroke="#2a1f14" stroke-width="8"/>
<!-- Moonlight shaft cast on floor -->
<polygon points="220,340 420,340 540,1200 160,1200"
         fill="url(#moonlight)" opacity="0.15"/>
```

---

### 3.4 Fireplace

```svg
<defs>
  <!-- Ember/flame animated gradient -->
  <radialGradient id="flameGlow" cx="0.5" cy="1" r="0.8">
    <stop offset="0%"   stop-color="#ff6b00" stop-opacity="0.9"/>
    <stop offset="40%"  stop-color="#ff3300" stop-opacity="0.7"/>
    <stop offset="100%" stop-color="#8b0000" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="emberLight" cx="0.5" cy="0.8" r="1">
    <stop offset="0%"   stop-color="#ff9500" stop-opacity="0.6"/>
    <stop offset="100%" stop-color="#ff4400" stop-opacity="0"/>
  </radialGradient>
</defs>

<!-- Fireplace stone mantle -->
<rect x="380" y="800" width="320" height="20" rx="4" fill="#2e2015"/>
<!-- Mantle top slab -->
<rect x="360" y="780" width="360" height="24" rx="3" fill="#3a2819"/>
<!-- Firebox opening (arch) -->
<path d="M400,820 Q400,870 540,870 Q680,870 680,820 L680,1050 L400,1050 Z"
      fill="#0d0906"/>
<!-- Fire glow area -->
<ellipse cx="540" cy="1020" rx="120" ry="30" fill="url(#flameGlow)"/>
<!-- Flame shapes (SVG paths) -->
<path d="M480,1020 Q490,970 510,990 Q520,940 540,960 Q555,920 560,970 Q580,950 590,1010 Q570,990 555,1015 Q540,985 525,1015 Q505,995 480,1020Z"
      fill="#ff6b00" opacity="0.9">
  <!-- Animate with JS: oscillate opacity 0.7–1.0 at 0.2s intervals -->
</path>
<!-- Ambient orange room light from fire -->
<radialGradient id="fireAmbient" cx="0.5" cy="1" r="1.2">
  <stop offset="0%"   stop-color="#ff7700" stop-opacity="0.3"/>
  <stop offset="100%" stop-color="#ff4400" stop-opacity="0"/>
</radialGradient>
<rect x="0" y="600" width="1080" height="1320" fill="url(#fireAmbient)"/>
```

---

### 3.5 Furniture — Workbench / Table

**Perspective table** using isometric-ish trapezoid for the top surface:
```svg
<defs>
  <linearGradient id="tableTop" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#6b3f1f"/>
    <stop offset="100%" stop-color="#4a2a0f"/>
  </linearGradient>
  <linearGradient id="tableSide" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#3a1e08"/>
    <stop offset="100%" stop-color="#250f03"/>
  </linearGradient>
</defs>

<!-- Table top (perspective trapezoid — wider at bottom/near, narrow at top/far) -->
<polygon points="120,1480  960,1480  900,1420  180,1420"
         fill="url(#tableTop)"/>
<!-- Table front face (rectangle below trapezoid) -->
<rect x="120" y="1480" width="840" height="40" fill="url(#tableSide)"/>
<!-- Table left leg -->
<rect x="140" y="1520" width="40" height="260" rx="4" fill="#2a1508"/>
<!-- Table right leg -->
<rect x="900" y="1520" width="40" height="260" rx="4" fill="#2a1508"/>
<!-- Table cross-brace -->
<rect x="140" y="1660" width="800" height="16" rx="3" fill="#200f04"/>
<!-- Wood grain on table top -->
<line x1="200" y1="1420" x2="180" y2="1480" stroke="#5a3015" stroke-width="1" opacity="0.4"/>
<line x1="400" y1="1420" x2="380" y2="1480" stroke="#5a3015" stroke-width="1" opacity="0.4"/>
<line x1="600" y1="1420" x2="580" y2="1480" stroke="#5a3015" stroke-width="1" opacity="0.4"/>
<line x1="800" y1="1420" x2="780" y2="1480" stroke="#5a3015" stroke-width="1" opacity="0.4"/>
```

---

### 3.6 Shelves with Items

```svg
<!-- Shelf board -->
<rect x="60" y="680" width="340" height="22" rx="3" fill="#3d2210"/>
<!-- Shelf bracket (left) -->
<polygon points="60,702 60,750 90,702" fill="#2a1508"/>
<!-- Shelf bracket (right) -->
<polygon points="400,702 400,750 370,702" fill="#2a1508"/>

<!-- Book 1 on shelf -->
<rect x="80"  y="620" width="38" height="60" rx="2" fill="#8b2020"/>
<rect x="80"  y="620" width="6"  height="60" fill="#6b1818"/>
<text x="99" y="660" font-size="10" fill="#f5c842" transform="rotate(-90,99,650)"
      font-family="serif" opacity="0.7">SPELLS</text>
<!-- Book 2 -->
<rect x="122" y="630" width="32" height="50" rx="2" fill="#1a4a2a"/>
<rect x="122" y="630" width="5"  height="50" fill="#133820"/>
<!-- Book 3 (leaning) -->
<rect x="158" y="635" width="28" height="45" rx="2"
      fill="#3a2a7a" transform="rotate(-5, 172, 658)"/>
<!-- Potion bottle -->
<ellipse cx="230" cy="668" rx="12" ry="8" fill="#2a4a2a"/>
<rect x="218" y="638" width="24" height="30" rx="8" fill="#1a3a1a" opacity="0.9"/>
<ellipse cx="230" cy="638" rx="8" ry="5" fill="#2a4a2a"/>
<rect x="225" y="626" width="10" height="14" rx="3" fill="#3a5a3a"/>
<!-- Potion liquid glow -->
<ellipse cx="230" cy="655" rx="10" ry="12" fill="#00ff88" opacity="0.4"
         filter="url(#glow)"/>
```

---

### 3.7 Shoes & Props

```svg
<!-- Left shoe (flat vector, Comicron style) -->
<g transform="translate(560, 1390)">
  <!-- Sole -->
  <ellipse cx="0" cy="20" rx="55" ry="12" fill="#1a1008"/>
  <!-- Upper -->
  <path d="M-55,10 Q-50,-25 -10,-28 Q20,-30 45,-15 Q55,0 50,10 Z"
        fill="#2d1a0a" stroke="#1a0d05" stroke-width="2"/>
  <!-- Toe cap -->
  <path d="M-55,10 Q-55,-5 -30,-10 Q-10,-12 10,-5 Q-10,5 -30,8 Z"
        fill="#3d2614"/>
  <!-- Lace holes -->
  <circle cx="-15" cy="-5" r="3" fill="#0a0604"/>
  <circle cx="5"   cy="-8" r="3" fill="#0a0604"/>
  <circle cx="22"  cy="-8" r="3" fill="#0a0604"/>
  <!-- Laces -->
  <path d="M-15,-5 Q-5,-12 5,-8 Q15,-14 22,-8" stroke="#f5e6c8" stroke-width="1.5" fill="none"/>
  <!-- Highlight -->
  <path d="M-30,0 Q-10,-15 15,-12" stroke="#5a3a1f" stroke-width="1" fill="none" opacity="0.5"/>
</g>
```

---

### 3.8 Atmospheric Lighting Effects

#### Single-Point Lantern Light
```svg
<defs>
  <!-- Warm lantern: radial from lamp position -->
  <radialGradient id="lanternGlow" cx="0.5" cy="0.1" r="1">
    <stop offset="0%"   stop-color="#ffd700" stop-opacity="0.7"/>
    <stop offset="20%"  stop-color="#ff9500" stop-opacity="0.4"/>
    <stop offset="60%"  stop-color="#ff5500" stop-opacity="0.1"/>
    <stop offset="100%" stop-color="#8b2200" stop-opacity="0"/>
  </radialGradient>
</defs>

<!-- Lantern body (hanging from ceiling) -->
<rect x="516" y="80" width="48" height="70" rx="8"
      fill="#8b6914" stroke="#5a4209" stroke-width="3"/>
<!-- Glass panels (glowing) -->
<rect x="522" y="88" width="14" height="54" rx="2" fill="#ffe87a" opacity="0.9"
      filter="url(#blur2)"/>
<rect x="540" y="88" width="14" height="54" rx="2" fill="#ffdd55" opacity="0.8"
      filter="url(#blur2)"/>
<!-- Lantern chain -->
<line x1="540" y1="0"  x2="540" y2="80" stroke="#5a4209" stroke-width="4"/>
<!-- Warm light cone cast downward -->
<polygon points="400,150  680,150  900,1920  180,1920"
         fill="url(#lanternGlow)" opacity="0.35"/>
<!-- Caustic light shimmer on floor (animated via GSAP) -->
<ellipse cx="540" cy="1800" rx="300" ry="50"
         fill="#ff9500" opacity="0.08" filter="url(#blur20)"/>
```

#### Volumetric God Ray (Skylight)
```svg
<defs>
  <linearGradient id="godRay" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#c8d8f5" stop-opacity="0.6"/>
    <stop offset="100%" stop-color="#c8d8f5" stop-opacity="0"/>
  </linearGradient>
</defs>
<!-- Ray 1 (main) -->
<polygon points="420,0 620,0 780,1300 240,1300"
         fill="url(#godRay)" opacity="0.18" filter="url(#blur8)"/>
<!-- Ray 2 (thinner, offset) -->
<polygon points="520,0 580,0 650,1300 450,1300"
         fill="url(#godRay)" opacity="0.12" filter="url(#blur4)"/>
<!-- Dust motes in ray (animated) -->
<!-- 20 tiny circles scattered in ray band, opacity pulsed with GSAP -->
<circle cx="490" cy="300"  r="2.5" fill="#e0d0b0" opacity="0.6"/>
<circle cx="560" cy="480"  r="2"   fill="#e0d0b0" opacity="0.5"/>
<circle cx="530" cy="650"  r="3"   fill="#e0d0b0" opacity="0.4"/>
<circle cx="510" cy="820"  r="1.5" fill="#e0d0b0" opacity="0.55"/>
<circle cx="580" cy="1000" r="2"   fill="#e0d0b0" opacity="0.3"/>
```

---

### 3.9 Depth Layering: Atmospheric Desaturation

Objects **far from camera** = desaturated (grey-ish), blurred, darker.
Objects **near camera** = saturated, sharp, brighter.

```svg
<defs>
  <!-- Depth-of-field blur for far elements -->
  <filter id="blur2">  <feGaussianBlur stdDeviation="2"/></filter>
  <filter id="blur4">  <feGaussianBlur stdDeviation="4"/></filter>
  <filter id="blur8">  <feGaussianBlur stdDeviation="8"/></filter>
  <filter id="blur20"> <feGaussianBlur stdDeviation="20"/></filter>
  <!-- Desaturate filter for far BG elements -->
  <filter id="desaturate">
    <feColorMatrix type="saturate" values="0.3"/>
    <feColorMatrix type="matrix"
      values="0.7 0 0 0 0
              0   0.7 0 0 0
              0   0 0.7 0 0
              0   0 0   1 0"/>
  </filter>
  <!-- Cinematic color grade (warm shadows, cool highlights) -->
  <filter id="colorGrade">
    <feColorMatrix type="matrix"
      values="1.1  0.0  0.0  0  0.02
              0.0  0.95 0.0  0  0.00
              0.0  0.0  0.85 0  0.00
              0.0  0.0  0.0  1  0.0"/>
  </filter>
  <!-- Glow for emissive elements (lantern, gems, fire) -->
  <filter id="glow">
    <feGaussianBlur stdDeviation="8" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="glowStrong">
    <feGaussianBlur stdDeviation="18" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>

<!-- Far background elements: apply filter="url(#desaturate)" + filter="url(#blur4)" -->
<!-- Mid elements: no filter, or feColorMatrix tweak only -->
<!-- Near elements: filter="url(#colorGrade)" for warmth -->
```

---

### 3.10 Edge Vignette (Cinema Look)

Always add as the TOPMOST background layer:
```svg
<defs>
  <radialGradient id="vignette" cx="0.5" cy="0.5" r="0.8">
    <stop offset="0%"   stop-color="#000000" stop-opacity="0"/>
    <stop offset="70%"  stop-color="#000000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.75"/>
  </radialGradient>
</defs>
<rect x="0" y="0" width="1080" height="1920" fill="url(#vignette)"
      pointer-events="none"/>
```

---

## 4. Scene Recipes

### Recipe A: Medieval Cobbler Workshop (Night Interior)

```
Layers:
  SKY          → none (interior, ceiling is dark stone)
  BACK WALL    → stoneWall pattern + wallGrad + timber frames
  WINDOW       → arched window, left ~x=180–380, moonlight shaft
  FIREPLACE    → right side ~x=700–900, y=800–1100
  FLOOR        → woodFloor perspective polygon, VP(540,1150)
  WORKBENCH    → table SVG, center x=180–900, y=1420–1520
  SHELVES      → left wall x=60–400, y=620–710 (3 levels)
  PROPS        → shoes, tools, candles on table
  LANTERN      → hanging center, y=0–150
  ATMOSPHERE   → fire glow radial, lantern cone polygon, dust motes
  VIGNETTE     → full-frame radial vignette

GSAP camera drift: scale 1.0→1.03, translate (-8px, 0)→(8px, -6px) over 5s
```

### Recipe B: Medieval Street (Night, Exterior)

```
Layers:
  SKY          → linearGradient #05080f → #0d1428 (deep night)
  MOON         → circle cx=800 cy=180 r=70, radialGradient white→blue
  BUILDINGS    → 3 buildings: left/center/right, stoneWall + arched doors
  LANTERN POSTS → 2 posts, hanging lanterns with warm glow cones
  COBBLE FLOOR → cobblestone polygon, VP(540,1400)
  SHOP SIGN    → hanging sign with rope, painted text
  SNOW/FOG     → optional white circles + fog overlay at bottom
  VIGNETTE     → standard

Buildings: simple rectangles with pointed/flat roofs (polygon), stone pattern,
           arched doorways, shuttered windows (dark rect with light leak).
```

### Recipe C: Grand Boutique Hall (Luxury Interior)

```
Layers:
  CEILING      → linearGradient dark → slightly warm, ornate cornice (rect+pattern)
  CHANDELIERS  → 2 hanging SVG chandeliers with glow
  BACK WALL    → tall arched display cases (rect + arch clip), warm marble gradient
  MARBLE FLOOR → polygon with checkerboard pattern (white/off-white tiles, perspective)
  DISPLAY CASES → glass (rect + opacity 0.3) with shoes/items inside
  GOLD TRIM    → lines/rects with #d4a017 fill
  COLUMNS      → 2 columns left/right, cylindrical (rect + ellipse top/bottom)
  ATMOSPHERE   → golden light pools, soft vignette
```

### Recipe D: Winter Street (Exterior, Snow)

```
Layers:
  SKY          → linearGradient #1a2235 → #0d1428 (pre-dawn)
  SNOW GROUND  → white polygon perspective, slightly blue-tinted
  BUILDINGS    → grey stone buildings, snow on roofs (white polygons)
  BARE TREES   → recursive SVG branch paths (organic fractal)
  SNOW FALL    → 60 white circles, r=2–6, animated downward with GSAP
  FOG          → white linearGradient bottom overlay, opacity 0.3
  VIGNETTE     → standard (darker for cold feel)
```

---

## 5. GSAP Animation Hooks for Procedural Backgrounds

```javascript
// Camera drift (sub-current — mandatory per "Camera Kabhi Rukta Nahi")
gsap.to(".camera-rig", {
  x: 15, y: -8, scale: 1.035,
  duration: 5, ease: "sine.inOut",
  yoyo: true, repeat: -1
});

// Flame flicker (fireplace)
gsap.to("#flame-path", {
  scaleY: 0.88, scaleX: 1.08, transformOrigin: "50% 100%",
  duration: 0.18, ease: "power1.inOut",
  yoyo: true, repeat: -1
});

// Lantern sway
gsap.to("#lantern-g", {
  rotation: 4, transformOrigin: "50% 0%",
  duration: 2.4, ease: "sine.inOut",
  yoyo: true, repeat: -1
});

// Dust motes float upward in light ray
gsap.to(".dust-mote", {
  y: "-=80", opacity: 0,
  duration: 3, ease: "none",
  stagger: { each: 0.4, repeat: -1,
             from: "random", yoyo: false },
  onRepeat: function() {
    gsap.set(this.targets(), { y: "+=80", opacity: 0.6 });
  }
});

// Snow fall
gsap.to(".snowflake", {
  y: "+=1920", opacity: 0,
  duration: () => Math.random() * 4 + 3,
  ease: "none",
  stagger: { each: 0.1, repeat: -1 },
  onRepeat: function() {
    gsap.set(this.targets(), { y: -20, x: () => Math.random() * 1080 });
  }
});
```

---

## 6. Performance Rules

| Rule | Requirement |
|------|------------|
| Max SVG elements per scene | ≤ 800 (avoid DOM bloat) |
| Animated elements | Use GSAP `set()` before `to()` to prevent layout thrash |
| Blur filters | Never apply `feGaussianBlur` with `stdDeviation > 20` to animated elements |
| Particle count | ≤ 60 per scene (snowflakes, dust motes) |
| Pattern usage | Pre-define all `<pattern>` in `<defs>`, never inline |
| Color grading | Apply `filter="url(#colorGrade)"` to entire scene `<g>`, not individual elements |
| Virtual clock | Background GSAP animations MUST be on `masterTimeline` so `seekToTime(t)` controls them |

---

## 7. Quick Asset Catalog

| Asset | SVG Technique | Key Elements |
|-------|--------------|-------------|
| Medieval building | `rect` + stone `pattern` + arch `path` | Staggered stone blocks, arched doorway |
| Rope (hanging) | Wavy `path`, brown stroke | `M x,0 Q x+5,20 x,40 Q x-5,60 x,40...` |
| Candle | Thin `rect` + ellipse flame + radial glow | 3px wide rect, flicker animation |
| Coin (gold) | `ellipse` + inner ellipse + feDropShadow | Stacked ellipses for 3D look |
| Book | `rect` + spine `rect` + rotated `text` | Multiple rects per book |
| Phone (modern) | `rect` rx=12 + inner screen rect | Dark body, bright screen |
| Scroll/sign | `rect` with rolled ends (ellipses) | Brown rect + 2 horizontal cylinders |
| Tree (bare) | Recursive `path` or `polyline` branches | Fractal-like branch splitting |
| Snow on surface | `path` with wavy top + white fill | Irregular polygon |
| Fog layer | `linearGradient` rect, opacity 0.2–0.4 | Bottom 30% of frame, white→transparent |

---

## 8. Integration with scene.html (HyperFrames contract)

```html
<!-- In scene HTML, background SVG goes inside .camera-rig, BEFORE character SVGs -->
<div class="scene active" id="scene1">
  <div class="camera-rig" id="cam1">

    <!-- PROCEDURAL BACKGROUND (no image files!) -->
    <svg id="bg-scene1" xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 1080 1920" width="1080" height="1920"
         style="position:absolute;top:0;left:0;z-index:0;">
      <!-- All background layers here -->
    </svg>

    <!-- CHARACTER SVGs (z-index 10) -->
    <svg id="chars-scene1" ... style="position:absolute;top:0;left:0;z-index:10;">
      <!-- Character groups here -->
    </svg>

    <!-- SUBTITLE LAYER (z-index 20) -->
    <div id="subs-scene1" style="position:absolute;bottom:200px;...;z-index:20;">
    </div>

  </div>
</div>
```

> [!TIP]
> Always put background SVG with `z-index:0` and `pointer-events:none`.
> Characters go on a separate SVG or `<div>` with `z-index:10`.
> This separation makes it easy to swap backgrounds without touching character rigs.

---

## 10. The Script-to-Screen Doctrine: 100% Narrative Matching & Micro-Detail Mastery

> [!CAUTION]
> **Zero Story Disconnect**: A background or scene is NOT complete if any spoken word in the script lacks its matching visual prop, character action, or environment state. Never draw generic filler — every detail must serve the script.

### 10.1 The 4 Laws of Narrative Synchronization
1. **The Number & Noun Rule**:
   - If the script mentions a specific number or object (e.g. *"300 right shoes"*, *"10 guards"*, *"5 coins"*, *"for firewood"*, *"one leg"*), it MUST appear visibly on screen as a counted element, badge, tally board, or prop.
2. **The Cause-and-Effect Visual**:
   - When a transition occurs (*"Old Corvin counted what was left... nobody came"*, *"the thief never showed up... every left boot vanished"*), the scene must reflect the emotional and physical aftermath (empty street, yawning guards, smoke where boots used to be).
3. **The Infographic Climax for Complex Logic**:
   - When the narrative explains a twist or economic strategy (*"one shoe was worthless... he stole the half nobody could sell and let Corvin sell him the rest... paid 5 coins for 300 pairs"*), use **high-clarity visual comparison cards / puzzle mechanics** (e.g. `[Left 0$] + [Right 0$] ➔ [Pair 100$]`) so the viewer instantly grasps the genius of the plot.
4. **Micro-Grounding & Shadow Anchor**:
   - Characters, benches, tables, and coins must NEVER float. Every object on a surface must cast a perspective ellipse shadow (`rx`, `ry`, `fill="rgba(10,15,25,0.55)"`) directly under its contact point.

### 10.2 Character Anatomy & Joint Alignment
- **Head-to-Torso Weld**: Always ensure the head `<circle>` overlaps the neck/collar by at least 10–14px, or sits within the same `<g>` transform. Never leave an open gap between head and body.
- **Arm-to-Prop Weld**: When a character holds an item (shoe, sign, hammer, coins), the hand circle/endpoint must overlap the prop's coordinate origin.
- **Face Emotion Fidelity**:
  - Hysterical laugh: curved upward eyes (`Q` curves), open mouth with tongue + teeth, tear droplets.
  - Grief / Relief: drooping head, quivering mouth, tear stream paths with cyan drop highlights.
  - Mystery / Smug: one arched eyebrow, single-eye wink, tilted smirk.

---

## 11. File Naming Convention

```
projects/<project>/
├── scene.html              ← master HTML (all scenes)
├── bg_scene1.svg           ← optional: standalone SVG for scene 1 BG (can be inlined)
├── bg_scene2.svg
└── assets/
    └── master_audio.mp3    ← ONLY file allowed to be non-code
```

**NO** `.jpg`, `.png`, `.webp` background files. Audio files are the sole exception.

