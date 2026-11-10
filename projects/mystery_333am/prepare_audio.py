import os
import subprocess
import json
import av
from gtts import gTTS

sentences = [
    {'id': 'beat_1', 'text': 'रात के तीन बजकर तैंतीस मिनट। तुम्हारा फ़ोन बजता है।', 'pause': 0.6},
    {'id': 'beat_2', 'text': 'स्क्रीन पर नंबर चमकता है — तुम्हारा ही नंबर।', 'pause': 0.8},
    {'id': 'beat_3', 'text': 'तुम कॉल उठाते हो। दूसरी तरफ़ तुम्हारी अपनी आवाज़: दरवाज़ा मत खोलना।', 'pause': 0.7},
    {'id': 'beat_4', 'text': 'कॉल लॉग में लिखा है — आउटगोइंग। कॉल तुमने की थी... पर तुमने की ही नहीं।', 'pause': 0.8},
    {'id': 'beat_5', 'text': 'तभी दरवाज़े पर दस्तक होती है। तीन हल्की, एक ज़ोर की — बिल्कुल तुम्हारे अंदाज़ में।', 'pause': 1.0},
    {'id': 'beat_6', 'text': 'तुम दबे पाँव पीपहोल से झाँकते हो — गलियारा खाली है।', 'pause': 0.7},
    {'id': 'beat_7', 'text': 'तभी उसी नंबर से मैसेज आता है: दोबारा देखो। पीपहोल पूरी बात नहीं दिखाता।', 'pause': 0.9},
    {'id': 'beat_8', 'text': 'तुम फिर झाँकते हो। कोई नहीं। पर दरवाज़े के नीचे से पानी आ रहा है।', 'pause': 0.8},
    {'id': 'beat_9', 'text': 'गीले पैरों के निशान दरवाज़े से तुम्हारे कमरे तक आ रहे हैं — और उनका नाप बिल्कुल तुम्हारे पैरों जितना है।', 'pause': 0.9},
    {'id': 'beat_10', 'text': 'कुंडी अंदर से लगी है। तो अंदर आया कौन?', 'pause': 1.2},
    {'id': 'beat_11', 'text': 'फ़ोन फिर बजता है। वही आवाज़: अब पीछे मत मुड़ना।', 'pause': 0.9},
    {'id': 'beat_12', 'text': 'तुम जम जाते हो — क्योंकि इस बार आवाज़ फ़ोन से नहीं आई। वो ठीक तुम्हारे पीछे से आई है।', 'pause': 1.2},
    {'id': 'beat_13', 'text': 'सारे सुराग जोड़ो — अपना नंबर, दस्तक की लय, खाली गलियारा, अंदर आते निशान।', 'pause': 0.7},
    {'id': 'beat_14', 'text': 'दस्तक किसने दी — बाहर वाले ने, या पीछे खड़े उसी ने?', 'pause': 0.8},
    {'id': 'beat_15', 'text': 'जवाब कमेंट में लिखो। अगली रील में इस रहस्य का सच दिखाएँगे।', 'pause': 0.5}
]

base_dir = "projects/mystery_333am/audio"
parts_dir = os.path.join(base_dir, "parts")
os.makedirs(parts_dir, exist_ok=True)

concat_lines = []
timeline = []
current_time = 0.0

print("[*] Generating Hindi voiceover with gTTS...")
for idx, s in enumerate(sentences):
    raw_file = os.path.join(parts_dir, f"raw_{idx:02d}.mp3")
    padded_file = os.path.join(parts_dir, f"padded_{idx:02d}.mp3")
    
    if not os.path.exists(raw_file):
        tts = gTTS(s['text'], lang='hi')
        tts.save(raw_file)
    
    # Measure duration with av
    container = av.open(raw_file)
    raw_dur = float(container.duration) / av.time_base
    container.close()
    
    # Pad with silence for tension
    pause = s['pause']
    pad_cmd = [
        "ffmpeg", "-y", "-i", raw_file,
        "-af", f"apad=pad_dur={pause}",
        "-c:a", "libmp3lame", padded_file
    ]
    subprocess.run(pad_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    total_dur = raw_dur + pause
    timeline.append({
        "id": s["id"],
        "text": s["text"],
        "start": round(current_time, 2),
        "speech_end": round(current_time + raw_dur, 2),
        "total_end": round(current_time + total_dur, 2),
        "duration": round(raw_dur, 2),
        "pause": pause
    })
    
    concat_lines.append(f"file '{os.path.abspath(padded_file).replace(os.sep, '/')}'")
    current_time += total_dur
    print(f"  + Beat {idx+1}/{len(sentences)} ({raw_dur:.2f}s + {pause}s pause): {s['text'][:30]}...")

concat_txt = os.path.join(base_dir, "concat.txt")
with open(concat_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(concat_lines))

timestamps_json = os.path.join(base_dir, "timestamps.json")
with open(timestamps_json, "w", encoding="utf-8") as f:
    json.dump({"total_duration": round(current_time, 2), "beats": timeline}, f, indent=2, ensure_ascii=False)

# Concat to master voiceover
master_voice = os.path.join(base_dir, "voiceover.mp3")
concat_cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_txt,
    "-c:a", "libmp3lame", "-b:a", "192k",
    master_voice
]
subprocess.run(concat_cmd, check=True)
print(f"[SUCCESS] Master voiceover ready: {master_voice} (Duration: {current_time:.2f}s)")
