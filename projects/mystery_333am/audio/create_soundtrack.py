"""
Soundtrack & SFX Generator — projects/mystery_333am
Creates atmospheric horror background bed, phone rings, knocks, and mixes to -14 LUFS
"""

import os
import subprocess
import numpy as np
import wave
import struct

def generate_tone(freq, duration, sample_rate=44100, volume=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(2 * np.pi * freq * t) * volume
    return tone

def create_horror_bed(output_wav, total_duration=104, sample_rate=44100):
    total_samples = int(sample_rate * total_duration)
    t = np.linspace(0, total_duration, total_samples, False)

    # 1. Dark Sub Drone (55Hz + 110Hz harmonic with slow LFO)
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.15 * t)
    sub = np.sin(2 * np.pi * 55 * t) * 0.25 * lfo
    sub += np.sin(2 * np.pi * 52 * t) * 0.15 # binaural beat for unease

    # 2. Filtered mystery noise (atmospheric wind)
    noise = np.random.uniform(-1, 1, total_samples) * 0.05
    # Smooth noise
    kernel_size = 80
    kernel = np.ones(kernel_size) / kernel_size
    smoothed_noise = np.convolve(noise, kernel, mode='same')

    mix = sub + smoothed_noise

    # 3. Phone Ringing pulses (t=1.8s - 4.5s) and (t=58s - 61s)
    for start_t in [1.8, 3.2, 58.5, 60.0]:
        idx_start = int(start_t * sample_rate)
        ring_dur = 0.8
        n_ring = int(ring_dur * sample_rate)
        if idx_start + n_ring < total_samples:
            tr = np.linspace(0, ring_dur, n_ring, False)
            ring_tone = (np.sin(2 * np.pi * 440 * tr) + np.sin(2 * np.pi * 480 * tr)) * 0.12
            # Envelope
            env = np.sin(np.pi * tr / ring_dur)
            mix[idx_start:idx_start+n_ring] += ring_tone * env

    # 4. Knocks (3 light, 1 heavy) around t=27.5s
    knock_times = [27.0, 27.6, 28.2, 29.0] # 3 light, 1 heavy
    for i, kt in enumerate(knock_times):
        k_idx = int(kt * sample_rate)
        k_dur = 0.25 if i < 3 else 0.8
        n_k = int(k_dur * sample_rate)
        if k_idx + n_k < total_samples:
            tk = np.linspace(0, k_dur, n_k, False)
            freq = 90 if i < 3 else 48
            vol = 0.4 if i < 3 else 0.85
            env = np.exp(-tk * (18 if i < 3 else 6))
            k_tone = (np.sin(2 * np.pi * freq * tk) + np.random.uniform(-0.5, 0.5, n_k) * 0.3) * env * vol
            mix[k_idx:k_idx+n_k] += k_tone

    # 5. Tension Riser (t=68s to 74s - "वो ठीक तुम्हारे पीछे से आई है")
    r_start = int(68.0 * sample_rate)
    r_dur = 6.0
    n_r = int(r_dur * sample_rate)
    if r_start + n_r < total_samples:
        tr = np.linspace(0, r_dur, n_r, False)
        # Rising frequency from 80Hz to 320Hz
        instant_freq = np.linspace(80, 320, n_r)
        phase = 2 * np.pi * np.cumsum(instant_freq) / sample_rate
        riser = np.sin(phase) * (tr / r_dur) * 0.3
        mix[r_start:r_start+n_r] += riser

    # Normalize float to 16-bit PCM
    mix = np.clip(mix, -0.95, 0.95)
    pcm = (mix * 32767).astype(np.int16)

    with wave.open(output_wav, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())

    print(f"[*] Horror soundscape bed created: {output_wav}")

if __name__ == "__main__":
    bed_wav = "projects/mystery_333am/audio/bed_sfx.wav"
    create_horror_bed(bed_wav, total_duration=104)

    # Master mix with voiceover using FFmpeg ducking + loudnorm
    voice_mp3 = "projects/mystery_333am/audio/voiceover.mp3"
    final_audio = "projects/mystery_333am/audio/final_master_audio.mp3"

    print("[*] Mixing master audio with ducking and -14 LUFS mastering...")
    cmd = [
        "ffmpeg", "-y",
        "-i", voice_mp3,
        "-i", bed_wav,
        "-filter_complex",
        "[1:a]volume=0.32[bed];"
        "[bed][0:a]sidechaincompress=threshold=0.15:ratio=3:attack=25:release=300[ducked_bed];"
        "[0:a][ducked_bed]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
        "[mixed]loudnorm=I=-14:LRA=7:tp=-1.5[out]",
        "-map", "[out]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        final_audio
    ]
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Final master audio ready: {final_audio}")

