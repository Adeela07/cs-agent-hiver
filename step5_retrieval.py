import json
import pickle
from rank_bm25 import BM25Okapi

threads = []
with open("data/threads_clean.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        threads.append(json.loads(line))

corpus_texts = []
corpus_resolutions = []
for t in threads:
    customer_msg = t[0]["clean_text"]
    brand_turns = [x["clean_text"] for x in t if x["author"] != t[0]["author"]]
    resolution = brand_turns[-1] if brand_turns else ""
    corpus_texts.append(customer_msg)
    corpus_resolutions.append(resolution)

tokenized = [c.lower().split() for c in corpus_texts]
bm25 = BM25Okapi(tokenized)

with open("data/bm25_index.pkl", "wb") as f:
    pickle.dump({"bm25": bm25, "texts": corpus_texts, "resolutions": corpus_resolutions}, f)

print("Saved data/bm25_index.pkl with", len(corpus_texts), "entries")