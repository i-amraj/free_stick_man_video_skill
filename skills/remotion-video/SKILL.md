---
name: remotion-video
description: >-
  Creates programmatic videos using React and Remotion. Use when building
  dynamic motion graphics, social media video ads, kinetic typography,
  data visualizations, or batch rendering videos with code.
---

# Remotion Video Creation Skill

Remotion allows you to write videos programmatically using React, TailwindCSS, Canvas, WebGL, and SVG animations, and render them as MP4 or WebM files.

## Project Quickstart

### 1. Initialize Remotion in a Project
```bash
npx create-video@latest ./
# Or install in an existing React / Vite project:
npm i remotion @remotion/cli
```

### 2. Previewing Video in Studio
To open the live interactive player:
```bash
npx remotion studio
```

### 3. Rendering Video from CLI
```bash
# Render to MP4
npx remotion render Root MyComp out.mp4 --props='{"title": "Automated Fact #1"}'

# Render vertical 9:16 Short/Reel
npx remotion render Root MyComp short.mp4 --width=1080 --height=1920
```

---

## Core Remotion Concepts & Rules

1. **Use `useCurrentFrame()` and `useVideoConfig()`**:
   Remotion components must be pure functions of time:
   ```tsx
   import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

   export const TitleCard = ({ title }: { title: string }) => {
     const frame = useCurrentFrame();
     const { fps } = useVideoConfig();

     // Smooth spring bounce animation
     const scale = spring({
       frame,
       fps,
       config: { damping: 12 }
     });

     // Fade-in opacity over 30 frames
     const opacity = interpolate(frame, [0, 30], [0, 1], {
       extrapolateRight: 'clamp'
     });

     return (
       <div style={{ transform: `scale(${scale})`, opacity }}>
         <h1>{title}</h1>
       </div>
     );
   };
   ```

2. **Sequential Timing with `<Sequence>`**:
   Avoid manual timestamp calculations. Group scenes with `<Sequence>`:
   ```tsx
   import { Sequence } from 'remotion';

   export const Video = () => {
     return (
       <>
         <Sequence from={0} durationInFrames={90}>
           <IntroScene />
         </Sequence>
         <Sequence from={90} durationInFrames={150}>
           <MainFactScene />
         </Sequence>
       </>
     );
   };
   ```

3. **Audio Syncing with `<Audio>`**:
   ```tsx
   import { Audio, staticFile } from 'remotion';

   <Audio src={staticFile('voiceover.mp3')} volume={(f) => interpolate(f, [0, 30], [0, 1])} />
   ```

---

## Reference Template
Check out the ready-to-use template in:
[SampleVideo.tsx](./examples/SampleVideo.tsx)
