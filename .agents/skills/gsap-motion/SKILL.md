---
name: gsap-motion
description: >-
  Advanced GSAP motion choreography and continuous camera movement system ("Camera Kabhi Rukta Nahi").
  Use this skill whenever animating scenes, creating continuous camera drifts, pan/zoom transitions,
  velocity-matched momentum cuts, character movement physics, or building high-retention motion graphics.
  Enforces the rule that the camera must maintain intentional, continuous visual motion throughout every frame.
---

# GSAP Motion Choreography (`gsap-motion`)
## "Camera Kabhi Rukta Nahi" (Continuous Camera & Dynamic Motion)

The core rule of viral high-retention video: **The viewer's eye must never encounter a static, dead frame.** 
Static frames break engagement. In `gsap-motion`, the viewport behaves like a live, handheld or fluidly tracked camera that continuously drifts, pushes in, orbits, or glides through the scene.

---

## 1. The 4 Laws of "Camera Kabhi Rukta Nahi"

1. **The Persistent Sub-Current (Base Drift)**:
   - Every single scene must have an underlying, low-intensity camera tween running from frame 0 to the final frame.
   - Example: A slow, continuous zoom (`scale: 1.0 -> 1.07`) paired with a slight diagonal pan (`x: 0 -> -24px, y: 0 -> -16px`).
   - Easing: `"none"` or `"sine.inOut"` for seamless, unhurried drift.

2. **Causal Acceleration (Punch-in on Key Beats)**:
   - When the narrator reveals a key phrase, mystery clue, or shocking fact, overlay a fast **punch-in punch-out nudge** on top of the base drift:
   ```javascript
   // Narrator says: "Lekin yeh sab ek jhoot tha!"
   cameraTimeline.to(".stage", {
     scale: 1.18,
     duration: 0.35,
     ease: "power3.out"
   }).to(".stage", {
     scale: 1.12, // Settles back into slightly heightened zoom
     duration: 0.6,
     ease: "power2.inOut"
   });
   ```

3. **Momentum Handoff (The Vector Rule)**:
   - If Scene A exits with camera panning to the right (`x: -120px`), Scene B MUST enter already moving to the right with matching or greater velocity.
   - Never reverse camera direction abruptly without a causal collision or hard impact SFX.

4. **Multiplane Parallax**:
   - Background layers move at **0.3x** speed.
   - Main character moves at **1.0x** speed.
   - Foreground props/overlays move at **1.4x** speed.
   - This creates an immediate sensation of real 3D depth even inside a 2D canvas.

---

## 2. Core GSAP Camera Snippets

### Continuous Viewport Camera Controller
```javascript
export function initContinuousCamera(stageSelector, duration = 5) {
  const stage = document.querySelector(stageSelector);
  const cam = gsap.timeline();

  // Primary continuous drift
  cam.to(stage, {
    scale: 1.08,
    x: -30,
    y: -20,
    duration: duration,
    ease: "sine.inOut"
  }, 0);

  // Micro handheld sway (organic human feel)
  cam.to(stage, {
    rotation: 0.6,
    duration: duration * 0.45,
    repeat: 1,
    yoyo: true,
    ease: "sine.inOut"
  }, 0);

  return cam;
}
```

### Punch-In Zoom on Sound / Action
```javascript
export function triggerPunchZoom(stageSelector, targetScale = 1.15, duration = 0.25) {
  return gsap.to(stageSelector, {
    scale: targetScale,
    duration: duration,
    ease: "power4.out",
    yoyo: true,
    repeat: 1
  });
}
```

### Smooth Velocity-Matched Scene Exit
```javascript
export function exitSceneVelocity(sceneSelector, direction = 'left', duration = 0.4) {
  const xDist = direction === 'left' ? -1200 : 1200;
  return gsap.to(sceneSelector, {
    x: xDist,
    duration: duration,
    ease: "power3.in"
  });
}
```

---

## 3. Motion Curves Reference

| Motion Type | Purpose | GSAP Ease String | Duration |
|-------------|---------|------------------|----------|
| Continuous Drift | Base camera life | `"sine.inOut"` or `"none"` | Full scene length (3–6s) |
| Punch Zoom | Beat/word emphasis | `"power3.out"` | 0.25s – 0.35s |
| Snappy Entry | Props/cards pop-in | `"back.out(1.8)"` | 0.4s – 0.6s |
| Velocity Cut Exit | Seamless scene seam | `"power3.in"` | 0.28s – 0.35s |
| Organic Float | Icons, question marks | `"sine.inOut"` (yoyo) | 1.4s – 2.0s |

