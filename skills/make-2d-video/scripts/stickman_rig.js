/**
 * Stickman Rig Generator — GrowKaz Studio
 * Generates and manipulates procedural 2D stickman SVG characters
 */

export class StickmanRig {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.options = {
      color: options.color || '#f8fafc',
      strokeWidth: options.strokeWidth || 7,
      scale: options.scale || 1,
      x: options.x || 540,
      y: options.y || 1100,
      ...options
    };
    this.init();
  }

  init() {
    const { color, strokeWidth, x, y, scale } = this.options;
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('id', 'stickman-actor');
    g.setAttribute('transform', `translate(${x}, ${y}) scale(${scale})`);

    g.innerHTML = `
      <!-- Spine -->
      <line class="sm-spine" x1="0" y1="-120" x2="0" y2="60" stroke="${color}" stroke-width="${strokeWidth + 1}" stroke-linecap="round"/>
      <!-- Head -->
      <circle class="sm-head" cx="0" cy="-160" r="38" fill="#0f172a" stroke="${color}" stroke-width="${strokeWidth}"/>
      <!-- Eyes -->
      <circle class="sm-eye-l" cx="-12" cy="-164" r="4" fill="${color}"/>
      <circle class="sm-eye-r" cx="12" cy="-164" r="4" fill="${color}"/>
      <!-- Mouth -->
      <path class="sm-mouth" d="M -10 -146 Q 0 -138 10 -146" stroke="${color}" stroke-width="4" fill="none" stroke-linecap="round"/>
      <!-- Left Arm -->
      <path class="sm-arm-l" d="M 0 -100 L -45 -50 L -80 -80" stroke="${color}" stroke-width="${strokeWidth}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Right Arm -->
      <path class="sm-arm-r" d="M 0 -100 L 45 -50 L 80 -10" stroke="${color}" stroke-width="${strokeWidth}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Left Leg -->
      <path class="sm-leg-l" d="M 0 60 L -35 140 L -45 240" stroke="${color}" stroke-width="${strokeWidth + 1}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- Right Leg -->
      <path class="sm-leg-r" d="M 0 60 L 35 140 L 45 240" stroke="${color}" stroke-width="${strokeWidth + 1}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    `;

    this.container.appendChild(g);
    this.el = g;
  }

  setPose(poseName, duration = 0.4, ease = 'power2.out') {
    const poses = {
      idle: {
        armL: 'M 0 -100 L -45 -50 L -75 -10',
        armR: 'M 0 -100 L 45 -50 L 75 -10',
        legL: 'M 0 60 L -35 140 L -45 240',
        legR: 'M 0 60 L 35 140 L 45 240',
        mouth: 'M -10 -146 Q 0 -140 10 -146'
      },
      pointing_up: {
        armL: 'M 0 -100 L -35 -40 L -60 10',
        armR: 'M 0 -100 L 50 -120 L 100 -170',
        legL: 'M 0 60 L -30 140 L -40 240',
        legR: 'M 0 60 L 40 140 L 50 240',
        mouth: 'M -12 -145 Q 0 -134 12 -145'
      },
      shocked: {
        armL: 'M 0 -100 L -50 -140 L -30 -190',
        armR: 'M 0 -100 L 50 -140 L 30 -190',
        legL: 'M 0 60 L -60 130 L -80 220',
        legR: 'M 0 60 L 60 130 L 80 220',
        mouth: 'M -8 -148 A 6 9 0 1 0 8 -148 A 6 9 0 1 0 -8 -148'
      },
      thinking: {
        armL: 'M 0 -100 L -30 -40 L 20 -40',
        armR: 'M 0 -100 L 40 -110 L 15 -145',
        legL: 'M 0 60 L -35 140 L -45 240',
        legR: 'M 0 60 L 35 140 L 45 240',
        mouth: 'M -8 -145 L 8 -147'
      }
    };

    const target = poses[poseName] || poses.idle;
    if (window.gsap) {
      const tl = gsap.timeline();
      tl.to(this.el.querySelector('.sm-arm-l'), { attr: { d: target.armL }, duration, ease }, 0);
      tl.to(this.el.querySelector('.sm-arm-r'), { attr: { d: target.armR }, duration, ease }, 0);
      tl.to(this.el.querySelector('.sm-leg-l'), { attr: { d: target.legL }, duration, ease }, 0);
      tl.to(this.el.querySelector('.sm-leg-r'), { attr: { d: target.legR }, duration, ease }, 0);
      tl.to(this.el.querySelector('.sm-mouth'), { attr: { d: target.mouth }, duration: 0.2 }, 0);
      return tl;
    }
  }
}

