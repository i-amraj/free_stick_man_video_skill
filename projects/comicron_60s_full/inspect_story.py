import json
import os

with open('projects/channel_analysis/transcripts/transcript_8eeoDztahuM.json', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total duration: {d['segments'][-1]['end']}s")
print(f"Total segments: {len(d['segments'])}")
print("-" * 60)
for idx, s in enumerate(d['segments']):
    print(f"Beat {idx+1:02d} [{s['start']:5.1f}s -> {s['end']:5.1f}s]: {s['text']}")

