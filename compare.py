import json
import time

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

model = SentenceTransformer("all-MiniLM-L6-v2")

collections = [
    "news_cosine",
    "news_euclidean",
    "news_dot",
]

# Read queries
queries = []

with open("queries.md", "r") as file:
    for line in file:
        line = line.strip()

        if line.startswith(("1.", "2.", "3.", "4.", "5.")):
            queries.append(line[2:].strip())

results = {}

for query in queries:

    print("=" * 50)
    print(query)

    query_vector = model.encode(query).tolist()

    results[query] = {}

    for collection in collections:

        start = time.perf_counter()

        hits = client.query_points(
            collection_name=collection,
            query=query_vector,
            limit=5,
        ).points

        elapsed = time.perf_counter() - start

        results[query][collection] = []

        print(f"\n{collection}")

        for hit in hits:

            results[query][collection].append(
                {
                    "id": hit.id,
                    "score": hit.score,
                    "category": hit.payload["category"],
                    "text": hit.payload["text"][:120],
                }
            )

            print(
                f"{hit.score:.4f}",
                hit.payload["category"],
            )

        print(f"Latency: {elapsed:.4f} sec")

with open(
    "results/distance_metrics.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(results, file, indent=2)

print("\nResults saved.")