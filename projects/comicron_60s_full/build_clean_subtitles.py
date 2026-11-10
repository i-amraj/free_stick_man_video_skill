import json

data = json.load(open('projects/comicron_60s_full/word_timings.json'))
words = data['words']

# Let's inspect each word index to do flawless grouping
for i, w in enumerate(words):
    if any(w['word'].endswith(p) for p in ['.', '!', '?']):
        pass

# Group words by sentences first
sentences = []
curr_sent = []
for w in words:
    curr_sent.append(w)
    if any(w['word'].endswith(p) for p in ['.', '!', '?']):
        sentences.append(curr_sent)
        curr_sent = []
if curr_sent:
    sentences.append(curr_sent)

print(f"Total sentences: {len(sentences)}")

# Now for each sentence, if it has <= 7 words, it's 1 chunk.
# If it has > 7 words, split into 2 (or 3) balanced chunks.
final_chunks = []
for s in sentences:
    if len(s) <= 7:
        final_chunks.append({
            'start': s[0]['start'],
            'end': s[-1]['end'] + 0.15,
            'words': s
        })
    elif len(s) <= 14:
        # Split in half, preferably at comma
        comma_idx = -1
        for idx in range(3, len(s) - 3):
            if s[idx]['word'].endswith(','):
                comma_idx = idx
                break
        split_at = (comma_idx + 1) if comma_idx != -1 else (len(s) // 2)
        part1 = s[:split_at]
        part2 = s[split_at:]
        final_chunks.append({'start': part1[0]['start'], 'end': part1[-1]['end'] + 0.15, 'words': part1})
        final_chunks.append({'start': part2[0]['start'], 'end': part2[-1]['end'] + 0.15, 'words': part2})
    else:
        # 3 parts
        p_len = len(s) // 3
        part1 = s[:p_len]
        part2 = s[p_len:p_len*2]
        part3 = s[p_len*2:]
        final_chunks.append({'start': part1[0]['start'], 'end': part1[-1]['end'] + 0.15, 'words': part1})
        final_chunks.append({'start': part2[0]['start'], 'end': part2[-1]['end'] + 0.15, 'words': part2})
        final_chunks.append({'start': part3[0]['start'], 'end': part3[-1]['end'] + 0.15, 'words': part3})

print(f"Final natural chunks: {len(final_chunks)}")
for idx, c in enumerate(final_chunks):
    c['text'] = " ".join(w['word'] for w in c['words'])
    print(f"[{c['start']:05.2f}s - {c['end']:05.2f}s]: {c['text']}")

with open('projects/comicron_60s_full/subtitle_chunks.json', 'w') as f:
    json.dump(final_chunks, f, indent=2)
print("Saved clean sentence-aligned chunks!")

