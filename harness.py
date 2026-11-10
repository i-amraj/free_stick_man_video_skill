#!/usr/bin/env python3
"""
harness.py
Top-level entry point for the GrowKaz Video Production Harness.

Usage:
    # Run test verification
    python harness.py --test

    # Generate a video from script
    python harness.py --script "Detective Gary investigates the medieval alley. Aha! A gold coin!" --output my_video.mp4

    # Run reference demo
    python harness.py --demo
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="GrowKaz Stickman Video Production Harness")
    parser.add_argument("--test", action="store_true", help="Run harness automated test suite")
    parser.add_argument("--demo", action="store_true", help="Run standard 20s reference demo")
    parser.add_argument("--script", type=str, help="Raw script text to produce into a video")
    parser.add_argument("--output", type=str, default="output.mp4", help="Output MP4 file path")
    parser.add_argument("--fps", type=int, default=30, help="Framerate (default: 30)")
    
    args = parser.parse_args()
    
    if args.test:
        from harness.test_harness import run_tests
        success = run_tests()
        sys.exit(0 if success else 1)
        
    elif args.demo:
        print("Running pre-built 20s dialogue reference demo...")
        from harness.pipeline import run_pipeline
        demo_script = "Midnight in the narrow stone alley. Detective Gary searches the ground. Gary: Aha! The thief dropped the royal treasure! But wait, why does it smell like an old shoe?!"
        run_pipeline(demo_script, Path("projects/harness_demo_output.mp4").resolve(), fps=args.fps)
        
    elif args.script:
        from harness.pipeline import run_pipeline
        run_pipeline(args.script, Path(args.output).resolve(), fps=args.fps)
        
    else:
        parser.print_help()
        print("\nTip: Run 'python harness.py --test' to verify all pipeline components.")

if __name__ == "__main__":
    main()

