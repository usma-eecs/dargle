import pandas as pd
from urllib.parse import urlparse

df = pd.read_csv("complete_dump.csv")

# to see every url an onion was seen on
df[df["onion"] == "wlchatc3pjwpli5r.onion"]

# add a domain column
df["domain"] = df["url"].apply(lambda d: urlparse(d).netloc)

# create a dataframe of unique domain/onion pairs
pairs = df.drop('url', 1).groupby(["domain","onion"]).size()

# unique onions on each domain
domain_counts = pairs.groupby('domain').count().sort_values(ascending=False)

# unique domains for each onion
onion_counts = pairs.groupby('onion').count().sort_values(ascending=False)  

# write the results
domain_counts.reset_index().rename(columns={0:"unique_onions"}).to_csv("domain_counts.csv")
onion_counts.reset_index().rename(columns={0:"unique_domains"}).to_csv("onion_counts.csv")