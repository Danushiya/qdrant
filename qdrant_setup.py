import json
import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    HnswConfigDiff,
)

# -----------------------------
# Connect to Qdrant
# -----------------------------
client = QdrantClient(url="http://localhost:6333")

# -----------------------------
# Load vectors
# -----------------------------
vectors = np.load("data/vectors.npy")

with open("data/metadata.json", "r", encoding="utf-8") as file:
    metadata = json.load(file)

# -----------------------------
# Create Point objects ONCE
# -----------------------------
points = []

for idx, vector in enumerate(vectors):
    points.append(
        PointStruct(
            id=idx,
            vector=vector.tolist(),
            payload={
                "text": metadata[idx]["text"],
                "category": metadata[idx]["category"],
            },
        )
    )

print(f"Loaded {len(points)} vectors.")

# -----------------------------
# Batch upload function
# -----------------------------
BATCH_SIZE = 500


def upload_points(collection_name):
    """Upload vectors in batches."""

    for i in range(0, len(points), BATCH_SIZE):

        batch = points[i : i + BATCH_SIZE]

        client.upsert(
            collection_name=collection_name,
            points=batch,
        )

        print(
            f"{collection_name}: Uploaded "
            f"{i + len(batch)} / {len(points)}"
        )


# -----------------------------
# Part 2
# Create collections
# -----------------------------
collections = {
    "news_cosine": Distance.COSINE,
    "news_euclidean": Distance.EUCLID,
    "news_dot": Distance.DOT,
}

for collection_name, distance in collections.items():

    print(f"\nCreating {collection_name}...")

    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vectors.shape[1],
            distance=distance,
        ),
    )

    upload_points(collection_name)

    print(f"{collection_name} created successfully.")

# -----------------------------
# Part 3
# Under-tuned HNSW collection
# -----------------------------
bad_collection = "news_hnsw_bad"

print(f"\nCreating {bad_collection}...")

if client.collection_exists(bad_collection):
    client.delete_collection(bad_collection)

client.create_collection(
    collection_name=bad_collection,
    vectors_config=VectorParams(
        size=vectors.shape[1],
        distance=Distance.COSINE,
    ),
    hnsw_config=HnswConfigDiff(
        m=4,
        ef_construct=16,
    ),
)
# m=16
# ef_cons=100
upload_points(bad_collection)

print(f"{bad_collection} created successfully.")

print("\nAll collections are ready!")