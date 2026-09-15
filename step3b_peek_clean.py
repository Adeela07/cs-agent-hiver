import json

with open("data/threads_clean.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        turns = json.loads(line)
        if len(turns) == 4:
            print(json.dumps(turns, indent=2))
            break