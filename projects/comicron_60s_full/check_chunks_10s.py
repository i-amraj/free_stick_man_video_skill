import json
chunks = json.load(open("projects/comicron_60s_full/subtitle_chunks.json", encoding="utf-8"))
sub10 = [c for c in chunks if c["start"] < 10.0]
print(f"Total chunks in 10s: {len(sub10)}")
for c in sub10:
    print(f"{c['start']}s -> {c['end']}s: {c['text']}")

