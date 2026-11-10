import asyncio
import edge_tts
import json
import subprocess

SCRIPT = "Every night, a thief broke into a shoe shop and stole only the left shoes. The guards laughed. We're hunting a man with one leg!"
VOICE = "en-US-ChristopherNeural"
OUT_AUDIO = "projects/comicron_demo/voice.mp3"
OUT_TIMINGS = "projects/comicron_demo/word_timings.json"

async def gen():
    communicate = edge_tts.Communicate(SCRIPT, VOICE, rate="+8%")
    submaker = edge_tts.SubMaker()
    
    with open(OUT_AUDIO, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    # get audio duration with ffprobe
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", OUT_AUDIO]
    dur = float(subprocess.check_output(cmd).decode().strip())
    print(f"Generated {OUT_AUDIO}, duration: {dur:.2f}s")
    
    # Save word timings
    words = []
    for item in submaker.cues:
        words.append({
            "start": item.start.total_seconds(),
            "end": item.end.total_seconds(),
            "word": item.text
        })
    with open(OUT_TIMINGS, "w", encoding="utf-8") as f:
        json.dump({"duration": dur, "words": words}, f, indent=2)
    print(f"Saved {len(words)} word timings to {OUT_TIMINGS}")

if __name__ == "__main__":
    asyncio.run(gen())

