import pandas as pd
import numpy as np
df = pd.read_csv("data/trends_clean.csv")
print("Loaded data:", df.shape)
print("\nFirst 5 rows:")
print(df.head())


average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print("\nAverage score   :", average_score)
print("Average comments:", average_comments)
scores = np.array(df["score"])

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print("\n--- NumPy Stats ---")
print("Mean score   :", mean_score)
print("Median score :", median_score)
print("Std deviation:", std_score)

print("Max score    :", np.max(scores))
print("Min score    :", np.min(scores))

category_counts = df["category"].value_counts()
most_category = category_counts.idxmax()
most_category_count = category_counts.max()

print("\nMost stories in:", most_category,
      "(", most_category_count, "stories)")

most_commented = df.loc[df["num_comments"].idxmax()]

print("\nMost commented story:",
      most_commented["title"],
      "—", most_commented["num_comments"], "comments")

df["engagement"] = df["num_comments"] / (df["score"] + 1)
df["is_popular"] = df["score"] > average_score

df.to_csv("data/trends_analysed.csv", index=False)

print("\nSaved to data/trends_analysed.csv")