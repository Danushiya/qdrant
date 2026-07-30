import json
import os

import numpy as np
from sentence_transformers import SentenceTransformer


os.makedirs("data", exist_ok=True)

# Load saved documents
with open("data/documents.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Extract only the text
texts = [doc["text"] for doc in documents]

print("Generating embeddings...")

vectors = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True
)

# Save vectors
np.save("data/vectors.npy", vectors)

# Save metadata separately
metadata = [
    {
        "text": doc["text"],
        "category": doc["category"]
    }
    for doc in documents
]

with open("data/metadata.json", "w", encoding="utf-8") as file:
    json.dump(metadata, file, indent=2)

print(f"Saved {len(vectors)} embeddings.")
print(f"Embedding dimension: {vectors.shape[1]}")