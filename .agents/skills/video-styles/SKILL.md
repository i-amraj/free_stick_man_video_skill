---
name: video-styles
description: >-
  Visual design system and aesthetic lock-in ("look lock") for 2D stickman and explainer videos.
  Use this skill to select, enforce, and validate a unified visual identity across all scenes,
  ensuring character stroke weights, typography hierarchies, color tokens (GrowKaz Dark Mystery,
  Paper Minimalist, Tech Blueprint, Viral High-Contrast), and UI card aesthetics remain strictly consistent.
---

# Video Styles & Look Lock (`video-styles`)

A successful video channel requires an unmistakable, locked visual identity. `video-styles` ensures every scene, character, prop, and overlay adheres to a unified visual language without stylistic drift.

---

## 1. The 4 Production Look Profiles

### Profile 1: GrowKaz Dark Mystery (Default Channel Style)
The signature look for mystery explainers, conspiracies, historical investigations, and deep dives.
- **Background**: Deep space slate `#0a0e1a` with subtle ambient radial vignette (`rgba(30, 41, 59, 0.4)`).
- **Stickman Character**: Crisp white `#f8fafc` stroke, `stroke-width: 7px`, head filled with `#0f172a`.
- **Primary Accent**: Electric Cyan (`#38bdf8`) for clues, data cards, and glowing focus items.
- **Secondary Accent**: Hot Pink / Magenta (`#ec4899`) for danger, twists, and shock warnings.
- **Typography**: Inter / Outfit (Headlines: 800 ExtraBold, Body: 500 Medium).

### Profile 2: Paper Minimalist (Chalk / Hand-drawn Feel)
- **Background**: Textured cream/paper `#fcfaf7`.
- **Stickman Character**: Charcoal ink `#18181b`, subtle hand-drawn wobble filter, `stroke-width: 6px`.
- **Accent Colors**: Highlighter Amber (`#f59e0b`) and Crimson (`#ef4444`).
- **Typography**: Caveat / Syne / Plus Jakarta Sans.

### Profile 3: Tech Cyber Blueprint
- **Background**: Deep blueprint navy `#030712` with subtle 40px grid overlay (`rgba(34, 211, 238, 0.08)`).
- **Stickman Character**: Neon cyan wireframe with subtle glow filter (`drop-shadow(0 0 6px #22d3ee)`).
- **Typography**: JetBrains Mono or Space Grotesk.

### Profile 4: Viral High-Contrast Short
- **Background**: Pure pitch `#000000`.
- **Character & UI**: Pure white `#ffffff` with high-saturation Electric Lime (`#22c55e`) and Cyber Yellow (`#facc15`).
- **Typography**: Anton or Montserrat Black (900 weight, all-caps, heavy black outline).

---

## 2. Character Anatomy & Stroke Specs (GrowKaz Lock)

To maintain exact continuity across all animator files, all SVG stickmen must conform to:

```css
:root {
  --sm-stroke: #f8fafc;
  --sm-stroke-width: 7px;
  --sm-head-r: 38px;
  --sm-spine-len: 180px;
  --sm-limb-width: 7px;
  --sm-eye-r: 4px;
}
```

- **Stroke Join**: Always `round` (`stroke-linejoin="round"`).
- **Stroke Cap**: Always `round` (`stroke-linecap="round"`).
- **Head Ratio**: Exactly **1:4.5** relative to total body height (oversized cartoon proportion).

---

## 3. UI Card & Overlay Token Standards

When rendering evidence cards, mystery clues, tweets, or chart overlays:

```css
.mystery-card {
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(56, 189, 248, 0.25);
  border-radius: 18px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45), 0 0 20px rgba(56, 189, 248, 0.15);
  padding: 24px 32px;
  color: #f8fafc;
}
```

---

## 4. Automated Style Linter (`scripts/lint_styles.py`)

Run this linter across your HTML/CSS scene files to verify zero color or stroke violations:
```bash
python scripts/lint_styles.py --dir ./scenes --profile growkaz_mystery
```

