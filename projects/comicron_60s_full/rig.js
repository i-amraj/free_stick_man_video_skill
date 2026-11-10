/* GrowKaz RIG  v2  —  rotation-driven welded skeleton (SVG + GSAP)
 * Everything lives on ONE GSAP timeline -> seek-safe, deterministic, render-safe.
 * Angle law (screen truth, degrees):  bone drawn along +y.  0 = hangs DOWN,
 *   +90 = tip points screen-LEFT, -90 = tip points screen-RIGHT, +-180 = UP.
 *   spine/neck/head (drawn along -y): +deg leans toward screen-RIGHT.
 * Limb "L" = screen-left limb (front view) / NEAR limb (side view).
 */
(function (g) {
'use strict';
const GK = g.GK = g.GK || {};
const NS = 'http://www.w3.org/2000/svg', D2R = Math.PI / 180;

/* ───────── helpers ───────── */
GK.el = (tag, attrs, parent) => {
  const n = document.createElementNS(NS, tag);
  for (const k in (attrs || {})) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
};
const el = GK.el;
GK.shade = (hex, amt) => {                       // amt -1..1  (darken..lighten)
  let c = hex.replace('#', ''); if (c.length === 3) c = c.split('').map(x => x + x).join('');
  const n = parseInt(c, 16), f = v => Math.round(amt < 0 ? v * (1 + amt) : v + (255 - v) * amt);
  return '#' + [n >> 16, (n >> 8) & 255, n & 255].map(f).map(v => v.toString(16).padStart(2, '0')).join('');
};
GK.rng = seed => () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);  // deterministic random
GK.cm = v => v * 2.4;                            // 1 cm = 2.4 px  (character ≈ 175 cm ≈ 420 px)

GK.ik2 = (l1, l2, tx, ty, bend = 1) => {         // 2-bone IK, bones along +y; returns degrees
  const max = l1 + l2 - 0.01, min = Math.abs(l1 - l2) + 0.01;
  const d = Math.min(Math.max(Math.hypot(tx, ty), min), max), cl = v => Math.min(1, Math.max(-1, v));
  const phi = Math.atan2(-tx, ty);
  const a = Math.acos(cl((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)));
  const b = Math.acos(cl((l1 * l1 + l2 * l2 - d * d) / (2 * l1 * l2)));
  return { a1: (phi + bend * a) / D2R, a2: -bend * (Math.PI - b) / D2R };
};

class Joint {                                    // transform node: translate -> rotate -> scale
  constructor(parent, x = 0, y = 0) {
    this.parent = parent instanceof Joint ? parent : null;
    this.g = el('g', {}, parent instanceof Joint ? (parent.host || parent.g) : parent);
    this.x = x; this.y = y; this.rot = 0; this.sx = 1; this.sy = 1; this.apply();
  }
  apply() {
    this.g.setAttribute('transform',
      `translate(${this.x.toFixed(2)} ${this.y.toFixed(2)}) rotate(${this.rot.toFixed(2)}) scale(${this.sx.toFixed(3)} ${this.sy.toFixed(3)})`);
  }
  world(px = 0, py = 0) {                        // local point -> stage coords (includes all parents)
    let p = [px, py];
    for (let j = this; j; j = j.parent) {
      const r = j.rot * D2R, c = Math.cos(r), s = Math.sin(r), x = p[0] * j.sx, y = p[1] * j.sy;
      p = [j.x + x * c - y * s, j.y + x * s + y * c];
    }
    return p;
  }
}
GK.Joint = Joint;
GK.tw = (tl, j, vars, dur, at, ease) =>          // tween any Joint / plain object, re-applying transform
  tl.to(j, Object.assign({}, vars, { duration: Math.max(dur, 0.001), ease: ease || 'power2.inOut',
    onUpdate: j.apply ? () => j.apply() : (j.onUp ? () => j.onUp() : undefined) }), at);

/* ───────── constants ───────── */
const DIM = GK.DIM = { thigh: 95, shin: 90, foot: 18, upper: 62, fore: 56, spine: 110, neck: 14, headR: 42, hipW: 14, shW: 28 };
const G = GK.GROUND = DIM.thigh + DIM.shin + DIM.foot;     // pelvis -> sole = 203 px
GK.STRIDE = 280;                                 // px travelled per full walk cycle (no foot-slide)

const VIS = GK.VISEMES = {                       // mouth shapes {half-width, corner-y, upper-ctrl, lower-ctrl}
  neutral: { w: 11, cy: 13, up: 13, dn: 13 },  rest: { w: 13, cy: 11, up: 19, dn: 19 },
  smile: { w: 16, cy: 9, up: 22, dn: 22 },     grin: { w: 18, cy: 8, up: 12, dn: 30 },
  frown: { w: 12, cy: 17, up: 8, dn: 8 },      MBP: { w: 10, cy: 13, up: 13, dn: 13 },
  AA: { w: 15, cy: 9, up: 8, dn: 38 },         EE: { w: 18, cy: 10, up: 12, dn: 23 },
  OO: { w: 7, cy: 13, up: 5, dn: 32 },         FV: { w: 13, cy: 12, up: 11, dn: 17 },
  wow: { w: 10, cy: 8, up: 0, dn: 42 },        laugh: { w: 19, cy: 7, up: 9, dn: 40 }
};
const EXPR = GK.EXPRESSIONS = {                  // brow y/rot, eye openness, mouth, look
  neutral:  { brow: 0, rotL: 0, rotR: 0, eye: 1, mouth: 'rest' },
  happy:    { brow: -3, rotL: -4, rotR: 4, eye: .92, mouth: 'smile' },
  laugh:    { brow: -5, rotL: -6, rotR: 6, eye: .45, mouth: 'laugh' },
  sad:      { brow: 2, rotL: -16, rotR: 16, eye: .8, mouth: 'frown', lookY: 2 },
  angry:    { brow: 3, rotL: 18, rotR: -18, eye: .72, mouth: 'frown' },
  surprised:{ brow: -9, rotL: 0, rotR: 0, eye: 1.25, mouth: 'wow' },
  scared:   { brow: -7, rotL: -12, rotR: 12, eye: 1.2, mouth: 'wow' },
  thinking: { browYL: -7, browYR: 0, rotL: 0, rotR: -8, eye: .9, mouth: 'neutral', lookX: -3, lookY: -3 },
  confused: { browYL: -6, browYR: 3, rotL: -8, rotR: -6, eye: 1, mouth: 'frown' },
  smug:     { browYL: -4, browYR: 1, rotL: 6, rotR: -4, eye: .62, mouth: 'smile' },
  sleepy:   { brow: 2, rotL: 0, rotR: 0, eye: .18, mouth: 'neutral' },
  wink:     { brow: -2, rotL: 0, rotR: 0, eye: 1, eyeR: .08, mouth: 'grin' }
};

/* every pose = FULL set (missing keys fall back to IDLE) — screen-truth degrees */
const IDLE = { pelvisX: 0, pelvisY: 0, pelvisRot: 0, spine: 0, neck: 0, head: 0,
  hipL: 3, kneeL: 0, ankleL: 0, hipR: -3, kneeR: 0, ankleR: 0,
  shL: 7, elL: -8, wrL: 0, shR: -7, elR: 8, wrR: 0 };
const POSES = GK.POSES = {
  idle: {},
  relaxed: { pelvisX: 4, hipL: 2, hipR: -9, kneeR: 4, spine: -2, head: 3, shL: 10, shR: -5 },
  wave: { shR: -100, elR: -80, spine: -2, head: 4 },
  pointR: { shR: -90, elR: 0, spine: 2 },   pointL: { shL: 90, elL: 0, spine: -2 },
  pointUp: { shR: -172, elR: -4 },
  shrug: { shL: 30, elL: 80, shR: -30, elR: -80, head: 4 },
  shock: { shL: 140, elL: 20, shR: -140, elR: -20, hipL: 8, hipR: -8, spine: -4, pelvisY: 4 },
  cheer: { shL: 165, elL: 10, shR: -165, elR: -10, spine: -3, head: -4 },
  sad: { spine: 8, head: 14, shL: 3, shR: -3, elL: -3, elR: 3 },
  bow: { spine: 35, head: 10, shL: 4, shR: -4 },
  laugh: { spine: 14, head: 8, ikL: [-14, -62], ikR: [14, -62], pelvisY: 3 },
  thinking: { head: -6, ikR: [8, -122], shL: 5 },
  facepalm: { head: 10, spine: 6, ikR: [0, -150] },
  handsOnHips: { ikL: [-30, -22], ikR: [30, -22] },
  phone: { head: 6, ikR: [32, -150], shL: 6 },
  salute: { ikR: [24, -182] },
  clap: { ikL: [-4, -72], ikR: [4, -72] },
  crouch: { plant: { drop: 60, dx: 40 }, spine: 18, head: -10, ikL: [-30, -40], ikR: [30, -40] },
  sitSide: { sit: { seatH: 102 }, ikL: [40, -16, 1], ikR: [48, -16, 1], spine: -2 },
  hop1: { hipR: 28, kneeR: 72, hipL: -4 }
};

/* WALK: 8 key phases for the near leg (side view, facing +x).  Far leg = phase+4.
 * [hip, knee, ankle]  hip<0 = leg forward.  bob = pelvis y.  */
const WALK = [[-28, 5, -14], [-20, 20, 0], [-4, 8, 0], [12, 4, 4], [26, 14, 26], [14, 60, 10], [-8, 62, 0], [-26, 22, -10]];
const BOB = [3, 8, -2, -6, 3, 8, -2, -6];

/* HANDS: [angle, length] for [thumb,index,middle,ring,pinky]; +angle = toward thumb side */
const HANDS = GK.HANDS = {
  relaxed: [[25, 8], [6, 9], [0, 10], [-5, 9], [-10, 8]],
  open:    [[45, 10], [10, 12], [0, 13], [-8, 12], [-16, 10]],
  fist:    [[-25, 5], [0, 4], [0, 4], [0, 4], [0, 4]],
  grip:    [[-10, 6], [0, 6], [0, 6], [0, 6], [0, 6]],
  point:   [[-20, 5], [0, 18], [0, 4], [0, 4], [0, 4]],
  peace:   [[-20, 5], [8, 16], [-8, 16], [0, 4], [0, 4]]
};

/* ───────── the character factory ───────── */
const DEF = { id: 'c', view: 'front', style: 'toon', skin: '#fde0b5', shirt: '#2f6fed', pants: '#2b3445',
  shoe: '#3b2f2f', hair: '#2a2118', hairStyle: 'short', outline: '#121824', line: '#f8fafc', ow: 3.2,
  limbW: 12, sleeves: 'short', blush: false };

GK.createCharacter = function (parent, opts) {
  const o = Object.assign({}, DEF, opts), side = o.view === 'side', stick = o.style === 'stick';
  const rig = { o, J: {}, slots: {}, groundY: G, _x: 0 };
  const J = rig.J, S = (w) => ({ stroke: o.outline, 'stroke-width': w == null ? o.ow : w, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' });
  const dark = (c, s) => (side && s === 'R') ? GK.shade(c, -0.22) : c;

  const root = J.root = new Joint(parent); root.g.setAttribute('id', o.id + '-ROOT');
  const shadow = rig.shadow = el('ellipse', { cx: 0, cy: G + 3, rx: 56, ry: 11, fill: 'rgba(0,0,0,.33)' }, root.g);
  const flip = J.flip = new Joint(root); const pelvis = J.pelvis = new Joint(flip);

  const bone = (par, x, y, len, w, col) => {     // outline -> child host -> fill  (seamless joints)
    const j = new Joint(par, x, y);
    if (!stick) el('line', Object.assign({ x1: 0, y1: 0, x2: 0, y2: len }, S(w + o.ow * 2)), j.g);
    j.host = el('g', {}, j.g);
    el('line', stick ? { x1: 0, y1: 0, x2: 0, y2: len, stroke: o.line, 'stroke-width': 8, 'stroke-linecap': 'round' }
      : { x1: 0, y1: 0, x2: 0, y2: len, stroke: col, 'stroke-width': w, 'stroke-linecap': 'round' }, j.g);
    return j;
  };

  /* LEG */
  const leg = s => {
    const sg = s === 'L' ? -1 : 1, hx = side ? 3 : DIM.hipW;
    const hip = J['hip' + s] = bone(pelvis, sg * hx, 0, DIM.thigh, o.limbW + 3, dark(o.pants, s));
    const knee = J['knee' + s] = bone(hip, 0, DIM.thigh, DIM.shin, o.limbW + 1, dark(o.pants, s));
    const ank = J['ankle' + s] = new Joint(knee, 0, DIM.shin); rig.slots['foot' + s] = ank.g;
    const sh = dark(o.shoe, s);
    if (side) {
      el('path', Object.assign({ d: 'M -11 -4 L 7 -4 Q 22 -2 31 10 L 31 16 L -14 16 Q -16 6 -11 -4 Z', fill: sh }, S(2.8)), ank.g);
      el('rect', { x: -14, y: 13, width: 45, height: 5, rx: 2, fill: GK.shade(sh, -.45), stroke: o.outline, 'stroke-width': 2 }, ank.g);
      el('path', { d: 'M 14 2 Q 22 4 26 10', stroke: GK.shade(sh, .5), 'stroke-width': 2, fill: 'none', 'stroke-linecap': 'round' }, ank.g);
    } else {
      el('ellipse', Object.assign({ cx: sg * 6, cy: 9, rx: 15, ry: 9, fill: sh }, S(2.8)), ank.g);
      el('rect', { x: sg * 6 - 15, y: 13, width: 30, height: 4, rx: 2, fill: GK.shade(sh, -.45) }, ank.g);
      el('ellipse', { cx: sg * 6, cy: 6, rx: 7, ry: 3, fill: GK.shade(sh, .45), opacity: .55 }, ank.g);
    }
  };

  /* ARM + HAND */
  const arm = (s, par) => {
    const sg = s === 'L' ? -1 : 1, sx = side ? 4 : DIM.shW;
    const sleeveC = o.sleeves === 'none' ? o.skin : o.shirt, foreC = o.sleeves === 'long' ? o.shirt : o.skin;
    const sh = J['sh' + s] = bone(par, sg * sx, -(DIM.spine - 10), DIM.upper, o.limbW, dark(sleeveC, s));
    const el_ = J['el' + s] = bone(sh, 0, DIM.upper, DIM.fore, o.limbW - 1, dark(foreC, s));
    const wr = J['wr' + s] = new Joint(el_, 0, DIM.fore); rig.slots['hand' + s] = wr.g;
    const skin = dark(o.skin, s), ts = s === 'L' ? 1 : -1;      // thumb side
    el('circle', Object.assign({ cx: 0, cy: 7, r: 9, fill: skin }, S(2.6)), wr.g);
    const fingers = [];
    for (let i = 0; i < 5; i++) {
      const bx = i === 0 ? ts * 8 : ts * (6 - (i - 1) * 4), by = i === 0 ? 4 : 11;
      const outl = stick ? null : el('line', Object.assign({ x1: bx, y1: by, x2: bx, y2: by }, S(5)), wr.g);
      const fl = el('line', { x1: bx, y1: by, x2: bx, y2: by, stroke: stick ? o.line : skin, 'stroke-width': stick ? 3 : 2.6, 'stroke-linecap': 'round' }, wr.g);
      fingers.push({ bx, by, a: 0, l: 5, outl, fl });
    }
    const hand = { fingers, ts, draw() { fingers.forEach(f => {
      const x2 = f.bx + f.l * Math.sin(f.a * D2R * ts), y2 = f.by + f.l * Math.cos(f.a * D2R);
      [f.outl, f.fl].forEach(n => n && (n.setAttribute('x2', x2.toFixed(2)), n.setAttribute('y2', y2.toFixed(2)))); }); } };
    rig['hand' + s] = hand; hand.set = (name) => { HANDS[name].forEach((v, i) => { fingers[i].a = v[0]; fingers[i].l = v[1]; }); hand.draw(); };
    hand.set('relaxed');
  };

  /* BACK slot, LEGS (far first), SPINE */
  leg('R');
  const spine = J.spine = new Joint(pelvis);
  rig.slots.back = el('g', {}, spine.g);
  if (side) arm('R', spine);
  const chest = J.chest = new Joint(spine);
  if (stick) el('line', { x1: 0, y1: 0, x2: 0, y2: -DIM.spine, stroke: o.line, 'stroke-width': 9, 'stroke-linecap': 'round' }, chest.g);
  else {
    const sw = side ? 17 : 30, ww = side ? 15 : 21;
    el('path', Object.assign({ d: `M ${-sw} -98 Q ${-sw} -110 ${-sw + 12} -110 L ${sw - 12} -110 Q ${sw} -110 ${sw} -98 L ${ww} -4 Q 0 9 ${-ww} -4 Z`, fill: o.shirt }, S()), chest.g);
    el('path', { d: `M ${-sw + 6} -92 Q 0 -86 ${sw - 6} -92`, stroke: GK.shade(o.shirt, .3), 'stroke-width': 2, fill: 'none', opacity: .5 }, chest.g);   // chest highlight
    el('rect', { x: -ww, y: -9, width: ww * 2, height: 9, rx: 3, fill: GK.shade(o.pants, -.1), stroke: o.outline, 'stroke-width': 2.4 }, chest.g);                 // waistband
  }
  rig.slots.torso = el('g', {}, spine.g);
  /* NECK + HEAD — welded inside spine */
  const neck = J.neck = new Joint(spine, 0, -DIM.spine);
  el('rect', Object.assign({ x: -9, y: -26, width: 18, height: 32, rx: 8, fill: o.skin }, stick ? { stroke: 'none' } : S(2.4)), neck.g);
  el('rect', { x: -7, y: -24, width: 14, height: 28, rx: 6, fill: o.skin }, neck.g);                                           // hides rect outline overlap
  const head = J.head = new Joint(neck, 0, -(DIM.neck + DIM.headR - 6));
  const hg = head.g, R = DIM.headR;
  const hairPath = {
    short: `M -43 -4 Q -50 -50 0 -52 Q 50 -50 43 -4 Q 32 -28 0 -29 Q -32 -28 -43 -4 Z`,
    spiky: `M -43 -4 L -46 -40 L -29 -34 L -25 -60 L -11 -43 L 0 -68 L 11 -43 L 25 -60 L 29 -34 L 46 -40 L 43 -4 Q 32 -28 0 -29 Q -32 -28 -43 -4 Z`,
    long: `M -43 -4 Q -50 -50 0 -52 Q 50 -50 43 -4 Q 32 -28 0 -29 Q -32 -28 -43 -4 Z`,
    bald: null };
  if (o.hairStyle === 'long') el('path', Object.assign({ d: 'M -47 -8 Q -54 44 -36 66 L 36 66 Q 54 44 47 -8 Q 40 -52 0 -52 Q -40 -52 -47 -8 Z', fill: GK.shade(o.hair, -.15) }, S(2.8)), hg);
  if (!side) [-1, 1].forEach(s => el('ellipse', Object.assign({ cx: s * (R + 1), cy: 2, rx: 6, ry: 9, fill: o.skin }, S(2.6)), hg));
  el('circle', Object.assign({ cx: 0, cy: 0, r: R, fill: o.skin }, S(stick ? 5 : 4.2)), hg);
  if (side) el('ellipse', Object.assign({ cx: -8, cy: 4, rx: 6, ry: 9, fill: o.skin }, S(2.6)), hg);
  if (side) el('path', Object.assign({ d: 'M 40 4 Q 54 12 40 18', fill: o.skin }, S(3)), hg);                                    // nose bump
  /* FACE */
  const faceX = side ? 0 : 0, face = new Joint(head, faceX, 0); rig.slots.face = face.g;
  const mk = (x, y) => new Joint(face, x, y);
  const eyeAt = (x, y, s) => {
    const e = new Joint(face, x, y);
    el('ellipse', Object.assign({ cx: 0, cy: 0, rx: 8.5, ry: 9.5, fill: '#fff' }, S(2.2)), e.g);
    const pu = new Joint(e, 0, 0); el('circle', { cx: 0, cy: 0, r: 4.7, fill: o.outline }, pu.g);
    el('circle', { cx: 1.6, cy: -1.8, r: 1.6, fill: '#fff' }, pu.g); e.pupil = pu; return e;
  };
  const browAt = (x, y) => { const b = new Joint(face, x, y); el('line', Object.assign({ x1: -9, y1: 0, x2: 9, y2: 0 }, S(4.2)), b.g); b.by = y; return b; };
  if (side) { J.eyeL = eyeAt(17, -4); J.eyeR = null; J.browL = browAt(17, -20); J.browR = null; }
  else { J.eyeL = eyeAt(-15, -4); J.eyeR = eyeAt(15, -4); J.browL = browAt(-15, -20); J.browR = browAt(15, -20); }
  if (o.blush) [-1, 1].forEach(s => el('ellipse', { cx: s * 26 + (side ? 12 : 0), cy: 10, rx: 7, ry: 4, fill: '#f87171', opacity: .35 }, face.g));
  const mouthJ = new Joint(face, side ? 22 : 0, 16); if (side) mouthJ.sx = .8;
  const mp = el('path', Object.assign({ d: '', fill: '#5a1515' }, S(3)), mouthJ.g);
  const M = rig.mouth = { w: 13, cy: 11, up: 19, dn: 19, onUp() { mp.setAttribute('d', `M ${-this.w} ${this.cy} Q 0 ${this.up} ${this.w} ${this.cy} Q 0 ${this.dn} ${-this.w} ${this.cy} Z`); mouthJ.apply(); } };
  M.onUp();
  if (!side) el('circle', { cx: 0, cy: 7, r: 2.2, fill: o.outline, opacity: .45 }, face.g);                                    // nose dot
  /* hair front */
  if (hairPath[o.hairStyle]) el('path', Object.assign({ d: hairPath[o.hairStyle], fill: o.hair }, S(stick ? 3 : 3)), hg);
  rig.slots.head = hg;
  if (!side) arm('R', spine);            // front view: both arms drawn AFTER head (hands can cover the face)
  arm('L', spine);
  leg('L');                              // near leg last

  /* eyes state: look, blink */
  const eyes = () => [J.eyeL, J.eyeR].filter(Boolean);
  rig.look = (tl, at, x, y, dur = .2) => { eyes().forEach(e => GK.tw(tl, e.pupil, { x: x, y: y }, dur, at)); return at + dur; };
  rig.blink = (tl, at, d = .12) => { eyes().forEach(e => { tl.to(e, { sy: .08, duration: d / 2, ease: 'sine.in', onUpdate: () => e.apply() }, at);
    tl.to(e, { sy: 1, duration: d / 2, ease: 'sine.out', onUpdate: () => e.apply() }, at + d / 2); }); return at + d; };
  rig.autoBlink = (tl, from, to, seed = 7) => { const r = GK.rng(seed); for (let t = from + 1 + r() * 2; t < to; t += 2 + r() * 3) rig.blink(tl, t); };

  /* expression */
  rig.expr = (tl, at, name, dur = .25) => {
    const e = Object.assign({ brow: 0, rotL: 0, rotR: 0, eye: 1, lookX: 0, lookY: 0 }, EXPR[name] || name);
    const bl = e.browYL != null ? e.browYL : e.brow, br = e.browYR != null ? e.browYR : e.brow;
    if (J.browL) GK.tw(tl, J.browL, { y: J.browL.by + bl, rot: e.rotL }, dur, at);
    if (J.browR) GK.tw(tl, J.browR, { y: J.browR.by + br, rot: e.rotR }, dur, at);
    if (J.eyeL) GK.tw(tl, J.eyeL, { sy: e.eye }, dur, at);
    if (J.eyeR) GK.tw(tl, J.eyeR, { sy: e.eyeR != null ? e.eyeR : e.eye }, dur, at);
    eyes().forEach(x => GK.tw(tl, x.pupil, { x: e.lookX, y: e.lookY }, dur, at));
    rig.viseme(tl, at, e.mouth, dur); return at + dur;
  };
  rig.viseme = (tl, at, name, dur = .08) => { const v = VIS[name] || name;
    tl.to(M, { w: v.w, cy: v.cy, up: v.up, dn: v.dn, duration: Math.max(dur, .001), ease: 'sine.inOut', onUpdate: () => M.onUp() }, at); return at + dur; };

  /* hands */
  rig.hand = (tl, at, sideKey, name, dur = .15) => {
    const h = rig['hand' + sideKey], tgt = HANDS[name];
    h.fingers.forEach((f, i) => tl.to(f, { a: tgt[i][0], l: tgt[i][1], duration: Math.max(dur, .001), ease: 'sine.inOut', onUpdate: () => h.draw() }, at));
    return at + dur;
  };

  /* POSE (with IK / planted feet / sitting) */
  const armBend = s => side ? 1 : (s === 'L' ? 1 : -1), legBend = s => side ? -1 : (s === 'L' ? 1 : -1);
  const TARGET = { pelvisX: [pelvis, 'x'], pelvisY: [pelvis, 'y'], pelvisRot: [pelvis, 'rot'], spine: [spine, 'rot'], neck: [neck, 'rot'], head: [head, 'rot'] };
  ['hip', 'knee', 'ankle', 'sh', 'el', 'wr'].forEach(k => ['L', 'R'].forEach(s => TARGET[k + s] = [J[k + s], 'rot']));
  rig.resolve = (name, over) => {
    const P = Object.assign({}, IDLE, typeof name === 'string' ? POSES[name] : name, over || {});
    ['L', 'R'].forEach(s => { const ik = P['ik' + s]; if (ik) {                    // hand target in SPINE space
      const sh = J['sh' + s], r = GK.ik2(DIM.upper, DIM.fore, ik[0] - sh.x, ik[1] - sh.y, ik[2] || armBend(s));
      P['sh' + s] = r.a1; P['el' + s] = r.a2; } });
    let drop = null, dx = side ? 20 : 34;
    if (P.plant) { drop = P.plant.drop; dx = P.plant.dx != null ? P.plant.dx : dx; }
    if (P.sit) { drop = G - (P.sit.seatH + 6); dx = P.sit.footX || 70; }
    if (drop != null) { P.pelvisY = drop;
      ['L', 'R'].forEach(s => { const sg = s === 'L' ? -1 : 1, hx = J['hip' + s].x;
        const fx = side ? (P.sit ? dx : dx * (s === 'L' ? -.3 : .3)) : sg * dx;
        const r = GK.ik2(DIM.thigh, DIM.shin, fx - hx, G - drop - DIM.foot, legBend(s));
        P['hip' + s] = r.a1; P['knee' + s] = r.a2; P['ankle' + s] = -(r.a1 + r.a2); }); }
    return P;
  };
  rig.pose = (tl, at, name, dur = .4, ease = 'power2.inOut', over) => {
    const P = rig.resolve(name, over), by = new Map();
    for (const k in TARGET) { const [j, p] = TARGET[k]; if (P[k] == null || !j) continue; if (!by.has(j)) by.set(j, {}); by.get(j)[p] = P[k]; }
    by.forEach((vars, j) => GK.tw(tl, j, vars, dur, at, ease)); return at + dur;
  };

  rig.part = (tl, at, obj, dur = .2, ease = 'power2.inOut') => {      // animate ONLY the given keys (supports ikL/ikR)
    const P = Object.assign({}, obj);
    ['L', 'R'].forEach(s => { const ik = P['ik' + s]; if (ik) { const sh = J['sh' + s], r = GK.ik2(DIM.upper, DIM.fore, ik[0] - sh.x, ik[1] - sh.y, ik[2] || armBend(s)); P['sh' + s] = r.a1; P['el' + s] = r.a2; } });
    const by = new Map();
    for (const k in TARGET) { const [j, p] = TARGET[k]; if (P[k] == null) continue; if (!by.has(j)) by.set(j, {}); by.get(j)[p] = P[k]; }
    by.forEach((vars, j) => GK.tw(tl, j, vars, dur, at, ease)); return at + dur; };

  /* placement / facing / jump */
  rig.place = (x, floorY, scale = 1) => { root.x = x; root.y = floorY - G * scale; root.sx = root.sy = scale; root.apply(); rig._x = x; rig._floor = floorY; return rig; };
  rig.face = (tl, at, dir, dur = .12) => GK.tw(tl, flip, { sx: dir < 0 ? -1 : 1 }, dur, at, 'sine.inOut');
  rig.moveTo = (tl, at, x, dur, ease = 'none') => { tl.fromTo(root, { x: rig._x }, { x, duration: dur, ease, onUpdate: () => root.apply() }, at); rig._x = x; return at + dur; };
  rig.jump = (tl, at, h = 60, dur = .5) => {
    tl.to(pelvis, { y: -h, duration: dur / 2, ease: 'power2.out', onUpdate: () => pelvis.apply() }, at);
    tl.to(pelvis, { y: 0, duration: dur / 2, ease: 'power2.in', onUpdate: () => pelvis.apply() }, at + dur / 2);
    tl.to(shadow, { attr: { rx: 40, opacity: .5 }, duration: dur / 2, ease: 'power2.out' }, at);
    tl.to(shadow, { attr: { rx: 56, opacity: 1 }, duration: dur / 2, ease: 'power2.in' }, at + dur / 2); return at + dur; };

  /* WALK / RUN (side view)  — returns end time */
  rig.walk = (tl, at, w = {}) => {
    const run = !!w.run, amp = run ? 1.5 : 1, period = w.period || (run ? .62 : 1), stride = GK.STRIDE * (run ? 1.4 : 1);
    const dx = w.toX != null ? w.toX - rig._x : 0;
    const n = w.cycles || Math.max(1, Math.round(Math.abs(dx) / stride)), step = period / 8, total = n * period;
    if (dx) rig.face(tl, at, dx, .08);
    for (let c = 0; c < n; c++) for (let i = 0; i < 8; i++) {
      const t = at + (c * 8 + i) * step, a = WALK[i], b = WALK[(i + 4) % 8], P = {};
      P.hipL = a[0] * amp; P.kneeL = a[1] * amp * (run ? 1.15 : 1); P.ankleL = a[2];
      P.hipR = b[0] * amp; P.kneeR = b[1] * amp * (run ? 1.15 : 1); P.ankleR = b[2];
      P.shL = -P.hipL * (run ? 1.3 : .9); P.shR = -P.hipR * (run ? 1.3 : .9);
      P.elL = -(run ? 75 : 20) - Math.abs(P.shL) * .3; P.elR = -(run ? 75 : 20) - Math.abs(P.shR) * .3;
      P.spine = run ? 12 : 3; P.head = -P.spine * .5; P.pelvisY = BOB[i] * amp * (run ? 1.4 : 1);
      rig.pose(tl, t, P, step, 'sine.inOut');
    }
    if (dx) rig.moveTo(tl, at, rig._x + dx, total, 'none');
    return at + total;
  };

  /* TALK — words:[{w,s,e,stress?}] absolute seconds on the timeline */
  rig.talk = (tl, words, t = {}) => {
    const gest = t.gestures !== false, V = { a: 'AA', e: 'EE', i: 'EE', o: 'OO', u: 'OO', m: 'MBP', b: 'MBP', p: 'MBP', f: 'FV', v: 'FV' };
    words.forEach((w, wi) => {
      const seq = [...w.w.toLowerCase()].map(ch => V[ch]).filter(Boolean); if (!seq.length) seq.push('EE');
      const slot = (w.e - w.s) / seq.length;
      seq.forEach((v, k) => rig.viseme(tl, w.s + k * slot, v, Math.min(.12, slot * .8)));
      rig.viseme(tl, w.e, 'MBP', .06);
      const stressed = w.stress || /[!A-Z]{2,}|!$/.test(w.w);
      if (stressed) { J.browL && GK.tw(tl, J.browL, { y: J.browL.by - 5 }, .1, w.s); J.browR && GK.tw(tl, J.browR, { y: J.browR.by - 5 }, .1, w.s);
        J.browL && GK.tw(tl, J.browL, { y: J.browL.by }, .15, w.s + .2); J.browR && GK.tw(tl, J.browR, { y: J.browR.by }, .15, w.s + .2); }
      if (gest && (stressed || wi % 4 === 3)) { GK.tw(tl, head, { y: head.y + 4 }, .08, w.s); GK.tw(tl, head, { y: head.y }, .14, w.s + .1);
        if (t.arms !== false) { const k = wi % 2 ? 'R' : 'L', sg = k === 'L' ? 1 : -1;
          const B = rig.resolve(t.base || 'idle');
          rig.part(tl, w.s, { ['sh' + k]: sg * 38, ['el' + k]: -sg * 40 }, .15);
          rig.part(tl, w.s + .25, { ['sh' + k]: B['sh' + k], ['el' + k]: B['el' + k] }, .3); } }
    });
    if (words.length) rig.viseme(tl, words[words.length - 1].e + .08, 'rest', .12);
  };
  rig.talkSimple = (tl, from, to, per = .22) => {                 // no word timing: cycle mouth
    const seq = ['AA', 'EE', 'MBP', 'OO', 'EE', 'AA']; let k = 0;
    for (let t = from; t < to - per; t += per) rig.viseme(tl, t, seq[k++ % seq.length], .09);
    rig.viseme(tl, to, 'rest', .1);
  };

  /* BREATHE (finite!) */
  rig.breathe = (tl, from, to, period = 3) => { for (let t = from; t < to; t += period) {
    tl.to(chest, { sy: 1.025, duration: period / 2, ease: 'sine.inOut', onUpdate: () => chest.apply() }, t);
    tl.to(chest, { sy: 1, duration: period / 2, ease: 'sine.inOut', onUpdate: () => chest.apply() }, t + period / 2); } };

  /* DANCE — styles: bounce | disco | sway | robot | party ; returns end time */
  rig.dance = (tl, at, style = 'bounce', beats = 8, bpm = 120) => {
    const b = 60 / bpm; let t = at;
    for (let i = 0; i < beats; i++, t += b) {
      const L = i % 2 === 0, k = L ? 1 : -1;
      const base = { bounce: { plant: { drop: L ? 20 : 4, dx: 36 }, shL: 40 * k + 20, shR: -40 * k - 20, elL: -50, elR: 50, spine: 4 * k, head: -6 * k },
        disco: { pelvisX: 12 * k, spine: 6 * k, hipL: 8, hipR: -8, ...(L ? { shR: -165, elR: -6, shL: 15, elL: -60 } : { shL: 165, elL: 6, shR: -15, elR: 60 }), head: 10 * k },
        sway: { pelvisX: 18 * k, spine: -8 * k, head: 8 * k, shL: 40 + 20 * k, shR: -40 + 20 * k, elL: -20, elR: 20, hipL: 3 + 6 * k, hipR: -3 + 6 * k },
        robot: { spine: 0, head: 0, shL: L ? 90 : 30, elL: L ? 90 : -90, shR: L ? -30 : -90, elR: L ? 90 : 90, hipL: 6, hipR: -6 },
        party: { pelvisY: L ? -10 : 6, shL: 150, elL: 10 * k, shR: -150, elR: -10 * k, hipL: 10 + 8 * k, hipR: -10 + 8 * k, spine: 5 * k, head: -8 * k } }[style];
      rig.pose(tl, t, base, b * (style === 'robot' ? .1 : .85), style === 'robot' ? 'steps(1)' : 'sine.inOut');
    }
    rig.pose(tl, t, 'idle', .3); return t + .3;
  };

  /* ATTACH props to slots (connected forever) */
  rig.attach = (node, slot, a = {}) => { const host = rig.slots[slot]; const w = el('g', { transform: `translate(${a.x || 0} ${a.y || 0}) rotate(${a.rot || 0}) scale(${a.s || 1})` }, host); w.appendChild(node); return w; };
  rig.worldPoint = (jointName, x = 0, y = 0) => J[jointName].world(x, y);       // stage coords of any joint-local point
  rig.tip = (limb) => J['wr' + limb].world(0, 8);                                // hand centre on stage

  rig.el = root.g;
  rig.setPose = (name, over) => { const P = rig.resolve(name, over);               // instant pose (no timeline)
    for (const k in TARGET) { const [j, p] = TARGET[k]; if (P[k] != null && j) { j[p] = P[k]; j.apply(); } } };
  rig.setPose('idle'); return rig;
};

g.GK = GK;
})(typeof window !== 'undefined' ? window : globalThis);
