import json

total = 0
empty_openers = 0

with open("data/threads_clean.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        turns = json.loads(line)
        total += 1
        opener = turns[0]["clean_text"].strip()
        if len(opener) < 5:  # essentially empty or near-empty
            empty_openers += 1

print(f"Total threads: {total}")
print(f"Threads with near-empty opener (<5 chars after cleaning): {empty_openers}")
print(f"Percentage: {100 * empty_openers / total:.1f}%")