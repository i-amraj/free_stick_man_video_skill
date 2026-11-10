/**
 * ============================================================
 * GrowKaz Stickman Studio — FULL SKELETON RIG v2.0
 * ============================================================
 *
 * Bone Hierarchy (53 Total Bones):
 *
 * ROOT
 *   └─ pelvis                   (hips center anchor)
 *       ├─ spine_lower           (lumbar, L3–L5)
 *       │   └─ spine_mid         (thoracic, T8)
 *       │       └─ spine_upper   (thoracic, T2)
 *       │           └─ neck      (cervical)
 *       │               └─ head  (skull)
 *       │                   ├─ eye_l      (left eye)
 *       │                   ├─ eye_r      (right eye)
 *       │                   ├─ eyebrow_l  (expression)
 *       │                   ├─ eyebrow_r  (expression)
 *       │                   ├─ mouth      (lips)
 *       │                   └─ sweat      (fear bead)
 *       │
 *       ├─ shoulder_l            (left clavicle/scapula)
 *       │   └─ upperarm_l        (left humerus)
 *       │       └─ forearm_l     (left ulna/radius)
 *       │           └─ hand_l    (left carpals)
 *       │               ├─ thumb_l
 *       │               ├─ index_l
 *       │               └─ pinky_l
 *       │
 *       ├─ shoulder_r            (right clavicle/scapula)
 *       │   └─ upperarm_r        (right humerus)
 *       │       └─ forearm_r     (right ulna/radius)
 *       │           └─ hand_r    (right carpals)
 *       │               ├─ thumb_r
 *       │               ├─ index_r
 *       │               └─ pinky_r
 *       │
 *       ├─ hip_l                 (left iliac)
 *       │   └─ thigh_l           (left femur)
 *       │       └─ shin_l        (left tibia/fibula)
 *       │           └─ foot_l    (left talus/ankle)
 *       │               └─ toe_l (left phalanges)
 *       │
 *       └─ hip_r                 (right iliac)
 *           └─ thigh_r           (right femur)
 *               └─ shin_r        (right tibia/fibula)
 *                   └─ foot_r    (right talus/ankle)
 *                       └─ toe_r (right phalanges)
 *
 * Usage:
 *   const rig = new GKStickmanSkeleton('my-svg-id', {
 *     x: 540, y: 1100, scale: 1.0, color: '#f8fafc', strokeWidth: 7
 *   });
 *   rig.pose('idle');                    // Instant snap to named pose
 *   rig.animate('idle', 0.5);           // GSAP smooth transition to named pose
 *   rig.getBone('hand_r');              // Get the SVG element for a bone
 *   rig.setBone('forearm_l', { d: 'M...' }); // Manually set bone attributes
 * ============================================================
 */

export class GKStickmanSkeleton {

  /**
   * @param {string} svgId   - ID of the parent <svg> or <g> element to inject into
   * @param {object} options - Configuration options
   */
  constructor(svgId, options = {}) {
    this.svg = document.getElementById(svgId);
    this.cfg = {
      id:          options.id          || 'gk-stickman',
      x:           options.x           || 540,
      y:           options.y           || 1100,
      scale:       options.scale       || 1.0,
      color:       options.color       || '#f8fafc',
      sw:          options.strokeWidth || 7,          // base stroke width
      fill:        options.fill        || '#090e1a',  // head/body fill
      eyeColor:    options.eyeColor    || '#38bdf8',
    };
    this.bones = {};   // { boneName: SVGElement }
    this.root = null;  // The root <g> element
    this._build();
  }

  // ─────────────────────────────────────────────
  //  PRIVATE: Build the full SVG skeleton
  // ─────────────────────────────────────────────
  _build() {
    const { id, x, y, scale, color, sw, fill, eyeColor } = this.cfg;
    const ns = 'http://www.w3.org/2000/svg';

    const root = document.createElementNS(ns, 'g');
    root.setAttribute('id', id);
    root.setAttribute('data-gk-rig', 'v2');
    root.setAttribute('transform', `translate(${x},${y}) scale(${scale})`);
    this.root = root;

    // ── Helper: create any SVG element with attrs ──────────────────
    const el = (tag, attrs, boneName) => {
      const e = document.createElementNS(ns, tag);
      for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
      if (boneName) {
        e.setAttribute('data-bone', boneName);
        this.bones[boneName] = e;
      }
      return e;
    };

    // ── BONE 01: pelvis (root anchor) ─────────────────────────────
    const pelvis = el('g', { id: `${id}-pelvis`, 'data-bone': 'pelvis' }, 'pelvis');
    root.appendChild(pelvis);

    // ── BONE 02–04: Spine chain ───────────────────────────────────
    // spine_lower: pelvis → lumbar
    const spineLower = el('line', {
      id: `${id}-spine-lower`, 'data-bone': 'spine_lower',
      x1: 0, y1: 60,
      x2: 0, y2: 10,
      stroke: color, 'stroke-width': sw + 1, 'stroke-linecap': 'round'
    }, 'spine_lower');

    // spine_mid: lumbar → thoracic
    const spineMid = el('line', {
      id: `${id}-spine-mid`, 'data-bone': 'spine_mid',
      x1: 0, y1: 10,
      x2: 0, y2: -50,
      stroke: color, 'stroke-width': sw, 'stroke-linecap': 'round'
    }, 'spine_mid');

    // spine_upper: thoracic → neck base
    const spineUpper = el('line', {
      id: `${id}-spine-upper`, 'data-bone': 'spine_upper',
      x1: 0, y1: -50,
      x2: 0, y2: -115,
      stroke: color, 'stroke-width': sw, 'stroke-linecap': 'round'
    }, 'spine_upper');

    pelvis.appendChild(spineLower);
    pelvis.appendChild(spineMid);
    pelvis.appendChild(spineUpper);

    // ── BONE 05: Neck ─────────────────────────────────────────────
    const neck = el('line', {
      id: `${id}-neck`, 'data-bone': 'neck',
      x1: 0, y1: -115,
      x2: 0, y2: -128,
      stroke: color, 'stroke-width': sw - 1, 'stroke-linecap': 'round'
    }, 'neck');
    pelvis.appendChild(neck);

    // ── BONE 06: Head ─────────────────────────────────────────────
    const headGroup = el('g', { id: `${id}-head-group`, 'data-bone': 'head' }, 'head');

    const headCircle = el('circle', {
      id: `${id}-head-circle`,
      cx: 0, cy: -165, r: 40,
      fill: fill, stroke: color, 'stroke-width': sw
    });
    headGroup.appendChild(headCircle);

    // ── BONE 07: eye_l  ───────────────────────────────────────────
    const eyeL = el('circle', {
      id: `${id}-eye-l`, 'data-bone': 'eye_l',
      cx: -13, cy: -168, r: 5,
      fill: eyeColor
    }, 'eye_l');
    headGroup.appendChild(eyeL);

    // ── BONE 08: eye_r  ───────────────────────────────────────────
    const eyeR = el('circle', {
      id: `${id}-eye-r`, 'data-bone': 'eye_r',
      cx: 13, cy: -168, r: 5,
      fill: eyeColor
    }, 'eye_r');
    headGroup.appendChild(eyeR);

    // ── BONE 09: eyebrow_l ────────────────────────────────────────
    const eyebrowL = el('path', {
      id: `${id}-eyebrow-l`, 'data-bone': 'eyebrow_l',
      d: 'M -20 -178 L -6 -180',
      stroke: color, 'stroke-width': 3, fill: 'none', 'stroke-linecap': 'round'
    }, 'eyebrow_l');
    headGroup.appendChild(eyebrowL);

    // ── BONE 10: eyebrow_r ────────────────────────────────────────
    const eyebrowR = el('path', {
      id: `${id}-eyebrow-r`, 'data-bone': 'eyebrow_r',
      d: 'M 6 -180 L 20 -178',
      stroke: color, 'stroke-width': 3, fill: 'none', 'stroke-linecap': 'round'
    }, 'eyebrow_r');
    headGroup.appendChild(eyebrowR);

    // ── BONE 11: mouth ────────────────────────────────────────────
    const mouth = el('path', {
      id: `${id}-mouth`, 'data-bone': 'mouth',
      d: 'M -10 -150 Q 0 -144 10 -150',
      stroke: color, 'stroke-width': 4, fill: 'none', 'stroke-linecap': 'round'
    }, 'mouth');
    headGroup.appendChild(mouth);

    // ── BONE 12: sweat (fear bead) ────────────────────────────────
    const sweat = el('circle', {
      id: `${id}-sweat`, 'data-bone': 'sweat',
      cx: 35, cy: -180, r: 4.5,
      fill: eyeColor, opacity: 0
    }, 'sweat');
    headGroup.appendChild(sweat);

    pelvis.appendChild(headGroup);

    // ── BONES 13–14: Shoulder girdle ──────────────────────────────
    // shoulder_l  (left collarbone segment)
    const shoulderL = el('line', {
      id: `${id}-shoulder-l`, 'data-bone': 'shoulder_l',
      x1: 0, y1: -100,
      x2: -28, y2: -105,
      stroke: color, 'stroke-width': sw - 1, 'stroke-linecap': 'round'
    }, 'shoulder_l');
    pelvis.appendChild(shoulderL);

    // shoulder_r  (right collarbone segment)
    const shoulderR = el('line', {
      id: `${id}-shoulder-r`, 'data-bone': 'shoulder_r',
      x1: 0, y1: -100,
      x2: 28, y2: -105,
      stroke: color, 'stroke-width': sw - 1, 'stroke-linecap': 'round'
    }, 'shoulder_r');
    pelvis.appendChild(shoulderR);

    // ── BONE 15: upperarm_l ───────────────────────────────────────
    const upperarmL = el('line', {
      id: `${id}-upperarm-l`, 'data-bone': 'upperarm_l',
      x1: -28, y1: -105,
      x2: -60, y2: -60,
      stroke: color, 'stroke-width': sw, 'stroke-linecap': 'round'
    }, 'upperarm_l');
    pelvis.appendChild(upperarmL);

    // ── BONE 16: forearm_l ────────────────────────────────────────
    const forearmL = el('line', {
      id: `${id}-forearm-l`, 'data-bone': 'forearm_l',
      x1: -60, y1: -60,
      x2: -85, y2: -15,
      stroke: color, 'stroke-width': sw - 1, 'stroke-linecap': 'round'
    }, 'forearm_l');
    pelvis.appendChild(forearmL);

    // ── BONE 17: hand_l ───────────────────────────────────────────
    const handL = el('g', { id: `${id}-hand-l`, 'data-bone': 'hand_l' }, 'hand_l');
    // Palm circle
    handL.appendChild(el('circle', {
      cx: -85, cy: -15, r: 7,
      fill: fill, stroke: color, 'stroke-width': sw - 2
    }));
    pelvis.appendChild(handL);

    // ── BONE 18: thumb_l ──────────────────────────────────────────
    const thumbL = el('line', {
      id: `${id}-thumb-l`, 'data-bone': 'thumb_l',
      x1: -85, y1: -15,
      x2: -96, y2: -24,
      stroke: color, 'stroke-width': 3, 'stroke-linecap': 'round'
    }, 'thumb_l');
    pelvis.appendChild(thumbL);

    // ── BONE 19: index_l ──────────────────────────────────────────
    const indexL = el('line', {
      id: `${id}-index-l`, 'data-bone': 'index_l',
      x1: -85, y1: -15,
      x2: -92, y2: -5,
      stroke: color, 'stroke-width': 3, 'stroke-linecap': 'round'
    }, 'index_l');
    pelvis.appendChild(indexL);

    // ── BONE 20: pinky_l ──────────────────────────────────────────
    const pinkyL = el('line', {
      id: `${id}-pinky-l`, 'data-bone': 'pinky_l',
      x1: -85, y1: -15,
      x2: -92, y2: -26,
      stroke: color, 'stroke-width': 3, 'stroke-linecap': 'round'
    }, 'pinky_l');
    pelvis.appendChild(pinkyL);

    // ── BONE 21: upperarm_r ───────────────────────────────────────
    const upperarmR = el('line', {
      id: `${id}-upperarm-r`, 'data-bone': 'upperarm_r',
      x1: 28, y1: -105,
      x2: 60, y2: -60,
      stroke: color, 'stroke-width': sw, 'stroke-linecap': 'round'
    }, 'upperarm_r');
    pelvis.appendChild(upperarmR);

    // ── BONE 22: forearm_r ────────────────────────────────────────
    const forearmR = el('line', {
      id: `${id}-forearm-r`, 'data-bone': 'forearm_r',
      x1: 60, y1: -60,
      x2: 85, y2: -15,
      stroke: color, 'stroke-width': sw - 1, 'stroke-linecap': 'round'
    }, 'forearm_r');
    pelvis.appendChild(forearmR);

    // ── BONE 23: hand_r ───────────────────────────────────────────
    const handR = el('g', { id: `${id}-hand-r`, 'data-bone': 'hand_r' }, 'hand_r');
    handR.appendChild(el('circle', {
      cx: 85, cy: -15, r: 7,
      fill: fill, stroke: color, 'stroke-width': sw - 2
    }));
    pelvis.appendChild(handR);

    // ── BONE 24: thumb_r ──────────────────────────────────────────
    const thumbR = el('line', {
      id: `${id}-thumb-r`, 'data-bone': 'thumb_r',
      x1: 85, y1: -15,
      x2: 96, y2: -24,
      stroke: color, 'stroke-width': 3, 'stroke-linecap': 'round'
    }, 'thumb_r');
    pelvis.appendChild(thumbR);

    // ── BONE 25: index_r ──────────────────────────────────────────
    const indexR = el('line', {
      id: `${id}-index-r`, 'data-bone': 'index_r',
      x1: 85, y1: -15,
      x2: 92, y2: -5,
      stroke: color, 'stroke-width': 3, 'stroke-linecap': 'round'
    }, 'index_r');
    pelvis.appendChild(indexR);

    // ── BONE 26: pinky_r ──────────────────────────────────────────
    const pinkyR = el('line', {
      id: `${id}-pinky-r`, 'data-bone': 'pinky_r',
      x1: 85, y1: -15,
      x2: 92, y2: -26,
      stroke: color, 'stroke-width': 3, 'stroke-linecap': 'round'
    }, 'pinky_r');
    pelvis.appendChild(pinkyR);

    // ── BONE 27: hip_l ────────────────────────────────────────────
    const hipL = el('line', {
      id: `${id}-hip-l`, 'data-bone': 'hip_l',
      x1: 0, y1: 60,
      x2: -18, y2: 72,
      stroke: color, 'stroke-width': sw, 'stroke-linecap': 'round'
    }, 'hip_l');
    pelvis.appendChild(hipL);

    // ── BONE 28: thigh_l ──────────────────────────────────────────
    const thighL = el('line', {
      id: `${id}-thigh-l`, 'data-bone': 'thigh_l',
      x1: -18, y1: 72,
      x2: -40, y2: 160,
      stroke: color, 'stroke-width': sw + 1, 'stroke-linecap': 'round'
    }, 'thigh_l');
    pelvis.appendChild(thighL);

    // ── BONE 29: shin_l ───────────────────────────────────────────
    const shinL = el('line', {
      id: `${id}-shin-l`, 'data-bone': 'shin_l',
      x1: -40, y1: 160,
      x2: -48, y2: 255,
      stroke: color, 'stroke-width': sw, 'stroke-linecap': 'round'
    }, 'shin_l');
    pelvis.appendChild(shinL);

    // ── BONE 30: foot_l ───────────────────────────────────────────
    const footL = el('path', {
      id: `${id}-foot-l`, 'data-bone': 'foot_l',
      d: 'M -48 255 L -48 265 L -72 265',
      stroke: color, 'stroke-width': sw, fill: 'none',
      'stroke-linecap': 'round', 'stroke-linejoin': 'round'
    }, 'foot_l');
    pelvis.appendChild(footL);

    // ── BONE 31: toe_l ────────────────────────────────────────────
    const toeL = el('line', {
      id: `${id}-toe-l`, 'data-bone': 'toe_l',
      x1: -72, y1: 265,
      x2: -84, y2: 265,
      stroke: color, 'stroke-width': sw - 2, 'stroke-linecap': 'round'
    }, 'toe_l');
    pelvis.appendChild(toeL);

    // ── BONE 32: hip_r ────────────────────────────────────────────
    const hipR = el('line', {
      id: `${id}-hip-r`, 'data-bone': 'hip_r',
      x1: 0, y1: 60,
      x2: 18, y2: 72,
      stroke: color, 'stroke-width': sw, 'stroke-linecap': 'round'
    }, 'hip_r');
    pelvis.appendChild(hipR);

    // ── BONE 33: thigh_r ──────────────────────────────────────────
    const thighR = el('line', {
      id: `${id}-thigh-r`, 'data-bone': 'thigh_r',
      x1: 18, y1: 72,
      x2: 40, y2: 160,
      stroke: color, 'stroke-width': sw + 1, 'stroke-linecap': 'round'
    }, 'thigh_r');
    pelvis.appendChild(thighR);

    // ── BONE 34: shin_r ───────────────────────────────────────────
    const shinR = el('line', {
      id: `${id}-shin-r`, 'data-bone': 'shin_r',
      x1: 40, y1: 160,
      x2: 48, y2: 255,
      stroke: color, 'stroke-width': sw, 'stroke-linecap': 'round'
    }, 'shin_r');
    pelvis.appendChild(shinR);

    // ── BONE 35: foot_r ───────────────────────────────────────────
    const footR = el('path', {
      id: `${id}-foot-r`, 'data-bone': 'foot_r',
      d: 'M 48 255 L 48 265 L 72 265',
      stroke: color, 'stroke-width': sw, fill: 'none',
      'stroke-linecap': 'round', 'stroke-linejoin': 'round'
    }, 'foot_r');
    pelvis.appendChild(footR);

    // ── BONE 36: toe_r ────────────────────────────────────────────
    const toeR = el('line', {
      id: `${id}-toe-r`, 'data-bone': 'toe_r',
      x1: 72, y1: 265,
      x2: 84, y2: 265,
      stroke: color, 'stroke-width': sw - 2, 'stroke-linecap': 'round'
    }, 'toe_r');
    pelvis.appendChild(toeR);

    this.svg.appendChild(root);
    console.log(`[GK Skeleton] Built ${Object.keys(this.bones).length} bones for rig "${id}"`);
  }

  // ─────────────────────────────────────────────
  //  PUBLIC API
  // ─────────────────────────────────────────────

  /** Get any bone SVG element by name */
  getBone(name) {
    return this.bones[name] || null;
  }

  /** Set any SVG attribute(s) on a bone directly */
  setBone(name, attrs) {
    const b = this.getBone(name);
    if (!b) return console.warn(`[GK Skeleton] Bone not found: ${name}`);
    for (const [k, v] of Object.entries(attrs)) b.setAttribute(k, v);
  }

  /** List all bone names */
  getBoneNames() {
    return Object.keys(this.bones);
  }

  /**
   * GSAP animate one or more bones to new attribute states.
   * @param {object} boneMap  { boneName: { attr1: val, ... }, ... }
   * @param {number} duration seconds
   * @param {string} ease     GSAP ease string
   * @returns {gsap.core.Timeline}
   */
  animateBones(boneMap, duration = 0.45, ease = 'power2.inOut') {
    if (!window.gsap) return console.error('[GK Skeleton] GSAP not found!');
    const tl = gsap.timeline();
    for (const [boneName, attrs] of Object.entries(boneMap)) {
      const b = this.getBone(boneName);
      if (!b) continue;
      tl.to(b, { attr: attrs, duration, ease }, 0);
    }
    return tl;
  }

  /**
   * Snap to a named pose instantly (no animation).
   * @param {string} poseName
   */
  pose(poseName) {
    const p = GKStickmanSkeleton.POSES[poseName];
    if (!p) return console.warn(`[GK Skeleton] Pose not found: ${poseName}`);
    for (const [boneName, attrs] of Object.entries(p)) {
      this.setBone(boneName, attrs);
    }
  }

  /**
   * Smoothly animate to a named pose via GSAP.
   * @param {string} poseName
   * @param {number} duration
   * @param {string} ease
   */
  animate(poseName, duration = 0.5, ease = 'power2.inOut') {
    const p = GKStickmanSkeleton.POSES[poseName];
    if (!p) return console.warn(`[GK Skeleton] Pose not found: ${poseName}`);
    return this.animateBones(p, duration, ease);
  }

  /**
   * Run the natural idle breathing loop on the rig.
   * Returns the GSAP timeline so you can .kill() it.
   */
  startBreathing() {
    if (!window.gsap) return;
    const id = this.cfg.id;
    const tl = gsap.timeline({ repeat: -1, yoyo: true });
    // Spine subtle bob
    tl.to(`#${id}-spine-upper`, { attr: { y2: -112, y1: -47 }, duration: 1.4, ease: 'sine.inOut' }, 0);
    // Neck/head bob
    tl.to(`#${id}-neck`,        { attr: { y1: -112, y2: -125 }, duration: 1.4, ease: 'sine.inOut' }, 0);
    tl.to(this.bones['head'],   { y: 3, duration: 1.4, ease: 'sine.inOut' }, 0);
    // Shoulder rise
    tl.to(this.bones['shoulder_l'], { attr: { y1: -97, y2: -103 }, duration: 1.4, ease: 'sine.inOut' }, 0);
    tl.to(this.bones['shoulder_r'], { attr: { y1: -97, y2: -103 }, duration: 1.4, ease: 'sine.inOut' }, 0);
    this._breathingTl = tl;
    return tl;
  }

  stopBreathing() {
    if (this._breathingTl) this._breathingTl.kill();
  }

  /**
   * Run a looping walk cycle on the rig.
   * @param {number} speed  Cycle duration in seconds (lower = faster walk)
   */
  startWalk(speed = 0.55) {
    if (!window.gsap) return;
    const id = this.cfg.id;
    const tl = gsap.timeline({ repeat: -1 });

    // Phase A: Left leg forward, right leg back
    tl.to(this.bones['thigh_l'],  { attr: { x2: -20, y2: 155 }, duration: speed, ease: 'sine.inOut' }, 0);
    tl.to(this.bones['shin_l'],   { attr: { x1: -20, y1: 155, x2: -15, y2: 255 }, duration: speed, ease: 'sine.inOut' }, 0);
    tl.to(this.bones['foot_l'],   { attr: { d: 'M -15 255 L -15 265 L -40 265' }, duration: speed, ease: 'sine.inOut' }, 0);
    tl.to(this.bones['thigh_r'],  { attr: { x2: 55, y2: 165 }, duration: speed, ease: 'sine.inOut' }, 0);
    tl.to(this.bones['shin_r'],   { attr: { x1: 55, y1: 165, x2: 65, y2: 255 }, duration: speed, ease: 'sine.inOut' }, 0);
    // Opposing arm swings
    tl.to(this.bones['upperarm_l'],{ attr: { x2: -72, y2: -55 }, duration: speed, ease: 'sine.inOut' }, 0);
    tl.to(this.bones['forearm_l'], { attr: { x1: -72, y1: -55, x2: -95, y2: -20 }, duration: speed, ease: 'sine.inOut' }, 0);
    tl.to(this.bones['upperarm_r'],{ attr: { x2: 45, y2: -65 }, duration: speed, ease: 'sine.inOut' }, 0);
    tl.to(this.bones['forearm_r'], { attr: { x1: 45, y1: -65, x2: 60, y2: -15 }, duration: speed, ease: 'sine.inOut' }, 0);
    // Pelvis bob
    tl.to(this.root, { y: `+=${this.cfg.y + 8}`, duration: speed / 2, ease: 'sine.inOut', yoyo: true, repeat: 1 }, 0);

    // Phase B: Right leg forward, left leg back
    tl.to(this.bones['thigh_r'],  { attr: { x2: 20, y2: 155 }, duration: speed, ease: 'sine.inOut' });
    tl.to(this.bones['shin_r'],   { attr: { x1: 20, y1: 155, x2: 15, y2: 255 }, duration: speed, ease: 'sine.inOut' }, `<`);
    tl.to(this.bones['foot_r'],   { attr: { d: 'M 15 255 L 15 265 L 40 265' } , duration: speed, ease: 'sine.inOut' }, `<`);
    tl.to(this.bones['thigh_l'],  { attr: { x2: -55, y2: 165 }, duration: speed, ease: 'sine.inOut' }, `<`);
    tl.to(this.bones['shin_l'],   { attr: { x1: -55, y1: 165, x2: -65, y2: 255 }, duration: speed, ease: 'sine.inOut' }, `<`);
    tl.to(this.bones['upperarm_r'],{ attr: { x2: 72, y2: -55 }, duration: speed, ease: 'sine.inOut' }, `<`);
    tl.to(this.bones['forearm_r'], { attr: { x1: 72, y1: -55, x2: 95, y2: -20 }, duration: speed, ease: 'sine.inOut' }, `<`);
    tl.to(this.bones['upperarm_l'],{ attr: { x2: -45, y2: -65 }, duration: speed, ease: 'sine.inOut' }, `<`);
    tl.to(this.bones['forearm_l'], { attr: { x1: -45, y1: -65, x2: -60, y2: -15 }, duration: speed, ease: 'sine.inOut' }, `<`);

    this._walkTl = tl;
    return tl;
  }

  stopWalk() {
    if (this._walkTl) this._walkTl.kill();
    this.animate('idle', 0.3);
  }

  /**
   * Run a full-body rhythmic DANCE routine on all 36 bones!
   * @param {string} style  'hiphop' | 'disco' | 'wave'
   * @param {number} bpm    Beats per minute (default: 124)
   * @returns {gsap.core.Timeline}
   */
  startDance(style = 'hiphop', bpm = 124) {
    if (!window.gsap) return;
    this.stopDance();
    this.stopBreathing();
    this.stopWalk();

    const beat = 60 / bpm; // ~0.484s per beat
    const id = this.cfg.id;
    const tl = gsap.timeline({ repeat: -1 });

    if (style === 'disco') {
      // 🕺 DISCO STYLE — Classic Travolta Diagonal Points & Hip Thrusts
      // Beat 1: Right arm points high 45°, Left hand on hip, Left hip thrust
      tl.to(this.bones['pelvis'],     { x: -14, y: 8, duration: beat, ease: 'power2.out' }, 0);
      tl.to(this.bones['spine_lower'],{ attr: { x1: 0, y1: 60, x2: -8, y2: 10 }, duration: beat, ease: 'power2.out' }, 0);
      tl.to(this.bones['spine_upper'],{ attr: { x1: -5, y1: -50, x2: 12, y2: -115 }, duration: beat, ease: 'power2.out' }, 0);
      tl.to(this.bones['head'],       { x: 12, y: -4, rotation: 12, duration: beat, ease: 'power2.out' }, 0);
      tl.to(this.bones['mouth'],      { attr: { d: 'M -12 -147 Q 0 -136 12 -147' }, duration: beat * 0.5 }, 0);
      tl.to(this.bones['eyebrow_r'],  { attr: { d: 'M 6 -183 L 20 -180' }, duration: beat * 0.5 }, 0);
      // Right arm high diagonal
      tl.to(this.bones['shoulder_r'], { attr: { x1: 0, y1: -100, x2: 32, y2: -110 }, duration: beat, ease: 'back.out(1.8)' }, 0);
      tl.to(this.bones['upperarm_r'], { attr: { x1: 32, y1: -110, x2: 75, y2: -150 }, duration: beat, ease: 'back.out(1.8)' }, 0);
      tl.to(this.bones['forearm_r'],  { attr: { x1: 75, y1: -150, x2: 115, y2: -195 }, duration: beat, ease: 'back.out(1.8)' }, 0);
      tl.to(this.bones['hand_r'],     { x: 30, y: -180, duration: beat, ease: 'back.out(1.8)' }, 0);
      tl.to(this.bones['index_r'],    { attr: { x1: 115, y1: -195, x2: 132, y2: -215 }, duration: beat }, 0);
      // Left arm on left hip
      tl.to(this.bones['shoulder_l'], { attr: { x1: 0, y1: -100, x2: -28, y2: -100 }, duration: beat }, 0);
      tl.to(this.bones['upperarm_l'], { attr: { x1: -28, y1: -100, x2: -58, y2: -50 }, duration: beat }, 0);
      tl.to(this.bones['forearm_l'],  { attr: { x1: -58, y1: -50, x2: -35, y2: 60 }, duration: beat }, 0);
      // Legs: Left knee pop, Right leg straight
      tl.to(this.bones['thigh_l'],    { attr: { x1: -18, y1: 72, x2: -50, y2: 150 }, duration: beat }, 0);
      tl.to(this.bones['shin_l'],     { attr: { x1: -50, y1: 150, x2: -42, y2: 245 }, duration: beat }, 0);
      tl.to(this.bones['foot_l'],     { attr: { d: 'M -42 245 L -35 255 L -62 255' }, duration: beat }, 0);
      tl.to(this.bones['thigh_r'],    { attr: { x1: 18, y1: 72, x2: 38, y2: 165 }, duration: beat }, 0);
      tl.to(this.bones['shin_r'],     { attr: { x1: 38, y1: 165, x2: 45, y2: 255 }, duration: beat }, 0);

      // Beat 2: Right arm points down-left across chest
      tl.to(this.bones['pelvis'],     { x: 10, y: 14, duration: beat, ease: 'power2.inOut' }, beat);
      tl.to(this.bones['spine_upper'],{ attr: { x1: 0, y1: -50, x2: -8, y2: -110 }, duration: beat }, beat);
      tl.to(this.bones['head'],       { x: -8, y: 0, rotation: -8, duration: beat }, beat);
      tl.to(this.bones['upperarm_r'], { attr: { x1: 28, y1: -105, x2: -15, y2: -45 }, duration: beat, ease: 'power2.inOut' }, beat);
      tl.to(this.bones['forearm_r'],  { attr: { x1: -15, y1: -45, x2: -65, y2: 15 }, duration: beat, ease: 'power2.inOut' }, beat);
      tl.to(this.bones['hand_r'],     { x: -150, y: 30, duration: beat }, beat);
      tl.to(this.bones['index_r'],    { attr: { x1: -65, y1: 15, x2: -82, y2: 35 }, duration: beat }, beat);

      // Beat 3: Left arm points high 45° up-left, Right hand on right hip
      tl.to(this.bones['pelvis'],     { x: 14, y: 8, duration: beat, ease: 'power2.out' }, beat * 2);
      tl.to(this.bones['spine_lower'],{ attr: { x1: 0, y1: 60, x2: 8, y2: 10 }, duration: beat }, beat * 2);
      tl.to(this.bones['spine_upper'],{ attr: { x1: 5, y1: -50, x2: -12, y2: -115 }, duration: beat }, beat * 2);
      tl.to(this.bones['head'],       { x: -12, y: -4, rotation: -12, duration: beat }, beat * 2);
      tl.to(this.bones['eyebrow_l'],  { attr: { d: 'M -20 -183 L -6 -180' }, duration: beat * 0.5 }, beat * 2);
      // Left arm high diagonal
      tl.to(this.bones['shoulder_l'], { attr: { x1: 0, y1: -100, x2: -32, y2: -110 }, duration: beat, ease: 'back.out(1.8)' }, beat * 2);
      tl.to(this.bones['upperarm_l'], { attr: { x1: -32, y1: -110, x2: -75, y2: -150 }, duration: beat, ease: 'back.out(1.8)' }, beat * 2);
      tl.to(this.bones['forearm_l'],  { attr: { x1: -75, y1: -150, x2: -115, y2: -195 }, duration: beat, ease: 'back.out(1.8)' }, beat * 2);
      tl.to(this.bones['hand_l'],     { x: -30, y: -180, duration: beat }, beat * 2);
      tl.to(this.bones['index_l'],    { attr: { x1: -115, y1: -195, x2: -132, y2: -215 }, duration: beat }, beat * 2);
      // Right arm on right hip
      tl.to(this.bones['shoulder_r'], { attr: { x1: 0, y1: -100, x2: 28, y2: -100 }, duration: beat }, beat * 2);
      tl.to(this.bones['upperarm_r'], { attr: { x1: 28, y1: -100, x2: 58, y2: -50 }, duration: beat }, beat * 2);
      tl.to(this.bones['forearm_r'],  { attr: { x1: 58, y1: -50, x2: 35, y2: 60 }, duration: beat }, beat * 2);
      tl.to(this.bones['hand_r'],     { x: -50, y: 75, duration: beat }, beat * 2);
      // Legs: Right knee pop, Left leg straight
      tl.to(this.bones['thigh_r'],    { attr: { x1: 18, y1: 72, x2: 50, y2: 150 }, duration: beat }, beat * 2);
      tl.to(this.bones['shin_r'],     { attr: { x1: 50, y1: 150, x2: 42, y2: 245 }, duration: beat }, beat * 2);
      tl.to(this.bones['foot_r'],     { attr: { d: 'M 42 245 L 35 255 L 62 255' }, duration: beat }, beat * 2);
      tl.to(this.bones['thigh_l'],    { attr: { x1: -18, y1: 72, x2: -38, y2: 165 }, duration: beat }, beat * 2);
      tl.to(this.bones['shin_l'],     { attr: { x1: -38, y1: 165, x2: -45, y2: 255 }, duration: beat }, beat * 2);

      // Beat 4: Left arm points down-right across chest + reset
      tl.to(this.bones['pelvis'],     { x: -10, y: 14, duration: beat, ease: 'power2.inOut' }, beat * 3);
      tl.to(this.bones['upperarm_l'], { attr: { x1: -28, y1: -105, x2: 15, y2: -45 }, duration: beat }, beat * 3);
      tl.to(this.bones['forearm_l'],  { attr: { x1: 15, y1: -45, x2: 65, y2: 15 }, duration: beat }, beat * 3);
      tl.to(this.bones['hand_l'],     { x: 150, y: 30, duration: beat }, beat * 3);
      tl.to(this.bones['index_l'],    { attr: { x1: 65, y1: 15, x2: 82, y2: 35 }, duration: beat }, beat * 3);

    } else if (style === 'wave') {
      // 🌊 LIQUID WAVE STYLE — Arm waves from finger to finger with body undulation
      const step = beat * 0.35;
      // Phase 1: Left fingers flex up
      tl.to(this.bones['thumb_l'],    { attr: { x2: -104, y2: -35 }, duration: step }, 0);
      tl.to(this.bones['index_l'],    { attr: { x2: -102, y2: -18 }, duration: step }, 0);
      tl.to(this.bones['forearm_l'],  { attr: { x1: -65, y1: -65, x2: -90, y2: -35 }, duration: step }, step * 0.5);
      tl.to(this.bones['upperarm_l'], { attr: { x1: -28, y1: -105, x2: -65, y2: -65 }, duration: step }, step);
      tl.to(this.bones['shoulder_l'], { attr: { y1: -95, y2: -115 }, duration: step }, step * 1.5);

      // Phase 2: Wave passes through chest and spine
      tl.to(this.bones['spine_upper'],{ attr: { x1: 0, y1: -45, x2: 10, y2: -118 }, duration: step }, step * 2);
      tl.to(this.bones['neck'],       { attr: { x1: 10, y1: -118, x2: 15, y2: -130 }, duration: step }, step * 2.2);
      tl.to(this.bones['head'],       { rotation: 14, x: 8, duration: step }, step * 2.2);
      tl.to(this.bones['eye_r'],      { scaleY: 0.1, duration: 0.12, yoyo: true, repeat: 1 }, step * 2.5); // Wink!

      // Phase 3: Wave exits right shoulder to right fingers
      tl.to(this.bones['shoulder_r'], { attr: { y1: -95, y2: -115 }, duration: step }, step * 3);
      tl.to(this.bones['upperarm_r'], { attr: { x1: 28, y1: -105, x2: 70, y2: -75 }, duration: step }, step * 3.5);
      tl.to(this.bones['forearm_r'],  { attr: { x1: 70, y1: -75, x2: 105, y2: -50 }, duration: step }, step * 4);
      tl.to(this.bones['thumb_r'],    { attr: { x2: 118, y2: -60 }, duration: step }, step * 4.5);
      tl.to(this.bones['index_r'],    { attr: { x2: 115, y2: -40 }, duration: step }, step * 4.5);

      // Phase 4: Knee dip and reverse wave back!
      tl.to(this.bones['pelvis'],     { y: 18, duration: step * 2, yoyo: true, repeat: 1, ease: 'sine.inOut' }, step * 2);
      tl.to(this.bones['thigh_l'],    { attr: { x2: -48, y2: 148 }, duration: step * 2, yoyo: true, repeat: 1 }, step * 2);
      tl.to(this.bones['thigh_r'],    { attr: { x2: 48, y2: 148 }, duration: step * 2, yoyo: true, repeat: 1 }, step * 2);

    } else {
      // ⚡ HIP-HOP / POPPIN GROOVE (Default) — Full 4-Beat Multi-Bone Dance
      // Beat 1: Left Hip Drop + Right Arm High Pump + Neck/Head Bob
      tl.to(this.bones['pelvis'],     { x: -16, y: 15, duration: beat * 0.7, ease: 'back.out(2)' }, 0);
      tl.to(this.bones['spine_lower'],{ attr: { x1: 0, y1: 60, x2: -10, y2: 12 }, duration: beat * 0.7 }, 0);
      tl.to(this.bones['spine_mid'],  { attr: { x1: -10, y1: 12, x2: -4, y2: -50 }, duration: beat * 0.7 }, 0);
      tl.to(this.bones['spine_upper'],{ attr: { x1: -4, y1: -50, x2: 6, y2: -112 }, duration: beat * 0.7 }, 0);
      tl.to(this.bones['neck'],       { attr: { x1: 6, y1: -112, x2: 10, y2: -124 }, duration: beat * 0.7 }, 0);
      tl.to(this.bones['head'],       { x: 10, y: 6, rotation: 10, duration: beat * 0.7, ease: 'back.out(2)' }, 0);
      tl.to(this.bones['mouth'],      { attr: { d: 'M -12 -147 Q 0 -137 12 -147' }, duration: beat * 0.4 }, 0);
      tl.to(this.bones['eyebrow_l'],  { attr: { d: 'M -20 -184 L -6 -182' }, duration: beat * 0.4 }, 0);
      tl.to(this.bones['eyebrow_r'],  { attr: { d: 'M 6 -182 L 20 -184' }, duration: beat * 0.4 }, 0);

      // Arms: Right high pump, Left low flex
      tl.to(this.bones['shoulder_r'], { attr: { x1: 0, y1: -100, x2: 28, y2: -112 }, duration: beat * 0.6 }, 0);
      tl.to(this.bones['upperarm_r'], { attr: { x1: 28, y1: -112, x2: 70, y2: -130 }, duration: beat * 0.6, ease: 'back.out(2)' }, 0);
      tl.to(this.bones['forearm_r'],  { attr: { x1: 70, y1: -130, x2: 60, y2: -185 }, duration: beat * 0.6, ease: 'back.out(2)' }, 0);
      tl.to(this.bones['hand_r'],     { x: -25, y: -170, duration: beat * 0.6 }, 0);
      tl.to(this.bones['shoulder_l'], { attr: { x1: 0, y1: -100, x2: -28, y2: -95 }, duration: beat * 0.6 }, 0);
      tl.to(this.bones['upperarm_l'], { attr: { x1: -28, y1: -95, x2: -65, y2: -45 }, duration: beat * 0.6 }, 0);
      tl.to(this.bones['forearm_l'],  { attr: { x1: -65, y1: -45, x2: -45, y2: 15 }, duration: beat * 0.6 }, 0);

      // Legs: Left knee bends deep, right leg extends with heel tap
      tl.to(this.bones['thigh_l'],    { attr: { x1: -18, y1: 72, x2: -48, y2: 152 }, duration: beat * 0.7 }, 0);
      tl.to(this.bones['shin_l'],     { attr: { x1: -48, y1: 152, x2: -40, y2: 242 }, duration: beat * 0.7 }, 0);
      tl.to(this.bones['foot_l'],     { attr: { d: 'M -40 242 L -35 252 L -65 252' }, duration: beat * 0.7 }, 0);
      tl.to(this.bones['thigh_r'],    { attr: { x1: 18, y1: 72, x2: 52, y2: 162 }, duration: beat * 0.7 }, 0);
      tl.to(this.bones['shin_r'],     { attr: { x1: 52, y1: 162, x2: 65, y2: 250 }, duration: beat * 0.7 }, 0);
      tl.to(this.bones['foot_r'],     { attr: { d: 'M 65 250 L 72 260 L 98 250' }, duration: beat * 0.7 }, 0); // Toe up heel tap!

      // Beat 2: Center Chest Pop & Jazz Hands Clap!
      tl.to(this.bones['pelvis'],     { x: 0, y: -6, duration: beat * 0.5, ease: 'power3.out' }, beat);
      tl.to(this.bones['spine_upper'],{ attr: { x1: 0, y1: -50, x2: 0, y2: -120 }, duration: beat * 0.5 }, beat); // Arch high!
      tl.to(this.bones['head'],       { x: 0, y: -8, rotation: 0, duration: beat * 0.5, ease: 'power3.out' }, beat);
      tl.to(this.bones['mouth'],      { attr: { d: 'M -8 -148 A 6 8 0 1 0 8 -148 A 6 8 0 1 0 -8 -148' }, duration: beat * 0.3 }, beat); // Pop 'O' mouth!
      // Arms snap forward together
      tl.to(this.bones['upperarm_l'], { attr: { x1: -28, y1: -105, x2: -45, y2: -65 }, duration: beat * 0.5, ease: 'back.out(2.5)' }, beat);
      tl.to(this.bones['forearm_l'],  { attr: { x1: -45, y1: -65, x2: -10, y2: -65 }, duration: beat * 0.5, ease: 'back.out(2.5)' }, beat);
      tl.to(this.bones['upperarm_r'], { attr: { x1: 28, y1: -105, x2: 45, y2: -65 }, duration: beat * 0.5, ease: 'back.out(2.5)' }, beat);
      tl.to(this.bones['forearm_r'],  { attr: { x1: 45, y1: -65, x2: 10, y2: -65 }, duration: beat * 0.5, ease: 'back.out(2.5)' }, beat);
      tl.to(this.bones['hand_l'],     { x: 75, y: -50, duration: beat * 0.5 }, beat);
      tl.to(this.bones['hand_r'],     { x: -75, y: -50, duration: beat * 0.5 }, beat);
      // Fingers spread wide
      tl.to(this.bones['thumb_l'],    { attr: { x2: -98, y2: -28 }, duration: beat * 0.4 }, beat);
      tl.to(this.bones['index_l'],    { attr: { x2: -96, y2: -2 }, duration: beat * 0.4 }, beat);
      tl.to(this.bones['pinky_l'],    { attr: { x2: -96, y2: -32 }, duration: beat * 0.4 }, beat);
      tl.to(this.bones['thumb_r'],    { attr: { x2: 98, y2: -28 }, duration: beat * 0.4 }, beat);
      tl.to(this.bones['index_r'],    { attr: { x2: 96, y2: -2 }, duration: beat * 0.4 }, beat);
      tl.to(this.bones['pinky_r'],    { attr: { x2: 96, y2: -32 }, duration: beat * 0.4 }, beat);
      // Legs straight
      tl.to(this.bones['thigh_l'],    { attr: { x1: -18, y1: 72, x2: -35, y2: 160 }, duration: beat * 0.5 }, beat);
      tl.to(this.bones['shin_l'],     { attr: { x1: -35, y1: 160, x2: -42, y2: 255 }, duration: beat * 0.5 }, beat);
      tl.to(this.bones['foot_l'],     { attr: { d: 'M -42 255 L -42 265 L -68 265' }, duration: beat * 0.5 }, beat);
      tl.to(this.bones['thigh_r'],    { attr: { x1: 18, y1: 72, x2: 35, y2: 160 }, duration: beat * 0.5 }, beat);
      tl.to(this.bones['shin_r'],     { attr: { x1: 35, y1: 160, x2: 42, y2: 255 }, duration: beat * 0.5 }, beat);
      tl.to(this.bones['foot_r'],     { attr: { d: 'M 42 255 L 42 265 L 68 265' }, duration: beat * 0.5 }, beat);

      // Beat 3: Right Hip Drop + Left Arm High Pump + Right Wink!
      tl.to(this.bones['pelvis'],     { x: 16, y: 15, duration: beat * 0.7, ease: 'back.out(2)' }, beat * 2);
      tl.to(this.bones['spine_lower'],{ attr: { x1: 0, y1: 60, x2: 10, y2: 12 }, duration: beat * 0.7 }, beat * 2);
      tl.to(this.bones['spine_mid'],  { attr: { x1: 10, y1: 12, x2: 4, y2: -50 }, duration: beat * 0.7 }, beat * 2);
      tl.to(this.bones['spine_upper'],{ attr: { x1: 4, y1: -50, x2: -6, y2: -112 }, duration: beat * 0.7 }, beat * 2);
      tl.to(this.bones['neck'],       { attr: { x1: -6, y1: -112, x2: -10, y2: -124 }, duration: beat * 0.7 }, beat * 2);
      tl.to(this.bones['head'],       { x: -10, y: 6, rotation: -10, duration: beat * 0.7, ease: 'back.out(2)' }, beat * 2);
      tl.to(this.bones['mouth'],      { attr: { d: 'M -12 -147 Q 0 -137 12 -147' }, duration: beat * 0.4 }, beat * 2);
      tl.to(this.bones['eye_l'],      { scaleY: 0.1, duration: 0.12, yoyo: true, repeat: 1 }, beat * 2.2); // Playful wink!

      // Arms: Left high pump, Right low flex
      tl.to(this.bones['shoulder_l'], { attr: { x1: 0, y1: -100, x2: -28, y2: -112 }, duration: beat * 0.6 }, beat * 2);
      tl.to(this.bones['upperarm_l'], { attr: { x1: -28, y1: -112, x2: -70, y2: -130 }, duration: beat * 0.6, ease: 'back.out(2)' }, beat * 2);
      tl.to(this.bones['forearm_l'],  { attr: { x1: -70, y1: -130, x2: -60, y2: -185 }, duration: beat * 0.6, ease: 'back.out(2)' }, beat * 2);
      tl.to(this.bones['hand_l'],     { x: 25, y: -170, duration: beat * 0.6 }, beat * 2);
      tl.to(this.bones['shoulder_r'], { attr: { x1: 0, y1: -100, x2: 28, y2: -95 }, duration: beat * 0.6 }, beat * 2);
      tl.to(this.bones['upperarm_r'], { attr: { x1: 28, y1: -95, x2: 65, y2: -45 }, duration: beat * 0.6 }, beat * 2);
      tl.to(this.bones['forearm_r'],  { attr: { x1: 65, y1: -45, x2: 45, y2: 15 }, duration: beat * 0.6 }, beat * 2);

      // Legs: Right knee bends deep, left leg extends with heel tap
      tl.to(this.bones['thigh_r'],    { attr: { x1: 18, y1: 72, x2: 48, y2: 152 }, duration: beat * 0.7 }, beat * 2);
      tl.to(this.bones['shin_r'],     { attr: { x1: 48, y1: 152, x2: 40, y2: 242 }, duration: beat * 0.7 }, beat * 2);
      tl.to(this.bones['foot_r'],     { attr: { d: 'M 40 242 L 35 252 L 65 252' }, duration: beat * 0.7 }, beat * 2);
      tl.to(this.bones['thigh_l'],    { attr: { x1: -18, y1: 72, x2: -52, y2: 162 }, duration: beat * 0.7 }, beat * 2);
      tl.to(this.bones['shin_l'],     { attr: { x1: -52, y1: 162, x2: -65, y2: 250 }, duration: beat * 0.7 }, beat * 2);
      tl.to(this.bones['foot_l'],     { attr: { d: 'M -65 250 L -72 260 L -98 250' }, duration: beat * 0.7 }, beat * 2); // Heel tap!

      // Beat 4: Low Groovy Squat Bounce + Smooth Reset
      tl.to(this.bones['pelvis'],     { x: 0, y: 22, duration: beat * 0.6, ease: 'sine.inOut' }, beat * 3);
      tl.to(this.bones['thigh_l'],    { attr: { x1: -18, y1: 72, x2: -50, y2: 140 }, duration: beat * 0.6 }, beat * 3);
      tl.to(this.bones['shin_l'],     { attr: { x1: -50, y1: 140, x2: -35, y2: 235 }, duration: beat * 0.6 }, beat * 3);
      tl.to(this.bones['thigh_r'],    { attr: { x1: 18, y1: 72, x2: 50, y2: 140 }, duration: beat * 0.6 }, beat * 3);
      tl.to(this.bones['shin_r'],     { attr: { x1: 50, y1: 140, x2: 35, y2: 235 }, duration: beat * 0.6 }, beat * 3);
      tl.to(this.bones['upperarm_l'], { attr: { x1: -28, y1: -105, x2: -58, y2: -60 }, duration: beat * 0.6 }, beat * 3);
      tl.to(this.bones['forearm_l'],  { attr: { x1: -58, y1: -60, x2: -85, y2: -15 }, duration: beat * 0.6 }, beat * 3);
      tl.to(this.bones['upperarm_r'], { attr: { x1: 28, y1: -105, x2: 58, y2: -60 }, duration: beat * 0.6 }, beat * 3);
      tl.to(this.bones['forearm_r'],  { attr: { x1: 58, y1: -60, x2: 85, y2: -15 }, duration: beat * 0.6 }, beat * 3);
      tl.to(this.bones['hand_l'],     { x: 0, y: 0, duration: beat * 0.6 }, beat * 3);
      tl.to(this.bones['hand_r'],     { x: 0, y: 0, duration: beat * 0.6 }, beat * 3);
    }

    this._danceTl = tl;
    return tl;
  }

  stopDance() {
    if (this._danceTl) this._danceTl.kill();
    this.animate('idle', 0.35);
  }

  // ─────────────────────────────────────────────
  //  STATIC: Named Pose Library
  //  Each pose maps boneName → new SVG attributes
  // ─────────────────────────────────────────────
  static get POSES() {
    return {

      // ── Idle — Natural relaxed stand ──────────────────────────────
      idle: {
        spine_lower:  { x1: 0, y1: 60,   x2: 0, y2: 10   },
        spine_mid:    { x1: 0, y1: 10,   x2: 0, y2: -50  },
        spine_upper:  { x1: 0, y1: -50,  x2: 0, y2: -115 },
        neck:         { x1: 0, y1: -115, x2: 0, y2: -128 },
        shoulder_l:   { x1: 0, y1: -100, x2: -28, y2: -105 },
        shoulder_r:   { x1: 0, y1: -100, x2:  28, y2: -105 },
        upperarm_l:   { x1: -28, y1: -105, x2: -60, y2: -60 },
        forearm_l:    { x1: -60, y1: -60,  x2: -85, y2: -15 },
        upperarm_r:   { x1:  28, y1: -105, x2:  60, y2: -60 },
        forearm_r:    { x1:  60, y1: -60,  x2:  85, y2: -15 },
        hip_l:        { x1: 0, y1: 60, x2: -18, y2: 72  },
        thigh_l:      { x1: -18, y1: 72,  x2: -40, y2: 160 },
        shin_l:       { x1: -40, y1: 160, x2: -48, y2: 255 },
        hip_r:        { x1: 0, y1: 60, x2:  18, y2: 72  },
        thigh_r:      { x1:  18, y1: 72,  x2:  40, y2: 160 },
        shin_r:       { x1:  40, y1: 160, x2:  48, y2: 255 },
        foot_l:       { d: 'M -48 255 L -48 265 L -72 265' },
        foot_r:       { d: 'M  48 255 L  48 265 L  72 265' },
        eyebrow_l:    { d: 'M -20 -178 L -6 -180'  },
        eyebrow_r:    { d: 'M 6 -180 L 20 -178'    },
        mouth:        { d: 'M -10 -150 Q 0 -144 10 -150' },
      },

      // ── Phone Call — Right arm raised to ear ──────────────────────
      phone_call: {
        upperarm_r: { x1: 28, y1: -105, x2: 55, y2: -125 },
        forearm_r:  { x1: 55, y1: -125, x2: 68, y2: -155 },
        upperarm_l: { x1: -28, y1: -105, x2: -50, y2: -55 },
        forearm_l:  { x1: -50, y1: -55,  x2: -55, y2: -5  },
        eyebrow_l:  { d: 'M -20 -182 L -6 -184' },
        eyebrow_r:  { d: 'M 6 -184 L 20 -182'   },
        mouth:      { d: 'M -8 -150 L 8 -150'   },
      },

      // ── Pointing Up — Right arm raised 45° diagonal ───────────────
      pointing_up: {
        upperarm_r: { x1: 28, y1: -105, x2: 65, y2: -130 },
        forearm_r:  { x1: 65, y1: -130, x2: 100, y2: -178 },
        upperarm_l: { x1: -28, y1: -105, x2: -45, y2: -55 },
        forearm_l:  { x1: -45, y1: -55,  x2: -55, y2: -5  },
        eyebrow_l:  { d: 'M -20 -177 L -6 -179' },
        eyebrow_r:  { d: 'M 6 -179 L 20 -177'   },
        mouth:      { d: 'M -12 -147 Q 0 -138 12 -147' },
      },

      // ── Shocked — Both arms up, wide stance ───────────────────────
      shocked: {
        upperarm_l: { x1: -28, y1: -105, x2: -60, y2: -140 },
        forearm_l:  { x1: -60, y1: -140, x2: -40, y2: -190 },
        upperarm_r: { x1:  28, y1: -105, x2:  60, y2: -140 },
        forearm_r:  { x1:  60, y1: -140, x2:  40, y2: -190 },
        thigh_l:    { x1: -18, y1: 72, x2: -60, y2: 155 },
        shin_l:     { x1: -60, y1: 155, x2: -80, y2: 250 },
        thigh_r:    { x1:  18, y1: 72, x2:  60, y2: 155 },
        shin_r:     { x1:  60, y1: 155, x2:  80, y2: 250 },
        eyebrow_l:  { d: 'M -20 -182 L -6 -187' },
        eyebrow_r:  { d: 'M 6 -187 L 20 -182'   },
        mouth:      { d: 'M -8 -148 A 7 10 0 1 0 8 -148 A 7 10 0 1 0 -8 -148' },
      },

      // ── Thinking — Right hand near chin, slight head tilt ─────────
      thinking: {
        upperarm_r: { x1: 28, y1: -105, x2: 50, y2: -65 },
        forearm_r:  { x1: 50, y1: -65,  x2: 25, y2: -145 },
        upperarm_l: { x1: -28, y1: -105, x2: -45, y2: -55 },
        forearm_l:  { x1: -45, y1: -55,  x2: -20, y2: -50 },
        eyebrow_l:  { d: 'M -20 -178 L -6 -180' },
        eyebrow_r:  { d: 'M 6 -183 L 20 -179'   },
        mouth:      { d: 'M -8 -150 L 8 -152'   },
      },

      // ── Crouching — Knees bent, hunched forward ───────────────────
      crouching: {
        spine_upper: { x1: 0, y1: -50, x2: -15, y2: -105 },
        neck:        { x1: -15, y1: -105, x2: -20, y2: -120 },
        thigh_l:     { x1: -18, y1: 72, x2: -55, y2: 130 },
        shin_l:      { x1: -55, y1: 130, x2: -30, y2: 215 },
        foot_l:      { d: 'M -30 215 L -28 228 L -55 228' },
        thigh_r:     { x1:  18, y1: 72, x2:  55, y2: 130 },
        shin_r:      { x1:  55, y1: 130, x2:  30, y2: 215 },
        foot_r:      { d: 'M  30 215 L  28 228 L  55 228' },
        upperarm_l:  { x1: -28, y1: -100, x2: -58, y2: -55 },
        forearm_l:   { x1: -58, y1: -55,  x2: -78, y2: -10 },
        upperarm_r:  { x1:  28, y1: -100, x2:  58, y2: -55 },
        forearm_r:   { x1:  58, y1: -55,  x2:  78, y2: -10 },
      },

      // ── Peephole — Leaning forward, hand on door ──────────────────
      peephole: {
        spine_upper: { x1: 0, y1: -50, x2: 15, y2: -112 },
        neck:        { x1: 15, y1: -112, x2: 22, y2: -126 },
        upperarm_r:  { x1: 28, y1: -100, x2: 65, y2: -90 },
        forearm_r:   { x1: 65, y1: -90,  x2: 95, y2: -78 },
        upperarm_l:  { x1: -28, y1: -100, x2: -50, y2: -55 },
        forearm_l:   { x1: -50, y1: -55,  x2: -60, y2: -5  },
        thigh_l:     { x1: -18, y1: 72, x2: -32, y2: 155 },
        shin_l:      { x1: -32, y1: 155, x2: -38, y2: 255 },
        thigh_r:     { x1:  18, y1: 72, x2:  28, y2: 160 },
        shin_r:      { x1:  28, y1: 160, x2:  35, y2: 255 },
      },

      // ── Foot Inspect — Looking down at feet, one leg raised ───────
      foot_inspect: {
        spine_upper: { x1: 0, y1: -50, x2: -8, y2: -112 },
        neck:        { x1: -8, y1: -112, x2: -12, y2: -126 },
        thigh_l:     { x1: -18, y1: 72, x2: -60, y2: 125 },
        shin_l:      { x1: -60, y1: 125, x2: -50, y2: 190 },
        foot_l:      { d: 'M -50 190 L -50 200 L -80 200' },
        thigh_r:     { x1:  18, y1: 72, x2:  40, y2: 160 },
        shin_r:      { x1:  40, y1: 160, x2:  48, y2: 255 },
        upperarm_l:  { x1: -28, y1: -100, x2: -55, y2: -55 },
        forearm_l:   { x1: -55, y1: -55,  x2: -70, y2: -10 },
        upperarm_r:  { x1:  28, y1: -100, x2:  55, y2: -55 },
        forearm_r:   { x1:  55, y1: -55,  x2:  70, y2: -10 },
        eyebrow_l:   { d: 'M -20 -180 L -6 -182' },
        eyebrow_r:   { d: 'M 6 -182 L 20 -180'   },
        mouth:       { d: 'M -8 -150 Q 0 -155 8 -150' },
      },

      // ── Frozen Horror — Stiff upright, fear ──────────────────────
      frozen_horror: {
        upperarm_l:  { x1: -28, y1: -105, x2: -55, y2: -65 },
        forearm_l:   { x1: -55, y1: -65,  x2: -72, y2: -20 },
        upperarm_r:  { x1:  28, y1: -105, x2:  55, y2: -65 },
        forearm_r:   { x1:  55, y1: -65,  x2:  72, y2: -20 },
        thigh_l:     { x1: -18, y1: 72, x2: -20, y2: 160 },
        shin_l:      { x1: -20, y1: 160, x2: -22, y2: 255 },
        thigh_r:     { x1:  18, y1: 72, x2:  20, y2: 160 },
        shin_r:      { x1:  20, y1: 160, x2:  22, y2: 255 },
        eyebrow_l:   { d: 'M -20 -186 L -6 -188' },
        eyebrow_r:   { d: 'M 6 -188 L 20 -186'   },
        mouth:       { d: 'M -6 -150 A 5 7 0 1 0 6 -150 A 5 7 0 1 0 -6 -150' },
      },

      // ── Flinch / Head snap ────────────────────────────────────────
      flinch: {
        spine_upper: { x1: 0, y1: -50, x2: -10, y2: -115 },
        upperarm_l:  { x1: -28, y1: -105, x2: -60, y2: -130 },
        forearm_l:   { x1: -60, y1: -130, x2: -50, y2: -170 },
        upperarm_r:  { x1:  28, y1: -105, x2:  40, y2: -55  },
        forearm_r:   { x1:  40, y1: -55,  x2:  55, y2: -5   },
        eyebrow_l:   { d: 'M -20 -183 L -6 -187' },
        eyebrow_r:   { d: 'M 6 -183 L 20 -187'   },
        mouth:       { d: 'M -10 -150 Q 0 -145 10 -150' },
      },

    }; // end POSES
  }
}

// ─────────────────────────────────────────────────────────────
//  BONE INDEX — All 36 Bones and Their Roles
// ─────────────────────────────────────────────────────────────
GKStickmanSkeleton.BONE_INDEX = {
  // Core Spine
  pelvis:       'Root anchor — parent of all bones. Translate to move whole body.',
  spine_lower:  'Lumbar spine segment (y: 60 → 10). Controls lower-back bend.',
  spine_mid:    'Mid-thoracic spine (y: 10 → -50). Controls torso lean.',
  spine_upper:  'Upper-thoracic spine (y: -50 → -115). Controls chest forward/back tilt.',
  neck:         'Cervical spine (y: -115 → -128). Controls head pitch axis.',
  head:         'Skull group. Contains eyes, brows, mouth, sweat. Translate for nodding.',
  // Face
  eye_l:        'Left eye circle (cx=-13, cy=-168). Scale to wink/blink.',
  eye_r:        'Right eye circle (cx=13, cy=-168). Scale to wink/blink.',
  eyebrow_l:    'Left brow path. Change d= to tilt/raise for expressions.',
  eyebrow_r:    'Right brow path. Change d= to tilt/raise for expressions.',
  mouth:        'Mouth path. Change d= for smile/frown/open/scream.',
  sweat:        'Fear bead circle (cx=35, cy=-180). Set opacity=1 for horror beats.',
  // Left Arm Chain
  shoulder_l:   'Left clavicle (x1=0 → x2=-28). Controls arm root attachment point.',
  upperarm_l:   'Left humerus (shoulder → elbow). Primary arm swing bone.',
  forearm_l:    'Left ulna/radius (elbow → wrist). Controls lower arm angle.',
  hand_l:       'Left hand palm circle. Translate for hand-prop attachment.',
  thumb_l:      'Left thumb stub. Rotate for grip poses.',
  index_l:      'Left index finger. Extend for pointing.',
  pinky_l:      'Left pinky finger. Use for open-hand spread.',
  // Right Arm Chain
  shoulder_r:   'Right clavicle (x1=0 → x2=28). Controls arm root attachment point.',
  upperarm_r:   'Right humerus (shoulder → elbow). Phone-hold / pointing / gestures.',
  forearm_r:    'Right ulna/radius (elbow → wrist). Controls lower arm angle.',
  hand_r:       'Right hand palm circle. Translate for phone/prop attachment.',
  thumb_r:      'Right thumb stub.',
  index_r:      'Right index finger. Pointing / accusation gesture.',
  pinky_r:      'Right pinky finger.',
  // Left Leg Chain
  hip_l:        'Left iliac stub (y: 60 → 72). Controls leg hip-socket pivot.',
  thigh_l:      'Left femur (hip → knee). Controls leg swing and kick.',
  shin_l:       'Left tibia/fibula (knee → ankle). Controls lower leg bend.',
  foot_l:       'Left foot path (ankle → heel → toe). Change d= for step angles.',
  toe_l:        'Left toe line stub.',
  // Right Leg Chain
  hip_r:        'Right iliac stub (y: 60 → 72). Controls leg hip-socket pivot.',
  thigh_r:      'Right femur (hip → knee). Controls leg swing and kick.',
  shin_r:       'Right tibia/fibula (knee → ankle). Controls lower leg bend.',
  foot_r:       'Right foot path (ankle → heel → toe). Change d= for step angles.',
  toe_r:        'Right toe line stub.',
};

export default GKStickmanSkeleton;

