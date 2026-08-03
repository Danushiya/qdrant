import json
import time

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import SearchParams

client = QdrantClient(url="http://localhost:6333")

model = SentenceTransformer("all-MiniLM-L6-v2")

collections = {
    "default_hnsw": "news_cosine",
    "bad_hnsw": "news_hnsw_bad",
}

queries = []

with open("queries.md") as file:
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

    # Exact Search
    start = time.perf_counter()

    exact = client.query_points(
        collection_name="news_cosine",
        query=query_vector,
        limit=5,
        search_params=SearchParams(
            exact=True
        ),
    ).points

    exact_time = time.perf_counter() - start
    print(f"Exact latency: {exact_time:.4f}s")

    exact_ids = [p.id for p in exact]

    results[query]["exact"] = {
        "latency": exact_time,
        "ids": exact_ids,
    }

    print(f"Exact: {exact_ids}")

    # HNSW Search
    for ef in [16, 64, 128]:

        for name, collection in collections.items():

            start = time.perf_counter()

            hits = client.query_points(
                collection_name=collection,
                query=query_vector,
                limit=5,
                search_params=SearchParams(
                    hnsw_ef=ef
                ),
            ).points

            latency = time.perf_counter() - start

            ids = [p.id for p in hits]

            overlap = len(set(ids) & set(exact_ids))

            results[query][f"{name}_ef_{ef}"] = {
                "latency": latency,
                "overlap": overlap,
                "ids": ids,
            }

            print(
                f"{name} ef={ef} overlap={overlap}/5 latency={latency:.4f}s"
            )

with open(
    "results/hnsw.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(results, file, indent=2)

print("Saved results.")