import json
import random
import csv

threads = []
with open("data/threads_clean.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        turns = json.loads(line)
        opener = turns[0]["clean_text"].strip()
        if len(opener) >= 5:  # skip near-empty openers
            threads.append(turns)

print(f"Usable threads (non-empty opener): {len(threads)}")

random.seed(42)
sample = random.sample(threads, min(300, len(threads)))

with open("eval/intent_sample.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["opening_message", "my_label"])
    for t in sample:
        opening = t[0]["clean_text"]
        writer.writerow([opening, ""])

print(f"Saved eval/intent_sample.csv with {len(sample)} rows")