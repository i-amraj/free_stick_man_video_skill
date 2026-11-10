import React from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

export interface FactVideoProps {
  factCategory: string;
  factText: string;
  accentColor?: string;
}

export const SampleVideo: React.FC<FactVideoProps> = ({
  factCategory = 'DID YOU KNOW?',
  factText = 'Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old!',
  accentColor = '#FFB800',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance animations
  const categoryScale = spring({
    frame,
    fps,
    config: { damping: 10, mass: 0.5 },
  });

  const cardSlide = spring({
    frame: frame - 15,
    fps,
    config: { damping: 12 },
  });

  const bgZoom = interpolate(frame, [0, 300], [1, 1.15]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0F172A',
        fontFamily: "'Inter', sans-serif",
        color: '#FFFFFF',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 60,
        overflow: 'hidden',
      }}
    >
      {/* Background ambient glow */}
      <div
        style={{
          position: 'absolute',
          width: 800,
          height: 800,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${accentColor}33 0%, transparent 70%)`,
          transform: `scale(${bgZoom})`,
        }}
      />

      {/* Top Category Badge */}
      <div
        style={{
          transform: `scale(${categoryScale})`,
          backgroundColor: accentColor,
          color: '#000000',
          padding: '12px 32px',
          borderRadius: 40,
          fontWeight: 900,
          letterSpacing: 3,
          fontSize: 28,
          marginBottom: 40,
          boxShadow: `0 10px 30px ${accentColor}66`,
        }}
      >
        {factCategory}
      </div>

      {/* Main Fact Card */}
      <div
        style={{
          transform: `translateY(${(1 - Math.max(0, cardSlide)) * 80}px)`,
          opacity: Math.max(0, cardSlide),
          maxWidth: 900,
          textAlign: 'center',
          fontSize: 44,
          lineHeight: 1.4,
          fontWeight: 700,
          background: 'rgba(255, 255, 255, 0.05)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          padding: '60px 40px',
          borderRadius: 24,
        }}
      >
        "{factText}"
      </div>
    </AbsoluteFill>
  );
};
