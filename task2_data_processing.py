import pandas as pd
import glob

file_path = glob.glob("data/trends_*.json")[0]
df = pd.read_json(file_path)
print("Loaded", len(df), "stories")

df = df.drop_duplicates(subset="post_id")
print("After removing duplicates:", len(df))

df = df.dropna(subset=["post_id", "title", "score"])
print("After removing nulls:", len(df))

df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")
df = df.dropna(subset=["score", "num_comments"])
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)
df = df[df["score"] >= 5]
print("After removing low scores:", len(df))

df["title"] = df["title"].str.strip()
output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)
print("Saved", len(df), "rows to", output_file)
print("\nStories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(category, count)