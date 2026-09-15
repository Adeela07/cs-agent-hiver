import json
import re
import html

def clean(text):
    text = html.unescape(text)          # &gt; -> >, &amp; -> &, etc.
    text = re.sub(r"@\w+", "", text)     # remove @mentions
    text = re.sub(r"http\S+", "", text)  # remove links
    text = text.encode("ascii", "ignore").decode("ascii")  # strip emoji/unicode junk like \ufe0f
    text = re.sub(r"\s+", " ", text)     # collapse extra whitespace left behind
    return text.strip()

cleaned_count = 0
with open("data/threads_multiturn.jsonl", "r", encoding="utf-8") as fin, \
     open("data/threads_clean.jsonl", "w", encoding="utf-8") as fout:
    for line in fin:
        turns = json.loads(line)
        for t in turns:
            t["clean_text"] = clean(t["text"])
        fout.write(json.dumps(turns) + "\n")
        cleaned_count += 1

print(f"Cleaned and saved {cleaned_count} threads to data/threads_clean.jsonl")