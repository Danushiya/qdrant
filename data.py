from sklearn.datasets import fetch_20newsgroups
import json
import os


# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Load the dataset
dataset = fetch_20newsgroups(
    subset="train",
    remove=("headers", "footers", "quotes")
)

# We only need about 6000 documents
documents = []

for text, target in zip(dataset.data[:6000], dataset.target[:6000]):
    documents.append({
        "text": text.strip(),
        "category": dataset.target_names[target]
    })

# Save to JSON
with open("data/documents.json", "w", encoding="utf-8") as file:
    json.dump(documents, file, indent=2)

print(f"Saved {len(documents)} documents.")