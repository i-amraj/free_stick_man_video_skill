# GrowKaz Character Animation & Micro-Detail Guide (v2.0)

> **Project Memory & Production Standard** for the Comicron / GrowKaz Stickman Engine.
> Ships with battle-tested modules: `rig.js` (FK-by-rotation, IK, walk/dance, lip-sync) and `props.js` (~35 SVG props + shading primitives + costumes).

---

## 0. Key Shift: Forward Kinematics by Rotation

- **Old v1 Bug**: Moving bones by editing `x2,y2` of `<line>` elements caused child joints to detach (e.g., shin detaching from thigh during walk or bounce).
- **New v2 Law**: Limbs use **Forward Kinematics by Rotation** (`translate(joint) -> rotate(angle)`). Children live inside parent groups. Positions never change; only rotation angles change. Bones cannot separate under any animation.

---

## 1. Core Rule: "Script-First Understanding"

Before any SVG line or GSAP timeline is created:
1. **Script Breakdown**: Read each beat. Identify the Subject, Action, Emotion, Props, and Spatial Movement.
2. **The Number & Noun Rule**: If the narrator says "300 pairs", a board with "300" must be visible. If "two guards laugh", both guards must laugh with animated open mouths and laugh tears. If "he went broke", his pockets must be pulled out empty.
3. **Continuous Motion**: "Camera Kabhi Rukta Nahi" — camera drift and micro-life animations must play across every single frame.

---

## 2. Using `rig.js` & `props.js` in Any Scene

```html
<script src="rig.js"></script>
<script src="props.js"></script>
```

### 2.1 Spawning Characters
```javascript
const hero = GK.createCharacter(stageGroup, {
  id: 'hero',
  view: 'side', // 'side' for walk/run/sit/dance, 'front' for dialogue/audience
  style: 'toon', // 'toon' (filled+outlined) or 'stick'
  hairStyle: 'spiky', // 'short', 'spiky', 'long', 'bald'
  skin: '#fde0b5',
  shirt: '#2f6fed',
  pants: '#2b3445',
  shoe: '#3b2f2f'
});

hero.place(x, floorY); // Soles land exactly at floorY
```

### 2.2 Locomotion, Lip-Sync & Emotion
```javascript
// Walk with locked stride (zero foot sliding)
let t = hero.walk(tl, 0, { toX: 500 });

// Emotion & Posing
hero.expr(tl, t, 'happy');
hero.pose(tl, t, 'wave', 0.35, 'back.out(1.4)');
hero.hand(tl, t, 'R', 'open');

// Word-level dialogue with visemes (AA, EE, OO, MBP, FV)
hero.talk(tl, [
  { w: 'Hello', s: t + 0.2, e: t + 0.6 },
  { w: 'World!', s: t + 0.6, e: t + 1.2, stress: true }
], { arms: false });

// Micro-life
hero.autoBlink(tl, 0, 10);
hero.breathe(tl, t, t + 5);

// Sitting on chairs (IK keeps feet planted)
hero.pose(tl, t + 2, 'sitSide', 0.5);

// Synchronized dancing
hero.dance(tl, t + 4, 'disco', 8, 120);
```

### 2.3 Ready-to-Use SVG Props (`GK.P.*`)
- **Furniture**: `table`, `chair`, `bed`, `sofa`, `lamp`, `door`, `window`, `shelf`, `tv`, `laptop`, `phone`, `mug`, `bottle`, `book`, `clock`, `sign`
- **World & Environment**: `tree`, `house`, `cloud`, `flower`, `car`
- **Treasures & Props**: `chest`, `coins`, `key`, `sword`, `shield`, `umbrella`, `bag`
- **Costumes**: `glasses`, `tie`, `belt`, `cap`, `crown`, `helmet`, `cape`, `backpack`

---

## 3. Contact & Holding Things (Connection Law)
Attach held items directly to character slots so they follow limb rotation naturally:
```javascript
const mug = GK.P.mug(dummyG, {});
hero.attach(mug, 'handR', { x: 0, y: 14, rot: 0, s: 0.8 });
hero.hand(tl, t, 'R', 'grip');
```

---

## 2. Anatomical Hierarchy (Welded Bone System)

To prevent floating heads or separated limbs during jumps, laughs, or run cycles:
```
ROOT (<g id="char-ROOT">)
 ├── Dynamic Perspective Shadow (<ellipse rx="65" ry="15">)
 ├── Legs Group (<g id="legs">)
 │    ├── Left Leg (Hip -> Thigh -> Knee -> Shin -> Ankle -> Detailed Shoe)
 │    └── Right Leg (Hip -> Thigh -> Knee -> Shin -> Ankle -> Detailed Shoe)
 └── Torso Group (<g id="torso">)
      ├── Spine (<line stroke-width="10">)
      ├── Clothing / Vest / Armor (<rect> or <path> over torso)
      ├── Left Arm (Shoulder -> Upper Arm -> Elbow -> Forearm -> Wrist -> Hand + Fingers)
      ├── Right Arm (Shoulder -> Upper Arm -> Elbow -> Forearm -> Wrist -> Hand + Fingers)
      └── Neck & Head Group (<g id="neck">)
           ├── Neck Bridge Collar (<rect fill="skin">) -- WELD LOCK
           ├── Neck Line (<line stroke-width="8">)
           └── Head (<g id="head">)
                ├── Skull (<circle r="46">)
                ├── Hair / Hat / Helmet
                ├── Eyes (<circle r="6">) + Shines (<circle r="2.2">)
                ├── Eyebrows (<path stroke-width="4.5">) -- Emotion Engine
                └── Mouth (<path stroke-width="4.5">) -- Speech & Expression Engine
```

---

## 3. Facial Expression Matrix

| Emotion | Eyebrow Path Left | Eyebrow Path Right | Mouth Path | Eye Radius |
|---|---|---|---|---|
| **Neutral / Idle** | `M -26 -20 Q -16 -26 -6 -20` | `M 6 -20 Q 16 -26 26 -20` | `M -16 14 Q 0 24 16 14` | 6 |
| **Happy / Smile** | `M -26 -22 Q -16 -28 -6 -22` | `M 6 -22 Q 16 -28 26 -22` | `M -16 10 Q 0 28 16 10` | 6 |
| **Talking Wide** | Raised for stress | Raised for stress | `M -18 10 Q 0 32 18 10` | 6 |
| **Talking Half** | Normal | Normal | `M -14 12 Q 0 26 14 12` | 6 |
| **Shock / Horror** | `M -26 -32 Q -16 -40 -6 -32` | `M 6 -32 Q 16 -40 26 -32` | `M -16 8 Q 0 38 16 8` (Drop jaw) | 8 |
| **Puzzled / Thinking**| `M -26 -28 Q -16 -34 -6 -28` | `M 6 -16 Q 16 -20 26 -16` | `M -14 16 Q 0 16 14 16` | 6 (pupils shifted) |
| **Angry** | `M -26 -16 Q -16 -24 -6 -16` | `M 6 -16 Q 16 -24 26 -16` | `M -14 20 Q 0 16 14 20` | 5 |

---

## 4. Micro-Assets Catalogue

All props must be created via procedural SVG code:
1. **Detailed Shoes**: Rounded toe cap, laces, sole thickness, and contact shadow.
2. **Tables & Desks**: 3/4 perspective trapezoid surface, beveled front edge, dual legs with cross-brace, and shadow ellipse.
3. **Chairs & Stools**: Perspective seat plank, backrest with cross-slats, 4 tapered legs.
4. **Notice Boards & Posters**: Pinned parchment texture, headers, sketch outlines, drop shadow.
5. **Coin Stacks**: Layered gold ellipses with specular highlights.
6. **Candles / Torches**: Wax drip cylinders, flame path, radialGradient flickering glow halo.

---

## 5. Automated Verification Checklist for Agents

Every agent generating scenes in this project must run this check:
- [x] Does the character have a ground shadow ellipse anchored to the floor plane?
- [x] Is the head group parented inside the neck/torso hierarchy with a neck bridge?
- [x] Do walking characters oscillate thighs, shins, and arms in opposite phases?
- [x] Does speaking sync mouth path morphs every ~0.2s with the voiceover timestamps?
- [x] Do small assets (shoes, tables, chairs) have correct depth layering and shadows?
- [x] Does the camera maintain subtle continuous movement throughout?

