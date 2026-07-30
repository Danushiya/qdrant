import json
import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

# Connect to Qdrant
client = QdrantClient(url="http://localhost:6333")

# Load vectors
vectors = np.load("data/vectors.npy")

# Load metadata
with open("data/metadata.json", "r", encoding="utf-8") as file:
    metadata = json.load(file)

collections = {
    "news_cosine": Distance.COSINE,
    "news_euclidean": Distance.EUCLID,
    "news_dot": Distance.DOT,
}

for collection_name, distance in collections.items():

    # Delete if it already exists
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name)

    # Create collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vectors.shape[1],
            distance=distance,
        ),
    )

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

    client.upsert(
        collection_name=collection_name,
        points=points,
    )

    print(f"{collection_name} created with {len(points)} vectors.")

print("Finished!")