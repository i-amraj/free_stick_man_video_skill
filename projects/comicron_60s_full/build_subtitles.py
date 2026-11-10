import json

data = json.load(open('projects/comicron_60s_full/word_timings.json'))
words = data['words']

# Refined natural chunking aligned with story beats
# Let's inspect the 23 beats from inspect_story.py
# In Comicron, each subtitle block typically contains 3-7 words, perfectly readable at the bottom.
refined_chunks = [
    # Beat 1 (0.0 -> 5.2s)
    {"start": 0.0, "end": 2.2, "words": words[0:5]},       # Every night for a month,
    {"start": 1.48, "end": 3.1, "words": words[5:12]},     # a thief broke into a shoe shop
    {"start": 3.1, "end": 5.1, "words": words[12:18]},     # and stole only the left shoes.
    
    # Beat 2 & 3 (5.2 -> 8.2s)
    {"start": 5.26, "end": 6.2, "words": words[18:21]},    # The guards laughed.
    {"start": 6.38, "end": 8.1, "words": words[21:28]},    # We're hunting a man with one leg.
    
    # Beat 4 & 5 (8.2 -> 15.3s)
    {"start": 8.24, "end": 10.0, "words": words[28:34]},   # Old Corvin counted what was left.
    {"start": 10.34, "end": 13.4, "words": words[34:43]},  # 300 right shoes, but nobody buys half a pair,
    {"start": 13.54, "end": 15.2, "words": words[43:51]},  # so he hung a sign in the window.
    
    # Beat 6 & 7 (15.3 -> 18.0s)
    {"start": 15.42, "end": 16.9, "words": words[51:56]},  # One right shoe, half price.
    {"start": 17.16, "end": 17.9, "words": words[56:58]},  # Nobody came.
    
    # Beat 8 & 9 (18.0 -> 21.9s)
    {"start": 18.08, "end": 20.5, "words": words[58:67]},  # Then, 10 guards hid in the shop all night.
    {"start": 20.66, "end": 21.9, "words": words[67:72]},  # The thief never showed up.
    
    # Beat 10 (21.9 -> 24.5s)
    {"start": 22.0, "end": 24.5, "words": words[72:79]},   # The next night, every left boot vanished too.
    
    # Beat 11 & 12 (24.5 -> 29.0s)
    {"start": 24.6, "end": 26.5, "words": words[79:87]},   # Soon, the town called it the hopping shop.
    {"start": 26.68, "end": 28.9, "words": words[87:95]},  # Children hopped past the window on one foot.
    
    # Beat 13 & 14 (29.0 -> 33.2s)
    {"start": 28.72, "end": 30.7, "words": words[95:100]},  # By winter, Corvin was broke.
    {"start": 30.84, "end": 33.1, "words": words[100:108]},# His shelves full of shoes nobody could wear.
    
    # Beat 15, 16, 17 (33.2 -> 41.7s)
    {"start": 33.26, "end": 35.8, "words": words[108:115]},# However, one morning, a quiet stranger walked in
    {"start": 35.8, "end": 38.1, "words": words[115:123]}, # and offered five coins for the lot.
    {"start": 38.26, "end": 39.5, "words": words[123:127]},# For firewood, he said.
    {"start": 39.7, "end": 41.5, "words": words[127:133]}, # Corvin took it and nearly cried.
    
    # Beat 18 & 19 (41.7 -> 50.2s)
    {"start": 41.66, "end": 44.4, "words": words[133:143]},# A week later, a new shoe shop opened in the next town.
    {"start": 44.54, "end": 47.6, "words": words[143:151]},# Its shelves held 300 pairs at full price,
    {"start": 47.8, "end": 50.1, "words": words[151:159]}, # and behind the counter stood the quiet stranger.
    
    # Beat 20 & 21 (50.2 -> 58.0s)
    {"start": 50.24, "end": 52.1, "words": words[159:165]},# You see, one shoe is worthless,
    {"start": 52.3, "end": 53.8, "words": words[165:173]}, # to a thief and to a shop.
    {"start": 53.92, "end": 56.1, "words": words[173:180]},# So he stole the half nobody could sell
    {"start": 56.1, "end": 57.8, "words": words[180:187]}, # and let Corvin sell him the rest.
    
    # Beat 22 (58.0 -> 61.3s)
    {"start": 57.66, "end": 61.1, "words": words[187:196]},# He paid five coins for 300 pairs of shoes.
    
    # Beat 23 (61.3 -> 65.5s)
    {"start": 61.24, "end": 63.4, "words": words[196:205]},# He became the richest shoe maker in the valley
    {"start": 63.4, "end": 65.4, "words": words[205:214]}  # and never made a single shoe.
]

# Check word count sanity
total_words = sum(len(c['words']) for c in refined_chunks)
print(f"Total words partitioned: {total_words} / {len(words)}")

for idx, c in enumerate(refined_chunks):
    txt = " ".join(w['word'] for w in c['words'])
    c['text'] = txt
    print(f"Line {idx+1:02d} [{c['start']:05.2f}s - {c['end']:05.2f}s]: {txt}")

with open('projects/comicron_60s_full/subtitle_chunks.json', 'w') as f:
    json.dump(refined_chunks, f, indent=2)
print("Saved perfect natural chunks to subtitle_chunks.json!")
