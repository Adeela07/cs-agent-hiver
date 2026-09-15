import pandas as pd

BRAND = "AppleSupport"  # change this to your brand's exact author_id
df = pd.read_csv("data/twcs.csv")

brand_replies = df[df.author_id == BRAND]
print("Brand replies found:", len(brand_replies))

inbound_ids = brand_replies.in_response_to_tweet_id.dropna().unique()
inbound = df[df.tweet_id.isin(inbound_ids)]

subset = pd.concat([inbound, brand_replies]).drop_duplicates()
subset.to_csv("data/subset_raw.csv", index=False)
print("Saved data/subset_raw.csv with", len(subset), "rows")