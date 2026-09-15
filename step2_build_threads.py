import pandas as pd
import json

BRAND = "AppleSupport"
df = pd.read_csv("data/subset_raw.csv")
df_idx = df.set_index("tweet_id")

def build_threads(df_idx):
    threads = []
    for tid, row in df_idx[df_idx.author_id == BRAND].iterrows():
        chain = [row]
        cur = row
        while pd.notna(cur.in_response_to_tweet_id) and cur.in_response_to_tweet_id in df_idx.index:
            cur = df_idx.loc[cur.in_response_to_tweet_id]
            chain.append(cur)
        chain = list(reversed(chain))
        threads.append(chain)
    return threads

threads = build_threads(df_idx)
print("Threads built:", len(threads))

with open("data/threads.jsonl", "w", encoding="utf-8") as f:
    for t in threads:
        turns = [{"author": r.author_id, "text": r.text} for r in t]
        f.write(json.dumps(turns) + "\n")

print("Saved data/threads.jsonl")