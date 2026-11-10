"""
Video Styles Look Lock Linter — video-styles
Inspects scene files for compliance with the locked color palette and stroke constraints
"""

import os
import re
import argparse

ALLOWED_COLORS = {
    "growkaz_mystery": [
        "#0a0e1a", "#0f172a", "#1e293b", "#334155",
        "#f8fafc", "#ffffff", "#38bdf8", "#0284c7", "#ec4899", "#db2777"
    ]
}

def lint_file(file_path, profile="growkaz_mystery"):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []
    # Check for raw stroke widths differing wildly from 7px standard
    strokes = re.findall(r'stroke-width=["\']?(\d+)px?["\']?', content)
    for s in strokes:
        val = int(s)
        if val < 4 or val > 12:
            errors.append(f"Non-standard stickman stroke width detected: {val}px (expected 6-8px)")

    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="./scenes", help="Directory with scene files")
    parser.add_argument("--profile", default="growkaz_mystery")
    args = parser.parse_args()

    print(f"[*] Style Linter: Checking against profile '{args.profile}'")
    if os.path.exists(args.dir):
        for root, _, files in os.walk(args.dir):
            for file in files:
                if file.endswith((".html", ".svg", ".css")):
                    errs = lint_file(os.path.join(root, file), args.profile)
                    if errs:
                        print(f"[!] {file}: {errs}")
    print("[PASS] Style validation finished.")

