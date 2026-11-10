# Comicron Style Guide & Visual Design System

## 1. Character Puppet Architecture (Hierarchical Rigging)

To prevent the "floating head" / detached mouth bug, all characters MUST use **Hierarchical Rigging**:

```
<g id="character-root">
  <ellipse class="ground-shadow" />
  <path class="stick-legs" />
  <g id="body-and-head-group">  <!-- BOUNCES TOGETHER IN GSAP -->
    <rect class="torso-capsule" />
    <path class="collar-trim" />
    <g id="head-group" transform="translate(0, -neckOffset)">
      <circle class="white-head" />
      <g class="hat" />
      <g class="facial-features" />
    </g>
  </g>
</g>
```

### Proportions Matrix
* **Head Radius**: `60px – 70px` (diameter `120px – 140px`).
* **Torso Dimensions**: Width `100px – 120px`, Height `150px – 180px`, corner radius `45px – 55px`.
* **Leg Length**: `140px – 165px` (~1.0x torso height).
* **Head Overlap**: Chin overlaps collar by `12px – 18px` so there is zero gap.
* **Top Hat**: Height `120px – 135px`, Brim Width `170px – 195px`.

### Color Palette Tokens
| Role | Hex Code | Usage |
|---|---|---|
| **Skin/Head** | `#FFFFFF` | All character heads |
| **Linework/Strokes** | `#121824` | Main outlines (6px - 7px) |
| **Royal Guard Blue** | `#2563eb` / `#1d4ed8` | Uniforms, top hats, fedoras |
| **Gold Trim** | `#eab308` / `#facc15` | Belts, buttons, medals, hat bands |
| **Corvin Clothes** | `#cbd5e1` / `#92400e` | Cobbler shirt & leather apron |
| **Stranger/Thief** | `#1e3a5f` / `#15803d` | Dark navy cloak, green & gold striped scarf |
| **Laugh Tongue** | `#ef4444` | Inside open laughing mouth |
| **Mouth Cavity** | `#7f1d1d` | Dark red interior of mouth |

---

## 2. Subtitle Typography (User Locked Doctrine)

Strictly use the **Demo 1 Typography**:
```css
#caption-box {
  position: absolute;
  bottom: 260px;
  left: 60px;
  right: 60px;
  z-index: 100;
  text-align: center;
  pointer-events: none;
}

.caption-phrase {
  font-family: 'Montserrat', sans-serif;
  font-size: 56px;
  font-weight: 900;
  color: #ffffff;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  line-height: 1.25;
  text-shadow: 
    0 4px 12px rgba(0,0,0,0.95),
    0 2px 4px #000,
    -2px -2px 0 #000,
     2px -2px 0 #000,
    -2px  2px 0 #000,
     2px  2px 0 #000;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.word-span {
  display: inline-block;
  transition: transform 0.08s ease, color 0.08s ease;
}

.word-span.active {
  color: #FFD700;
  transform: scale(1.18);
  text-shadow: 
    0 0 25px rgba(255, 215, 0, 0.7),
    0 4px 14px rgba(0,0,0,0.95),
    -2px -2px 0 #000,
     2px -2px 0 #000,
    -2px  2px 0 #000,
     2px  2px 0 #000;
}
```

---

## 3. Background Generation Prompt Formula
All background sets are generated in 9:16 vertical ratio using this syntax:
`"Stylized 3D low poly video game asset interior/exterior of [LOCATION] on [TIME/LIGHTING], Synty Studios polygonal art style. Vertical 9:16 composition. Clean faceted polygonal geometry, warm lighting, volumetric light beams, completely empty room/street, no people, no characters."`

