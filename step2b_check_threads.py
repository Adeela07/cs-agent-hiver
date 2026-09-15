import json

lengths = []
with open("data/threads.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        turns = json.loads(line)
        lengths.append(len(turns))

from collections import Counter
counts = Counter(lengths)
print("Thread length distribution:")
for length in sorted(counts):
    print(f"  {length} turns: {counts[length]} threads")

multi_turn = sum(c for l, c in counts.items() if l >= 2)
print(f"\nTotal threads: {len(lengths)}")
print(f"Multi-turn (real conversations): {multi_turn}")
print(f"Single-turn (likely broadcasts/orphans): {len(lengths) - multi_turn}")