"""
pipeline.py
The Complete End-to-End GrowKaz Production Pipeline.

Usage:
    python -m harness.pipeline --script "..." --output "output.mp4"
"""

import os
import argparse
from pathlib import Path
from .step1_script_breakdown import breakdown_script
from .step2_audio_engine import generate_audio_tracks
from .step4_motion_engine import build_scene_html
from .step5_virtual_renderer import render_scene_to_video
from .step6_qc_verifier import verify_video_quality

def run_pipeline(
    script_text: str,
    output_path: Path,
    theme: str = "medieval_alley",
    fps: int = 30
) -> Path:
    root_dir = Path(__file__).resolve().parent.parent
    work_dir = output_path.parent / "_harness_build"
    work_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n==================================================")
    print("🎬 GROWKAZ STICKMAN VIDEO PRODUCTION PIPELINE")
    print("==================================================")
    
    # Step 1: Script Breakdown
    print("\n[Step 1/6] Breaking down script into narrative beats...")
    beats = breakdown_script(script_text)
    print(f"  Generated {len(beats)} beats (estimated pacing: 2.2s - 2.8s per beat)")
    for b in beats:
        print(f"    - {b['id']} ({b['duration']}s): [{b['speaker'].upper()}] {b['dialogue'][:45]}... (Action: {b['action']})")
        
    # Step 2: Audio Engineering
    print("\n[Step 2/6] Synthesizing character voices and aligning word timestamps...")
    audio_info = generate_audio_tracks(beats, work_dir)
    total_duration = audio_info["total_duration"]
    print(f"  Master audio generated: {total_duration:.2f}s ({len(audio_info['word_timings'])} aligned words)")
    
    # Step 3 & 4: Staging & Motion Choreography
    print("\n[Step 3 & 4/6] Procedural staging & GSAP 'Camera Kabhi Rukta Nahi' choreography...")
    rig_js = root_dir / ".agents" / "skills" / "character-animation" / "assets" / "rig.js"
    props_js = root_dir / ".agents" / "skills" / "character-animation" / "assets" / "props.js"
    gsap_js = root_dir / "projects" / "comicron_60s_full" / "gsap.min.js"
    scene_html = work_dir / "scene.html"
    
    characters = [
        {
            "id": "gary",
            "head_shape": "square",
            "beard": "mustache",
            "jacket": "trench",
            "skin": "#E0AC69",
            "shirt": "#D32F2F",
            "pants": "#1E293B",
            "hat": "cap",
            "scale": 2.2,
            "x": 540,
            "y": 1460
        }
    ]
    
    build_scene_html(
        beats=beats,
        word_timings=audio_info["word_timings"],
        characters=characters,
        total_duration=total_duration,
        rig_js_path=str(rig_js),
        props_js_path=str(props_js),
        gsap_js_path=str(gsap_js),
        output_html_path=scene_html
    )
    print(f"  Stage assembled: {scene_html}")
    
    # Step 5: Virtual Clock Headless Capture
    print("\n[Step 5/6] Deterministic virtual clock rendering via Playwright & FFmpeg...")
    render_scene_to_video(
        html_path=scene_html,
        audio_path=Path(audio_info["master_audio_path"]),
        output_mp4=output_path,
        duration=total_duration,
        fps=fps
    )
    
    # Step 6: Automated QC Verification
    print("\n[Step 6/6] Executing 5-Gate automated Quality Control inspection...")
    qc = verify_video_quality(output_path, expected_duration=total_duration)
    for gate, status in qc["gates"].items():
        print(f"  [{gate}] {status}")
        
    if qc["passed"]:
        print(f"\n✅ PIPELINE COMPLETED WITH 100% SUCCESS: {output_path}")
    else:
        print(f"\n⚠️ PIPELINE FINISHED WITH WARNINGS: {qc['errors']}")
        
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GrowKaz Video Production Harness")
    parser.add_argument("--script", type=str, required=True, help="Story script text")
    parser.add_argument("--output", type=str, default="output_video.mp4", help="Path to output MP4 file")
    parser.add_argument("--fps", type=int, default=30, help="Framerate (default 30)")
    args = parser.parse_args()
    
    run_pipeline(
        script_text=args.script,
        output_path=Path(args.output).resolve(),
        fps=args.fps
    )

