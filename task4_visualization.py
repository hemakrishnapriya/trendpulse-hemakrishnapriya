import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/trends_analysed.csv")

os.makedirs("outputs", exist_ok=True)

top_stories = df.nlargest(10, "score").copy()
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..." if len(title) > 50 else title
)

plt.figure(figsize=(10, 6))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig("outputs/chart1_top_stories.png")
plt.show()
plt.close()

category_counts = df["category"].value_counts()

plt.figure(figsize=(9, 6))

plt.bar(
    category_counts.index,
    category_counts.values,
    color=["red", "blue", "green", "orange", "purple"]
)

plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.tight_layout()

plt.savefig("outputs/chart2_categories.png")
plt.show()
plt.close()

plt.figure(figsize=(10, 6))

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Non-Popular",
    alpha=0.7
)

plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()

plt.savefig("outputs/chart3_scatter.png")
plt.show()
plt.close()


fig, axes = plt.subplots(2, 2, figsize=(16, 10))

axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")
axes[0, 0].invert_yaxis()

axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=["red", "blue", "green", "orange", "purple"]
)
axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")

axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Non-Popular",
    alpha=0.7
)

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")
axes[1, 0].legend()
axes[1, 1].axis("off")

fig.suptitle("TrendPulse Dashboard", fontsize=18)

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.show()
plt.close()

print("All charts saved successfully in outputs/")