---
name: character-animation
description: >-
  GrowKaz master doctrine for drawing, rigging and animating stickman/toon characters and EVERY prop or
  scene asset (furniture, tools, vehicles, nature, weapons, food, buildings, clothing) as pure SVG code.
  Use this skill whenever a video needs a character that talks, walks, runs, dances, sits, points,
  emotes, holds objects, or any hand-built micro-asset (table, chair, shoe, mug, door, window, car, tree...).
  Always load BEFORE writing any character, pose, prop, background object or scene script, even for
  "simple" scenes, because it ships a tested rig (assets/rig.js) and prop kit (assets/props.js) that
  guarantee connected body parts, lip-sync, dance, walk cycles, IK hand-reach and consistent shading.
---

# Character & Asset Animation — Master Skill

**Files in this skill**

| File | What it is |
|---|---|
| `SKILL.md` | This doctrine (read fully once per project) |
| `assets/rig.js` | Tested rig: `GK.createCharacter`, poses, IK, walk/run, talk/lip-sync, dance, expressions, hands, attach |
| `assets/props.js` | Shading primitives + ~35 ready props + costumes (`GK.P.*`, `GK.costume.*`) |
| `assets/demo.html` | 12-second reference scene (walk-in, wave, talk, sit, dance). Copy its structure |

Inline both `.js` files into the scene HTML (or `<script src>` them). GSAP 3.12 from cdnjs is the only other dependency.

---

## 0. The non-negotiable workflow

```
READ beat -> WRITE manifest -> PICK rig/props -> BUILD on ONE master timeline -> VERIFY (checklist §12) -> render
```

Never start coding from the narration alone. For every beat fill this table first:

```
Beat | t0-t1 | Char(s)+view | x,floorY | pose -> pose | emotion | props (each with x,y,size) | enter/exit | camera
```

**100% rule:** every noun in the narration gets a visible element; every spoken number gets a counter/label/count of objects on screen; every verb gets a pose or motion.

---

## 1. Why the old rig broke (and what replaced it)

The v1 skeleton moved bones by editing `x2,y2` of `<line>`s while child groups kept hard-coded `translate()`s, so the shin detached from the thigh the moment a thigh was animated. **Never animate line endpoints.**
v2 is **forward-kinematics by rotation**: every bone is `translate(joint) -> rotate(angle)`, children live inside the parent's group, so limbs can not separate. Positions of bones never change, only angles.

---

## 2. Angle law, units, proportions

Memorise this; every pose number follows it (degrees, screen truth):

```
Limb bones hang along +y.     0 = down,  +90 = tip to screen-LEFT,  -90 = tip to screen-RIGHT,  +-180 = UP
spine / neck / head (up -y):  +deg leans toward screen-RIGHT
Elbow/knee: relative to parent. L = screen-left limb (front view) = NEAR limb (side view)
```

| Constant | px | Notes |
|---|---|---|
| `GK.cm(v)` | v*2.4 | 175 cm person = ~420 px tall |
| thigh / shin / foot | 95 / 90 / 18 | pelvis->sole `GK.GROUND` = 203 |
| upper arm / forearm | 62 / 56 | |
| spine / neck / head radius | 110 / 14 / 42 | head centre = 160 px above pelvis |
| walk stride | `GK.STRIDE` = 280 px per cycle | no foot sliding |

Real-world sizing for props (multiply by 2.4): door 200 cm, table 75 cm high, chair seat 42 cm (=102 px, matches sit pose), bed 45 cm, sofa seat 42 cm, mug 9 cm, phone 15 cm, laptop 2 cm thick closed, car 150 cm tall, tree 4-6 m, house wall 250 cm/floor. **Wrong scale is the #1 reason scenes feel amateur.**

---

## 3. Building characters

```js
const svg = document.querySelector('svg.stage');
const hero = GK.createCharacter(svg, {
  id:'hero', view:'front',          // 'front' (talking, gestures, sitting behind a desk) | 'side' (walk, run, sit on chair, dance)
  style:'toon',                     // 'toon' filled+outlined | 'stick' pure white-line stickman
  skin:'#fde0b5', shirt:'#2f6fed', pants:'#2b3445', shoe:'#3b2f2f',
  hair:'#2a2118', hairStyle:'short',// short|spiky|long|bald
  sleeves:'short',                  // short|long|none
  blush:false });
hero.place(300, 1500);              // x, floor y (feet land exactly here), optional 3rd arg = scale
```

**View choice rule:** walking, running, sitting on a chair, kicking, hopping => `view:'side'`. Facing the audience, talking, pointing, waving, shrugging => `view:'front'`. Same skeleton, same pose names.
`rig.face(tl, at, -1)` mirrors a character to face left (flip happens in the `flip` joint, so counter-flip any text you attached).

**Built-in structure (all welded):** `root > flip > pelvis > {legR, spine > {back slot, chest, torso slot, neck > head > face, arms}, legL}`.
Head is always inside the spine; neck rect overlaps both skull and torso; each bone draws `outline -> child -> fill` so elbow/knee seams are invisible.

**Slots** (append SVG here and it moves with the body part): `rig.slots.head`, `face`, `torso`, `back`, `handL`, `handR`, `footL`, `footR`.

---

## 4. Poses, IK and gestures

`rig.pose(tl, at, nameOrObject, dur=.4, ease, overrides)` tweens the **whole body** (missing keys fall back to idle, so poses never accumulate junk). `rig.part(tl, at, {keys}, dur)` tweens **only** the keys you pass.

Joint keys: `pelvisX pelvisY pelvisRot spine neck head  hipL kneeL ankleL hipR kneeR ankleR  shL elL wrL shR elR wrR`.

Special keys inside a pose object:

| Key | Meaning |
|---|---|
| `ikL:[x,y,bend?]` `ikR` | Hand goes to (x,y) in **spine space** (origin = pelvis, up = -y). Hand follows torso lean. Use for anything that must TOUCH something (chin, face, hips, phone, forehead, table, prop) |
| `plant:{drop,dx}` | Pelvis drops `drop` px and both feet stay glued to floor (crouch, squat, dance dip) |
| `sit:{seatH}` | Sits on a seat of that height (use with `view:'side'`; feet stay on floor via IK) |

Library (`GK.POSES`): `idle relaxed wave pointR pointL pointUp shrug shock cheer sad bow laugh thinking facepalm handsOnHips phone salute clap crouch sitSide hop1`.
Add project poses by `GK.POSES.myPose = {...}`; author with the angle law, then **render a still and look at it** before using it.

Checking contact: `rig.tip('R')` returns the stage position of the right hand; `rig.worldPoint('head',0,42)` the chin. Use these to place a held cup, a pointed-at sign, or to assert a hand touches a prop (distance < 20 px).

Two-bone IK directly: `GK.ik2(upperLen, foreLen, targetX, targetY, bend)` -> `{a1,a2}` degrees.

**Hands** (`rig.hand(tl, at, 'L'|'R', name, dur)`): `relaxed open fist grip point peace`. Hands are 5 fingers; every gesture needs a hand shape (point = `point`, holding = `grip`, wave = `open`, angry = `fist`).

### Wave / waggle recipe
```js
rig.pose(tl, 2.0, 'wave', .35, 'back.out(1.4)');  rig.hand(tl, 2.0, 'R', 'open');
for (let i=0;i<5;i++) rig.part(tl, 2.4+i*.22, {wrR: i%2? 18 : -18}, .22, 'sine.inOut');
rig.pose(tl, 3.6, 'idle', .3);
```

---

## 5. Faces and emotion

`rig.expr(tl, at, name, dur)`: `neutral happy laugh sad angry surprised scared thinking confused smug sleepy wink` (or pass your own `{brow, rotL, rotR, browYL, browYR, eye, eyeR, mouth, lookX, lookY}`).
Brow rotation: **inner end down = angry** (`rotL +, rotR -`), inner end up = sad/scared. Eyes: white sclera + pupil + highlight (never a black dot with white pupil).
Extras: `rig.look(tl, at, x, y)` (eyes follow targets: look at the prop being discussed), `rig.blink(tl, at)`, `rig.autoBlink(tl, from, to, seed)` (deterministic), `rig.breathe(tl, from, to)`.

Emotion must change **body + face + timing together**: shock = arms up + wide eyes + `wow` mouth + `pelvisY` recoil; sad = `spine 8, head 14` + frown + slow ease; anger = `fist` hands + `angry` brows + fast ease.

---

## 6. Talking & dialogue (lip-sync that reads)

```js
rig.talk(tl, [
  {w:'The',s:5.00,e:5.18}, {w:'THIEF',s:5.18,e:5.60,stress:true}, {w:'stole',s:5.60,e:5.95}, {w:'a',s:5.95,e:6.05}, {w:'shoe!',s:6.05,e:6.60}
], { base:'idle', arms:true, gestures:true });
```
- Each word is split into visemes by vowels/letters: a->`AA`, e,i->`EE`, o,u->`OO`, m,b,p->`MBP`, f,v->`FV`, mouth closes between words and rests after the last.
- Stressed words (`stress:true`, ALL CAPS, or ending `!`) raise eyebrows; every stressed word / 4th word gives a head nod and an alternating small arm beat. Pass `base:'sitSide'` (or the pose the body is currently in) so arms return to the right place, or `arms:false` while holding a prop.
- No word timing available: `rig.talkSimple(tl, from, to)`.
- Always add `rig.autoBlink`, `rig.breathe`, and `rig.look` toward the listener. A talking face with frozen eyes looks dead.

**Two-character dialogue:** left character `face(+1)`, right `face(-1)` (or build the right one and flip). Only the speaker runs `talk`; the listener gets `expr` reactions (nod = `head.y`, `thinking`, `surprised`) timed to the speaker's key words. Optional: dim listener to `opacity .75` while the other speaks.

---

## 7. Locomotion & dance

**Walk/run (side view):** 8-phase cycle (contact, recoil, passing, high, toe-off, swing lift, swing pass, reach) with opposite arm swing, pelvis bob, torso lean, foot angles.
```js
hero.place(-150, 1500); // off-screen left
let t = hero.walk(tl, 0.0, { toX: 600 });           // auto cycle count from distance, faces right
t = hero.walk(tl, t, { toX: 1300, run:true });      // run
hero.pose(tl, t, 'idle', .25);
```
Speed is locked to `GK.STRIDE` so feet do not slide; never retime a walk with a different `toX/duration` ratio than the cycle gives.

**Dance:** `rig.dance(tl, at, style, beats, bpm)` with `bounce | disco | sway | robot | party`. Use the music BPM from the audio skill; one pose per beat, arms alternate, `plant` keeps feet down. For a custom move, write one pose object per beat and call `rig.pose` at `t0 + i*60/bpm`.

**Jump / hop:** `rig.jump(tl, at, height, dur)` (shadow shrinks while airborne). One-leg hop: pose `hop1` + repeated `jump`.

**Sit on chair:** `view:'side'`; chair from `GK.P.chair(layer,{x,y,view:'side'})` (seat 102 px). Place character `x` on the seat's x, `y` = floor, then `rig.pose(tl,t,'sitSide',.5)`. Hands rest on lap by IK.

---

## 8. Holding things & wearing things (connection law)

Anything that touches a body part goes **into that part's slot**, never into the stage:
```js
const mug = GK.P.mug(document.createElementNS('http://www.w3.org/2000/svg','g'), {});
hero.attach(mug, 'handR', {x:0, y:14, rot:0, s:.8});   // follows wrist rotation forever
hero.hand(tl, t, 'R', 'grip');
```
Costumes: `GK.costume.glasses|tie|belt|cap|crown|helmet|cape|backpack(rig, color)`. `cape` returns a joint; tween `j.rot` (+-6 deg, finite) for flutter. Layer order inside the body: back slot -> torso -> clothes slot -> head -> arms, so a cape sits behind, a tie on the chest, a helmet on the skull.
Mirrored (`face -1`) characters flip attached text: put text on stage layers, not on attached props.

---

## 9. Building ANY asset (the method for "everything in the world")

Do not draw an object as one blob. Run this recipe for every asset, from a chair to a submarine:

1. **Identify the real size** (cm) and convert with `GK.cm`. Sits on ground -> origin bottom-centre.
2. **Decompose into primitives:** `P.box` (oblique block: lit front, lighter top, darker right), `P.cyl` (gradient barrel + cap ellipse), `P.ball` (radial gradient), `P.rect` (rounded), `path`, `polygon`, `ellipse`, `line`.
3. **Silhouette first** (readable at 10% size), then parts, then **three detail tiers**:
   - T1 structure: legs, panels, handles, hinges
   - T2 material: wood grain lines, metal rim highlight, glass transparency (`rgba` + white diagonal sheen), fabric stitch lines
   - T3 life: wear marks, steam, glow (`radialGradient`), cast shadow, reflections
4. **Shading law:** light from top-left. Lit side `shade(c,+.22)`, shadow side `shade(c,-.28)`, outline `#121824` 3-4 px (thicker for big props, 2 px for tiny).
5. **Contact shadow** under every grounded prop (`P.shadow`), stronger the closer to the ground.
6. **Moving parts get their own `GK.Joint`:** door panel, clock hands, car wheels, lamp shade, lid, drawer. Tween the joint, call nothing else (apply is automatic with `GK.tw`).
7. **State variants:** write the asset with parameters (`c, w, h, open, n`) so "three hundred right shoes" = a loop, not copy-paste.
8. Put the asset in `GK.P.<name>` style functions: `(parent, {x,y,s,...}) -> <g>` and return named sub-parts (`n.panel`, `n.hour`).

### Included props (`GK.P.*`)
Furniture/home: `table chair bed sofa lamp door window shelf tv laptop phone mug bottle book clock sign`
Nature/world: `tree house cloud flower car`
Items/treasure/weapons: `chest coins key sword shield umbrella bag`
Primitives: `box cyl ball rect text shadow`

### Blueprint cheat-sheet for everything else (compose from primitives)
| Object | Size cm | Recipe |
|---|---|---|
| Shoe | 28x10 | side path sole + upper + toe cap + lace lines + heel block + shine ellipse (see rig foot) |
| Bicycle | 170 long | 2 circles r=33 + spokes, diamond frame lines, handlebar, saddle, chain ellipse; wheels = Joints |
| Pot/pan | 25 | `cyl` + handle rect + inner ellipse darker + steam path |
| Plate/bowl | 25 | stacked ellipses (rim lighter, well darker); food = circles |
| Apple/fruit | 8 | `ball` + stem line + leaf path + highlight |
| Ladder | 200 | two rails + rungs every 30 cm |
| Boat | 400 | hull path + mast + sail triangle + water waves (sine path) |
| Rocket | 300 | long `cyl` + cone path + 3 fins + window circle + animated flame path |
| Bridge | any | planks rects + 2 arches (path arcs) + railings lines |
| Cat/dog/bird | 30-60 | body ellipse + head circle + ears + tail path + 4 stub legs (Joints for walk) |
| Fridge/oven | 180/85 | `box` + door seam lines + handle + inner shelves when open |
| Guitar | 100 | body figure-8 path + neck rect + sound-hole circle + 6 lines |
| Crowd | n/a | one character function + `GK.rng(seed)` for colour/height variety (no `Math.random`) |

---

## 10. Layers, frame, camera

```
bg layer -> back props -> shadows -> characters -> front occluders (table front, chair front, fence) -> FX -> subtitles
```
Safe frame 1080x1920: head close-up y 150-550; upper body: ROOT y~1000; full body: floor y 1650-1750; two-char x: left 220-320, right 760-860; keep props above y 1680 (subtitle zone below). Entry: slide in from x=-200 / 1280 with `walk`, never pop in. Camera never static: slow push-in `scale 1.06, 5s`, pan, punch-in on climax (see gsap-motion / motion-doctrine skills for recipes).
Table in front of a seated front-view character: draw character first, table second so the table front hides the legs.

---

## 11. Rendering/determinism rules (video pipelines scrub the timeline)

- **One master `gsap.timeline({paused:true})`.** Every motion is a `tl.to/fromTo` at an absolute time. No stand-alone `gsap.to`, no `setInterval`, no CSS animations.
- **No infinite loops** (`repeat:-1`). Write finite repeats (`for` loops that add tweens). Idle sway = breathe/blink helpers with `from,to`.
- **No `Math.random`.** Use `GK.rng(seed)`.
- Never use GSAP `rotation/transformOrigin` on rig parts (bbox-based origin bugs). Rig joints rotate around their own origin by design. Drive joints only with `rig.pose / part / expr / hand`, or `GK.tw(tl, joint, {rot:..}, dur, at)`.
- Render with the render-video skill by seeking the timeline per frame.

---

## 12. Quality checklist (run mentally and, where possible, on a still frame)

**Anatomy:** feet touch floor line exactly (check `place()`), shadow under every character, head/neck/torso joined, elbows and knees bend the natural way, no limb crosses subtitle zone, hands have a finger shape, eyes have highlights, mouth shape matches the sound.
**Motion:** nothing teleports (enter/exit with walk or tween), anticipation before big moves (small opposite motion 0.1 s), overshoot ease (`back.out`) on punches/waves, settle with `sine.inOut`, breathe + blink during any hold, stressed words trigger brow/nod.
**Script match:** every noun visible, every number shown as a counter or object count, emotion of face matches narration, listener reacts.
**Assets:** correct real-world scale, contact shadow, light from top-left, three detail tiers, moving parts are Joints, nothing uses image files.
**Polish:** background depth (gradient + glow + particles), consistent outline weight per distance, colour palette <= 6 hues per scene, text in Montserrat 900.

---

## 13. Common mistakes (v1 bugs and fixes)

| Mistake | Fix |
|---|---|
| Shin/forearm detaches when thigh is animated | Rotation rig only; never animate `x2,y2` |
| Ground shadow at hip height, feet floating | `place(x, floorY)` aligns sole to floor; shadow sits at `GK.GROUND` |
| Eyes = black dot with white pupil (dead look) | Use rig eyes (sclera + pupil + shine), `rig.look` |
| Walking looks like skating | Use `rig.walk` (locked stride) instead of tweening x separately |
| Door "rotationY" fails in SVG | Use `door.panel` joint: tween `sx` to .2 (+ small `rot` skew) |
| Held object floats | `attach` to `handR/handL` slot |
| Hand does not reach what it points at | Use `ikR:[x,y]` or `rig.worldPoint` to compute the target |
| Infinite loops break render | Finite loops only (section 11) |
| Props all the same size/flat | Section 2 sizes + section 9 shading law |
| Character faces wrong way in dialogue | `rig.face(tl,t,-1)` for the right-hand speaker |
| Text mirrored after flip | Keep text outside flipped groups |

---

## 14. Minimal scene skeleton

```html
<svg class="stage" viewBox="0 0 1080 1920" width="1080" height="1920"></svg>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="assets/rig.js"></script><script src="assets/props.js"></script>
<script>
const svg = document.querySelector('.stage'), tl = gsap.timeline({paused:true}), FLOOR = 1650;
const bg = GK.el('g',{},svg), mid = GK.el('g',{},svg), fg = GK.el('g',{},svg);
GK.P.table(bg,{x:760,y:FLOOR}); GK.P.window(bg,{x:300,y:900});
const a = GK.createCharacter(mid,{id:'a',view:'side'}); a.place(-150, FLOOR);
let t = a.walk(tl, 0, {toX: 420});
a.expr(tl, t, 'happy'); a.pose(tl, t, 'wave', .35); a.hand(tl, t, 'R', 'open');
a.talk(tl, [{w:'Hello',s:t+.3,e:t+.8},{w:'friends!',s:t+.8,e:t+1.4}], {arms:false});
a.autoBlink(tl, 0, 10); a.breathe(tl, t, t+6);
window.__tl = tl;   // renderer seeks this
</script>
```

Build, then **screenshot the still frames (start, mid-action, climax)**, look at them, and fix before rendering the video.

---

## 15. Integration with other skills

Backgrounds `procedural-backgrounds` | camera `gsap-motion`, `motion-doctrine` | captions `captions-overlay` | transitions `cut-the-curve`, `seam-craft` | render `render-video` | audio/BPM `video-sound` | palette `video-styles`.
