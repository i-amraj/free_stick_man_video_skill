import os
import json
import whisper

os.makedirs('projects/channel_analysis/transcripts', exist_ok=True)

model = whisper.load_model('base')

videos = [
    ('8eeoDztahuM', 'projects/channel_analysis/videos/video_8eeoDztahuM.mp3'),
    ('V5qnOWYIL7Y', 'projects/channel_analysis/videos/video_V5qnOWYIL7Y.mp3'),
    ('N_R7ZHTDNVo', 'projects/channel_analysis/videos/video_N_R7ZHTDNVo.mp3')
]

for vid, audio_path in videos:
    out_json = f'projects/channel_analysis/transcripts/transcript_{vid}.json'
    print(f'Transcribing {vid} ({audio_path})...')
    result = model.transcribe(audio_path, verbose=False)
    
    data = {
        'video_id': vid,
        'text': result['text'].strip(),
        'segments': [
            {
                'id': seg['id'],
                'start': round(seg['start'], 2),
                'end': round(seg['end'], 2),
                'text': seg['text'].strip()
            }
            for seg in result['segments']
        ]
    }
    
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f'Done {vid}: {len(data["segments"])} segments. Total words: {len(data["text"].split())}')

