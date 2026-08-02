import json
import time

from qdrant_client import QdrantClient
from qdrant_client.models import SearchParams
import numpy as np
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

# Load vectors
vectors = np.load("data/vectors.npy")

client = QdrantClient(url="http://localhost:6333")

# Load metadata
with open("data/metadata.json", "r", encoding="utf-8") as file:
    metadata = json.load(file)

NUM_CLUSTERS = 40

print("Building IVF index...")

kmeans = KMeans(
    n_clusters=NUM_CLUSTERS,
    random_state=42,
    n_init=10,
)

cluster_ids = kmeans.fit_predict(vectors)

centroids = kmeans.cluster_centers_

clusters = {}

for vector_id, cluster_id in enumerate(cluster_ids):
    clusters.setdefault(cluster_id, []).append(vector_id)

print(f"Created {len(clusters)} clusters.")

def cosine_similarity(query_vector, candidate_vectors):
    query_norm = np.linalg.norm(query_vector)

    candidate_norms = np.linalg.norm(
        candidate_vectors,
        axis=1
    )

    return (
        candidate_vectors @ query_vector
    ) / (
        candidate_norms * query_norm
    )

def search_ivf(query_vector, nprobe=1, top_k=5):

    centroid_scores = cosine_similarity(
        query_vector,
        centroids,
    )

    nearest_clusters = np.argsort(
        centroid_scores
    )[-nprobe:]

    candidate_ids = []

    for cluster in nearest_clusters:
        candidate_ids.extend(clusters[cluster])

    candidate_vectors = vectors[candidate_ids]

    scores = cosine_similarity(
        query_vector,
        candidate_vectors,
    )

    best = np.argsort(scores)[-top_k:][::-1]

    results = []

    for index in best:

        vector_id = candidate_ids[index]

        results.append(
            {
                "id": vector_id,
                "score": float(scores[index]),
                "category": metadata[vector_id]["category"],
                "text": metadata[vector_id]["text"],
            }
        )

    return results

model = SentenceTransformer("all-MiniLM-L6-v2")

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

    query_vector = model.encode(query)

    exact = client.query_points(
        collection_name="news_cosine",
        query=query_vector.tolist(),
        limit=5,
        search_params=SearchParams(
            exact=True
        ),
    ).points

    exact_ids = [p.id for p in exact]

    print(f"Exact: {exact_ids}")

    results[query] = {}

    for nprobe in [1, 8]:

        start = time.perf_counter()

        hits = search_ivf(
            query_vector,
            nprobe=nprobe,
            top_k=5,
        )

        ivf_ids = [hit["id"] for hit in hits]

        overlap = len(
            set(ivf_ids) & set(exact_ids)
        )

        latency = time.perf_counter() - start

        results[query][f"nprobe_{nprobe}"] = {
            "latency": latency,
            "overlap": overlap,
            "ids": ivf_ids,
            "results": hits,
        }

        print(
            f"nprobe={nprobe} "
            f"overlap={overlap}/5 "
            f"latency={latency:.4f}s"
        )

with open(
    "results/ivf.json",
    "w",
    encoding="utf-8",
) as file:
    json.dump(results, file, indent=2)

print("IVF results saved.")