from gtts import gTTS
import subprocess
import whisper
import json

text = "Every night, a thief broke into a shoe shop and stole only the left shoes. The guards laughed. We're hunting a man with one leg!"

raw_mp3 = "projects/comicron_demo/voice_raw.mp3"
voice_mp3 = "projects/comicron_demo/voice.mp3"
timings_json = "projects/comicron_demo/word_timings.json"

print("Generating gTTS audio...")
tts = gTTS(text=text, lang="en", tld="us", slow=False)
tts.save(raw_mp3)

# Speed up to exact Comicron cadence (~1.12x)
print("Adjusting tempo with ffmpeg...")
cmd = ["ffmpeg", "-y", "-i", raw_mp3, "-filter:a", "atempo=1.12", voice_mp3]
subprocess.run(cmd, check=True)

# Get duration using whisper or av
import whisper
print("Loading whisper for word timestamps...")
model = whisper.load_model("base")
result = model.transcribe(voice_mp3, word_timestamps=True)

dur = round(result["segments"][-1]["end"], 2)
print(f"Final voice duration: {dur:.2f}s")

words = []
for seg in result["segments"]:
    for w in seg.get("words", []):
        words.append({
            "word": w["word"].strip(),
            "start": round(w["start"], 2),
            "end": round(w["end"], 2)
        })

data = {
    "duration": dur,
    "text": text,
    "words": words
}

with open(timings_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Extracted {len(words)} timed words. Saved to {timings_json}")
