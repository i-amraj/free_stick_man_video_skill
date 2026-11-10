/* GrowKaz PROPS v2 — every asset is pure SVG code.
 * Convention: origin (0,0) = BOTTOM-CENTRE on the ground. Object grows toward -y.
 * Signature: GK.P.name(parentGroup, {x,y,s,c,...}) -> <g>.   Units px (GK.cm(cm) converts).
 * Light comes from TOP-LEFT: lit = lighter, right/under sides = darker, contact shadow always. */
(function (g) {
'use strict';
const GK = g.GK = g.GK || {}, P = GK.P = {}, el = GK.el, shade = GK.shade, cm = GK.cm;
const OL = '#121824', S = (w = 3) => ({ stroke: OL, 'stroke-width': w, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' });
let uid = 0;

GK.grad = (parent, kind, stops, attrs = {}) => {          // returns url(#id); creates <defs> if needed
  const svg = parent.ownerSVGElement || parent; let defs = svg.querySelector('defs');
  if (!defs) { defs = el('defs', {}); svg.insertBefore(defs, svg.firstChild); }
  const id = 'gk' + (uid++), n = el(kind === 'r' ? 'radialGradient' : 'linearGradient', Object.assign({ id }, attrs), defs);
  stops.forEach(([o, c, a]) => el('stop', { offset: o, 'stop-color': c, 'stop-opacity': a == null ? 1 : a }, n)); return `url(#${id})`;
};
P.root = (p, o = {}) => { const n = el('g', { transform: `translate(${o.x || 0} ${o.y || 0}) scale(${o.s || 1})` }, p); if (o.id) n.id = o.id; return n; };
P.shadow = (p, rx, y = 0, ry, op = .3) => el('ellipse', { cx: 0, cy: y, rx, ry: ry || rx * .16, fill: `rgba(0,0,0,${op})` }, p);

/* ── PRIMITIVES (build everything from these) ── */
P.box = (p, { x = 0, y = 0, w = 100, h = 100, d = 40, c = '#888', ow = 3 }) => {   // oblique block: front + top + right
  const n = el('g', { transform: `translate(${x} ${y})` }, p), dx = d * .5, dy = -d * .32;
  el('polygon', Object.assign({ points: `${w / 2},${-h} ${w / 2 + dx},${-h + dy} ${w / 2 + dx},${dy} ${w / 2},0`, fill: shade(c, -.28) }, S(ow)), n);
  el('polygon', Object.assign({ points: `${-w / 2},${-h} ${w / 2},${-h} ${w / 2 + dx},${-h + dy} ${-w / 2 + dx},${-h + dy}`, fill: shade(c, .22) }, S(ow)), n);
  el('rect', Object.assign({ x: -w / 2, y: -h, width: w, height: h, fill: c }, S(ow)), n); return n; };
P.rect = (p, x, y, w, h, c, o = {}) => el('rect', Object.assign({ x, y, width: w, height: h, rx: o.rx || 0, fill: c }, S(o.ow == null ? 3 : o.ow)), p);
P.cyl = (p, { x = 0, y = 0, rx = 30, ry, h = 60, c = '#888', ow = 3, cap = true }) => {
  ry = ry || rx * .32; const n = el('g', { transform: `translate(${x} ${y})` }, p);
  const f = GK.grad(p, 'l', [[0, shade(c, .3)], [.5, c], [1, shade(c, -.32)]], { x1: 0, y1: 0, x2: 1, y2: 0 });
  el('path', Object.assign({ d: `M ${-rx} ${-h} L ${-rx} 0 A ${rx} ${ry} 0 0 0 ${rx} 0 L ${rx} ${-h} Z`, fill: f }, S(ow)), n);
  if (cap) el('ellipse', Object.assign({ cx: 0, cy: -h, rx, ry, fill: shade(c, .32) }, S(ow)), n); return n; };
P.ball = (p, { x = 0, y = 0, r = 30, c = '#e03', ow = 3 }) => {
  const n = el('g', { transform: `translate(${x} ${y})` }, p); P.shadow(n, r * .8, 0, r * .16);
  el('circle', Object.assign({ cx: 0, cy: -r, r, fill: GK.grad(p, 'r', [[0, shade(c, .5)], [.55, c], [1, shade(c, -.38)]], { cx: .35, cy: .3, r: .8 }) }, S(ow)), n); return n; };
P.text = (p, str, x, y, size = 18, c = '#111', w = 900) => { const t = el('text', { x, y, 'text-anchor': 'middle', 'font-family': 'Montserrat,Arial,sans-serif', 'font-weight': w, 'font-size': size, fill: c }, p); t.textContent = str; return t; };
const J = (p, x, y) => new GK.Joint(p, x, y);

/* ── FURNITURE & HOME ── */
P.table = (p, o = {}) => { const n = P.root(p, o), w = o.w || cm(120), h = o.h || cm(75), d = o.d || cm(60), c = o.c || '#9a6b35', t = 12, dx = d * .5, dy = -d * .32;
  P.shadow(n, w * .62 + dx * .5, -6, 16);
  [[-1, dx, dy], [1, dx, dy], [-1, 0, 0], [1, 0, 0]].forEach(([sg, ox, oy]) => P.box(n, { x: sg * (w / 2 - 14) + ox, y: oy, w: 14, h: h - t, d: 14, c: shade(c, -.15), ow: 2.5 }));
  P.box(n, { x: 0, y: -(h - t), w, h: t, d, c }); return n; };
P.chair = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#7a4b24', sh = 102, v = o.view || 'side', part = o.part || 'all';
  if (v === 'side') { P.shadow(n, 58, 0, 9);
    P.rect(n, -46, -sh - 118, 12, 118 + 12, c); P.rect(n, -46, -sh + 8, 10, sh - 8, shade(c, -.2)); P.rect(n, 34, -sh + 8, 10, sh - 8, shade(c, -.2));
    P.rect(n, -46, -sh - 4, 92, 14, shade(c, .12), { rx: 4 }); P.rect(n, -44, -sh - 96, 8, 10, shade(c, -.3), { ow: 0 }); return n; }
  P.shadow(n, 70, 0, 11);
  if (part !== 'front') { P.rect(n, -48, -sh - 118, 96, 112, c, { rx: 6 }); P.rect(n, -40, -sh - 98, 80, 12, shade(c, -.25), { rx: 4 });
    P.rect(n, -46, -sh + 4, 10, sh - 4, shade(c, -.3)); P.rect(n, 36, -sh + 4, 10, sh - 4, shade(c, -.3)); }
  if (part !== 'back') { el('polygon', Object.assign({ points: `-52,${-sh - 6} 52,${-sh - 6} 66,${-sh + 12} -66,${-sh + 12}`, fill: shade(c, .25) }, S()), n);
    P.rect(n, -66, -sh + 12, 132, 9, c); P.rect(n, -62, -sh + 21, 12, sh - 21, shade(c, -.1)); P.rect(n, 50, -sh + 21, 12, sh - 21, shade(c, -.1)); } return n; };
P.bed = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#5b7bd5'; P.shadow(n, 230, 0, 14);   // side view
  P.rect(n, -210, -50, 16, 50, '#6b4423'); P.rect(n, 194, -50, 16, 50, '#6b4423'); P.rect(n, -214, -140, 18, 140, '#7a4b24', { rx: 6 });
  P.rect(n, -200, -86, 404, 40, '#8a5a2e', { rx: 4 }); P.rect(n, -196, -120, 396, 36, '#f1f5f9', { rx: 14 });
  el('path', Object.assign({ d: 'M -60 -122 Q 0 -150 60 -122 L 196 -122 L 196 -84 L -60 -84 Z', fill: c }, S()), n);
  el('path', { d: 'M -60 -108 H 196', stroke: shade(c, -.25), 'stroke-width': 3, opacity: .5 }, n);
  el('ellipse', Object.assign({ cx: -150, cy: -132, rx: 46, ry: 18, fill: '#fff' }, S()), n); return n; };
P.sofa = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#b8453d', w = o.w || 300; P.shadow(n, w / 2 + 20, 0, 12);
  P.rect(n, -w / 2, -150, w, 120, shade(c, -.12), { rx: 22 }); P.rect(n, -w / 2 - 22, -100, 44, 80, c, { rx: 16 }); P.rect(n, w / 2 - 22, -100, 44, 80, c, { rx: 16 });
  P.rect(n, -w / 2 + 12, -80, w / 2 - 12, 56, shade(c, .12), { rx: 12 }); P.rect(n, 0, -80, w / 2 - 12, 56, shade(c, .12), { rx: 12 });
  P.rect(n, -w / 2 + 6, -26, 14, 26, '#3a2512'); P.rect(n, w / 2 - 20, -26, 14, 26, '#3a2512'); return n; };
P.lamp = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#fbbf24'; P.shadow(n, 38, 0, 7);
  P.cyl(n, { rx: 30, h: 8, c: '#444', ry: 8 }); P.rect(n, -3, -180, 6, 172, '#555', { ow: 2 });
  const gl = el('ellipse', { cx: 0, cy: -190, rx: 120, ry: 100, fill: GK.grad(p, 'r', [[0, '#fff7b0', .75], [1, '#fbbf24', 0]]) }, n); n.glow = gl;
  el('path', Object.assign({ d: 'M -52 -176 L 52 -176 L 34 -226 L -34 -226 Z', fill: c }, S()), n); return n; };
P.door = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#8b5a2b', w = 110, h = cm(200); P.shadow(n, w * .6, 2, 7);
  P.rect(n, -w / 2 - 8, -h - 8, w + 16, h + 8, '#5a3a1a'); P.rect(n, -w / 2, -h, w, h, '#1b1410', { ow: 0 });
  const pan = n.panel = J(n, -w / 2, 0);                                      // hinge at left edge; open: tween sx -> .2, skew via rot
  P.rect(pan.g, 0, -h, w, h, c); P.rect(pan.g, 14, -h + 16, w - 28, h * .4, shade(c, -.12), { rx: 4, ow: 2 }); P.rect(pan.g, 14, -h * .5 + 8, w - 28, h * .42, shade(c, -.12), { rx: 4, ow: 2 });
  el('circle', Object.assign({ cx: w - 16, cy: -h * .48, r: 7, fill: '#fbbf24' }, S(2.5)), pan.g); return n; };
P.window = (p, o = {}) => { const n = P.root(p, o), w = o.w || 190, h = o.h || 230;
  const sky = GK.grad(p, 'l', [[0, '#7dd3fc'], [1, '#e0f2fe']], { x1: 0, y1: 0, x2: 0, y2: 1 });
  P.rect(n, -w / 2 - 10, -h - 10, w + 20, h + 20, '#e5e7eb'); P.rect(n, -w / 2, -h, w, h, sky);
  el('path', { d: `M ${-w / 2} ${-h * .35} Q ${-w / 4} ${-h * .5} 0 ${-h * .35} T ${w / 2} ${-h * .35} V 0 H ${-w / 2} Z`, fill: '#86efac', opacity: .8 }, n);
  P.rect(n, -3, -h, 6, h, '#e5e7eb', { ow: 2 }); P.rect(n, -w / 2, -h / 2 - 3, w, 6, '#e5e7eb', { ow: 2 }); P.rect(n, -w / 2 - 18, 0, w + 36, 12, '#d1d5db', { rx: 3 }); return n; };
P.shelf = (p, o = {}) => { const n = P.root(p, o), w = o.w || 220, h = o.h || 300, r = GK.rng(o.seed || 3), cols = ['#ef4444', '#3b82f6', '#22c55e', '#f59e0b', '#8b5cf6', '#14b8a6']; P.shadow(n, w * .6, 0, 10);
  P.rect(n, -w / 2, -h, w, h, '#7a4b24'); P.rect(n, -w / 2 + 8, -h + 8, w - 16, h - 16, '#3a2512', { ow: 0 });
  for (let r_ = 0; r_ < 3; r_++) { const y = -h + 8 + (r_ + 1) * (h - 16) / 3; let x = -w / 2 + 14;
    while (x < w / 2 - 30) { const bw = 12 + r() * 12, bh = 48 + r() * 30; P.rect(n, x, y - bh, bw, bh, cols[Math.floor(r() * 6)], { ow: 2 }); x += bw + 2; }
    P.rect(n, -w / 2 + 8, y, w - 16, 8, '#8a5a2e', { ow: 2 }); } return n; };
P.tv = (p, o = {}) => { const n = P.root(p, o), w = o.w || 260, h = w * .58; P.shadow(n, w * .4, 0, 8);
  P.rect(n, -34, -22, 68, 22, '#222'); P.rect(n, -w / 2, -h - 22, w, h, '#111', { rx: 8 });
  const scr = el('rect', { x: -w / 2 + 8, y: -h - 14, width: w - 16, height: h - 16, rx: 4, fill: GK.grad(p, 'l', [[0, '#38bdf8'], [1, '#6366f1']], { x1: 0, y1: 0, x2: 1, y2: 1 }) }, n); n.screen = scr;
  el('polygon', { points: `${-w / 2 + 8},${-h - 14} ${-w / 6},${-h - 14} ${-w / 2 + 8},${-h / 2 - 20}`, fill: '#fff', opacity: .12 }, n); return n; };
P.laptop = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#9ca3af'; P.shadow(n, 90, 0, 8);
  el('polygon', Object.assign({ points: '-70,-100 70,-100 62,-4 -62,-4', fill: '#1f2937' }, S()), n); el('polygon', { points: '-60,-92 60,-92 54,-12 -54,-12', fill: '#38bdf8', opacity: .85 }, n);
  el('polygon', Object.assign({ points: '-86,0 86,0 78,-10 -78,-10', fill: c }, S()), n); return n; };
P.phone = (p, o = {}) => { const n = P.root(p, o); P.rect(n, -22, -80, 44, 80, '#111', { rx: 8 }); P.rect(n, -18, -74, 36, 62, o.screen || '#60a5fa', { rx: 3, ow: 0 }); el('circle', { cx: 0, cy: -6, r: 3, fill: '#444' }, n); return n; };
P.mug = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#f8fafc'; P.shadow(n, 34, 0, 6); P.cyl(n, { rx: 22, h: 40, c });
  el('path', Object.assign({ d: 'M 22 -30 Q 42 -30 42 -18 Q 42 -6 22 -8', fill: 'none' }, S(5)), n); el('ellipse', { cx: 0, cy: -38, rx: 17, ry: 5, fill: '#6b3f1d' }, n);
  n.steam = el('path', { d: 'M -6 -48 Q -12 -60 -6 -70 Q 0 -80 -6 -90', stroke: '#fff', 'stroke-width': 3, fill: 'none', opacity: .6 }, n); return n; };
P.bottle = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#16a34a'; P.shadow(n, 26, 0, 5); P.cyl(n, { rx: 20, h: 70, c, cap: false });
  P.cyl(n, { rx: 8, h: 40, y: -66, c, cap: false }); P.rect(n, -9, -112, 18, 8, '#facc15', { rx: 2, ow: 2 }); P.rect(n, -20, -50, 40, 24, '#f8fafc', { ow: 1.5 }); return n; };
P.book = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#dc2626'; P.shadow(n, 50, 0, 6);
  P.box(n, { w: 90, h: 16, d: 60, c }); P.rect(n, -45, -16, 6, 16, shade(c, -.3), { ow: 0 }); return n; };
P.clock = (p, o = {}) => { const n = P.root(p, o), r = o.r || 50; el('circle', Object.assign({ cx: 0, cy: 0, r, fill: '#fff' }, S(6)), n);
  for (let i = 0; i < 12; i++) { const a = i * Math.PI / 6; el('line', Object.assign({ x1: Math.sin(a) * (r - 10), y1: -Math.cos(a) * (r - 10), x2: Math.sin(a) * (r - 4), y2: -Math.cos(a) * (r - 4) }, S(i % 3 ? 2 : 4)), n); }
  const mk = (len, w) => { const j = J(n, 0, 0); el('line', Object.assign({ x1: 0, y1: 6, x2: 0, y2: -len }, S(w)), j.g); return j; };
  n.hour = mk(r * .5, 5); n.min = mk(r * .75, 3.5); el('circle', { cx: 0, cy: 0, r: 4, fill: OL }, n); return n; };   // spin: tween n.min.rot (apply!)
P.sign = (p, o = {}) => { const n = P.root(p, o), w = o.w || 220; P.shadow(n, 30, 0, 6); P.rect(n, -6, -200, 12, 200, '#6b4423');
  P.rect(n, -w / 2, -260, w, 110, o.c || '#f5e6c8', { rx: 8, ow: 5 }); P.text(n, o.t1 || 'WANTED', 0, -212, 30, '#1e1e1e'); P.text(n, o.t2 || '', 0, -180, 18, '#7c1a1a'); return n; };

/* ── NATURE / WORLD ── */
P.tree = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#22a553'; P.shadow(n, 90, 0, 14);
  P.cyl(n, { rx: 18, h: 150, c: '#6b4423', cap: false });
  [[0, -230, 80], [-52, -180, 58], [54, -184, 60], [0, -280, 56]].forEach(([x, y, r], i) => el('circle', Object.assign({ cx: x, cy: y, r, fill: shade(c, i * .06 - .05) }, S(4)), n));
  el('ellipse', { cx: -22, cy: -262, rx: 26, ry: 14, fill: '#fff', opacity: .16 }, n); n.crown = n; return n; };
P.house = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#f4d9a8', w = 330, h = 220; P.shadow(n, w * .65, 0, 14);
  P.box(n, { w, h, d: 80, c, ow: 4 }); el('polygon', Object.assign({ points: `${-w / 2 - 24},${-h} ${w / 2 + 50},${-h + 8 - 26} ${w / 2 + 10},${-h - 100} ${-w / 2 + 14},${-h - 100}`, fill: '#b3472f' }, S(4)), n);
  P.rect(n, -34, -130, 68, 130, '#6b4423'); el('circle', { cx: 20, cy: -62, r: 5, fill: '#fbbf24' }, n);
  [-110, 110].forEach(x => { P.rect(n, x - 32, -170, 64, 64, '#bae6fd'); P.rect(n, x - 2, -170, 4, 64, '#fff', { ow: 1 }); }); return n; };
P.cloud = (p, o = {}) => { const n = P.root(p, o); [[0, 0, 40], [-44, 10, 30], [46, 10, 32], [14, -22, 30]].forEach(([x, y, r]) => el('circle', { cx: x, cy: y, r, fill: '#fff', opacity: .95 }, n)); return n; };
P.flower = (p, o = {}) => { const n = P.root(p, o); P.rect(n, -2, -60, 4, 60, '#16a34a', { ow: 1.5 }); for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3; el('circle', Object.assign({ cx: Math.sin(a) * 12, cy: -64 - Math.cos(a) * 12, r: 10, fill: o.c || '#f472b6' }, S(1.8)), n); }
  el('circle', Object.assign({ cx: 0, cy: -64, r: 8, fill: '#fbbf24' }, S(1.8)), n); return n; };
P.car = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#e11d48'; P.shadow(n, 190, 0, 14);   // side view facing +x
  el('path', Object.assign({ d: 'M -170 -40 L -170 -90 Q -160 -100 -110 -102 L -60 -150 Q -50 -160 -20 -160 L 70 -160 Q 90 -160 104 -140 L 130 -102 Q 170 -98 172 -70 L 172 -40 Z', fill: c }, S(4)), n);
  el('path', { d: 'M -52 -104 L -22 -146 L 66 -146 L 100 -104 Z', fill: '#bae6fd', stroke: OL, 'stroke-width': 3 }, n);
  n.wheels = [-100, 100].map(x => { const w = J(n, x, -30); el('circle', Object.assign({ cx: 0, cy: 0, r: 34, fill: '#222' }, S(4)), w.g); el('circle', { cx: 0, cy: 0, r: 16, fill: '#d1d5db', stroke: OL, 'stroke-width': 3 }, w.g);
    for (let i = 0; i < 5; i++) { const a = i * 72 * Math.PI / 180; el('line', { x1: 0, y1: 0, x2: Math.sin(a) * 15, y2: -Math.cos(a) * 15, stroke: OL, 'stroke-width': 2.5 }, w.g); } return w; }); return n; };  // spin: tween wheels[i].rot

/* ── ITEMS / TREASURE / WEAPONS ── */
P.chest = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#8b5a2b'; P.shadow(n, 110, 0, 10);
  P.box(n, { w: 150, h: 66, d: 60, c }); el('path', Object.assign({ d: 'M -75 -66 Q -75 -122 0 -122 Q 75 -122 75 -66 Z', fill: shade(c, .08) }, S()), n);
  P.rect(n, -75, -80, 150, 10, '#facc15', { ow: 2.5 }); P.rect(n, -10, -88, 20, 28, '#facc15', { rx: 3, ow: 2.5 }); el('circle', { cx: 0, cy: -72, r: 4, fill: OL }, n); return n; };
P.coins = (p, o = {}) => { const n = P.root(p, o), k = o.n || 5; P.shadow(n, 28, 4, 6);
  for (let i = 0; i < k; i++) { const y = -i * 9; el('ellipse', Object.assign({ cx: 0, cy: y, rx: 22, ry: 8, fill: shade('#f59e0b', i * .07) }, S(2.5)), n); }
  el('ellipse', { cx: -5, cy: -(k - 1) * 9 - 3, rx: 8, ry: 2.5, fill: '#fff', opacity: .4 }, n); return n; };
P.key = (p, o = {}) => { const n = P.root(p, o); el('circle', Object.assign({ cx: 0, cy: -50, r: 16, fill: 'none', stroke: '#facc15', 'stroke-width': 8 }, {}), n); el('circle', Object.assign({ cx: 0, cy: -50, r: 20, fill: 'none' }, S(2)), n);
  P.rect(n, -4, -34, 8, 40, '#facc15', { ow: 2 }); P.rect(n, 4, -4, 10, 6, '#facc15', { ow: 2 }); P.rect(n, 4, -14, 14, 6, '#facc15', { ow: 2 }); return n; };
P.sword = (p, o = {}) => { const n = P.root(p, o); el('polygon', Object.assign({ points: '-8,-30 8,-30 6,-190 0,-206 -6,-190', fill: '#cbd5e1' }, S()), n); el('line', { x1: 0, y1: -40, x2: 0, y2: -190, stroke: '#fff', 'stroke-width': 2, opacity: .7 }, n);
  P.rect(n, -26, -36, 52, 9, '#facc15', { rx: 4 }); P.rect(n, -5, -28, 10, 40, '#6b4423', { ow: 2 }); el('circle', Object.assign({ cx: 0, cy: 16, r: 8, fill: '#facc15' }, S(2.5)), n); return n; };
P.shield = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#2563eb'; el('path', Object.assign({ d: 'M -50 -110 L 50 -110 L 50 -50 Q 50 -10 0 10 Q -50 -10 -50 -50 Z', fill: c }, S(5)), n);
  el('path', { d: 'M 0 -104 V 2 M -44 -70 H 44', stroke: '#facc15', 'stroke-width': 9 }, n); return n; };
P.umbrella = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#ef4444'; P.rect(n, -2, -150, 4, 150, '#555', { ow: 1.5 });
  el('path', Object.assign({ d: 'M -90 -150 Q -80 -230 0 -236 Q 80 -230 90 -150 Q 60 -165 45 -150 Q 22 -165 0 -150 Q -22 -165 -45 -150 Q -60 -165 -90 -150 Z', fill: c }, S(3.5)), n); return n; };
P.bag = (p, o = {}) => { const n = P.root(p, o), c = o.c || '#7c3aed'; P.shadow(n, 50, 0, 8); el('path', Object.assign({ d: 'M -40 0 L -46 -80 Q -46 -100 -26 -100 L 26 -100 Q 46 -100 46 -80 L 40 0 Z', fill: c }, S()), n);
  el('path', Object.assign({ d: 'M -20 -100 Q 0 -140 20 -100', fill: 'none' }, S(6)), n); return n; };

/* ── COSTUMES (all attach to rig slots => never detach) ── */
GK.costume = {
  glasses(rig, c = '#121824') { const f = rig.slots.face, s = rig.o.view === 'side' ? [[17]] : [[-15], [15]];
    s.forEach(([x]) => el('circle', Object.assign({ cx: x, cy: -4, r: 12, fill: 'rgba(186,230,253,.35)' }, S(3)), f));
    if (rig.o.view !== 'side') el('line', Object.assign({ x1: -3, y1: -5, x2: 3, y2: -5 }, S(3)), f); },
  tie(rig, c = '#dc2626') { el('path', Object.assign({ d: 'M -6 -104 L 6 -104 L 10 -66 L 0 -54 L -10 -66 Z', fill: c }, S(2.5)), rig.slots.torso); },
  belt(rig, c = '#78350f') { P.rect(rig.slots.torso, -23, -14, 46, 11, c, { rx: 3, ow: 2.4 }); P.rect(rig.slots.torso, -7, -13, 14, 9, '#facc15', { rx: 2, ow: 2 }); },
  cap(rig, c = '#ef4444') { const h = rig.slots.head; el('path', Object.assign({ d: 'M -44 -10 Q -46 -56 0 -58 Q 46 -56 44 -10 Z', fill: c }, S(3.5)), h); el('path', Object.assign({ d: 'M 4 -14 L 64 -10 Q 66 -2 56 -2 L 6 -4 Z', fill: shade(c, -.2) }, S(3)), h); },
  crown(rig, c = '#facc15') { el('path', Object.assign({ d: 'M -34 -40 L -38 -80 L -18 -60 L 0 -88 L 18 -60 L 38 -80 L 34 -40 Z', fill: c }, S(3)), rig.slots.head); },
  helmet(rig, c = '#2563eb', plume = '#dc2626') { const h = rig.slots.head;
    el('path', { d: 'M 0 -64 Q 26 -84 14 -108 Q 0 -92 -14 -108 Q -26 -84 0 -64', fill: plume, stroke: OL, 'stroke-width': 3 }, h);
    el('path', Object.assign({ d: 'M -46 -6 Q -48 -62 0 -64 Q 48 -62 46 -6 L 40 -14 Q 0 -30 -40 -14 Z', fill: c }, S(4)), h); P.rect(h, -46, -24, 92, 10, '#facc15', { rx: 4 }); },
  cape(rig, c = '#7f1d1d') { const sw = rig.slots.back, j = new GK.Joint(rig.J.spine, 0, -100); sw.appendChild(j.g);        // back slot is under torso: sways with Joint
    el('path', Object.assign({ d: 'M -22 0 L 22 0 Q 46 70 56 120 Q 0 134 -56 120 Q -46 70 -22 0 Z', fill: c }, S(3.5)), j.g); return j; },   // tween j.rot for flutter
  backpack(rig, c = '#16a34a') { P.rect(rig.slots.back, -30, -100, 36, 70, c, { rx: 10 }); P.rect(rig.slots.back, -24, -80, 24, 22, shade(c, -.2), { rx: 5, ow: 2 }); }
};
g.GK = GK;
})(typeof window !== 'undefined' ? window : globalThis);
