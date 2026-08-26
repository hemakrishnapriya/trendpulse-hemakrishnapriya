import requests
import time
import json
import os
from datetime import datetime
headers = {"User-Agent": "TrendPulse/1.0"}
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Failed to fetch story IDs")
    exit()
story_ids = response.json()[:500]
print("Fetched", len(story_ids), "story IDs")


categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}
stories_by_category = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}
stories_by_category = {
    "technology": [],
    "worldnews": [],
    "sports": [],
    "science": [],
    "entertainment": []
}

all_fetched_stories = []
for story_id in story_ids:
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        print("Fetching story:", story_id, flush=True)
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            print("Failed to fetch story:", story_id)
            continue
        story = response.json()
        if story and story.get("type") == "story":
            all_fetched_stories.append(story)
    except requests.RequestException as error:
        print("Request failed:", story_id, error)
        continue
for category, keywords in categories.items():
    for story in all_fetched_stories:
        if len(stories_by_category[category]) >= 20:
            break
        title = story.get("title", "").lower()
        if any(keyword.lower() in title for keyword in keywords):
            already_added = any(
                story["id"] == existing["id"]
                for stories in stories_by_category.values()
                for existing in stories
            )
            if not already_added:
                stories_by_category[category].append(story)
for category in stories_by_category:
    if len(stories_by_category[category]) < 20:
        for story in all_fetched_stories:
            if len(stories_by_category[category]) >= 20:
                break
            already_added = any(
                story["id"] == existing["id"]
                for stories in stories_by_category.values()
                for existing in stories
            )
            if not already_added:
                stories_by_category[category].append(story)
for category, stories in stories_by_category.items():
    print(category, ":", len(stories))

all_stories = []
for category, stories in stories_by_category.items():
    for story in stories:
        cleaned_story = {
            "post_id": story.get("id"),
            "title": story.get("title", ""),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", ""),
            "collected_at": datetime.now().isoformat()
        }
        all_stories.append(cleaned_story)
print("Total stories:", len(all_stories))    



os.makedirs("data", exist_ok=True)
date_string = datetime.now().strftime("%Y%m%d")
file_path = f"data/trends_{date_string}.json"
with open(file_path, "w", encoding="utf-8") as file:
    json.dump(all_stories, file, indent=4, ensure_ascii=False)
print(f"Collected {len(all_stories)} stories. Saved to {file_path}")

