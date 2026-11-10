/**
 * GSAP Motion Engine — Continuous Camera Drift & Parallax Helper
 */

export class CameraMotionEngine {
  constructor(stageEl, layers = {}) {
    this.stage = typeof stageEl === 'string' ? document.querySelector(stageEl) : stageEl;
    this.bg = layers.bg ? document.querySelector(layers.bg) : null;
    this.mid = layers.mid ? document.querySelector(layers.mid) : null;
    this.fg = layers.fg ? document.querySelector(layers.fg) : null;
  }

  startContinuousMove(duration, options = {}) {
    const {
      zoomEnd = 1.07,
      panX = -35,
      panY = -20,
      rotation = 0.5
    } = options;

    const master = gsap.timeline();

    // Stage base drift
    master.to(this.stage, {
      scale: zoomEnd,
      x: panX,
      y: panY,
      rotation: rotation,
      duration: duration,
      ease: "sine.inOut"
    }, 0);

    // Parallax background (moves slower)
    if (this.bg) {
      master.to(this.bg, {
        x: panX * 0.4,
        y: panY * 0.4,
        duration: duration,
        ease: "sine.inOut"
      }, 0);
    }

    // Parallax foreground (moves faster)
    if (this.fg) {
      master.to(this.fg, {
        x: panX * 1.5,
        y: panY * 1.5,
        duration: duration,
        ease: "sine.inOut"
      }, 0);
    }

    return master;
  }

  pulseZoom(amount = 1.12, speed = 0.3) {
    return gsap.timeline()
      .to(this.stage, { scale: amount, duration: speed * 0.4, ease: "power3.out" })
      .to(this.stage, { scale: 1.05, duration: speed * 0.6, ease: "power2.inOut" });
  }
}

