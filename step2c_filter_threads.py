import json

kept = []
dropped = 0

with open("data/threads.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        turns = json.loads(line)
        if len(turns) >= 2:
            kept.append(turns)
        else:
            dropped += 1

with open("data/threads_multiturn.jsonl", "w", encoding="utf-8") as f:
    for turns in kept:
        f.write(json.dumps(turns) + "\n")

print(f"Kept {len(kept)} multi-turn threads")
print(f"Dropped {dropped} single-turn threads")
print("Saved data/threads_multiturn.jsonl")