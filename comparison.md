# Comparison

## Distance Metrics

After running all five queries, compare the ranking order of the results returned by:

- Cosine Similarity
- Euclidean Distance
- Dot Product

Record at least one query where the ranking changes and explain why

# HNSW Comparison

| Method | ef | Average Overlap | Average Latency |
|----------|----|----------------|-----------------|
| Exact | - | 5/5 | Baseline |
| Default HNSW | 16 | To be filled | To be filled |
| Default HNSW | 64 | To be filled | To be filled |
| Default HNSW | 128 | To be filled | To be filled |
| Bad HNSW | 16 | To be filled | To be filled |
| Bad HNSW | 64 | To be filled | To be filled |
| Bad HNSW | 128 | To be filled | To be filled |

Loading weights: 100%|███████████| 103/103 [00:00<00:00, 20678.41it/s]
==================================================
How do I install a graphics card driver?
Exact: [1285, 4532, 1456, 515, 678]
default_hnsw ef=16 overlap=5/5 latency=0.0029s
bad_hnsw ef=16 overlap=5/5 latency=0.0032s
default_hnsw ef=64 overlap=5/5 latency=0.0028s
bad_hnsw ef=64 overlap=5/5 latency=0.0028s
default_hnsw ef=128 overlap=5/5 latency=0.0029s
bad_hnsw ef=128 overlap=5/5 latency=0.0029s
==================================================
My computer keeps crashing after installing Windows.
Exact: [3448, 2089, 726, 93, 5972]
default_hnsw ef=16 overlap=5/5 latency=0.0032s
bad_hnsw ef=16 overlap=5/5 latency=0.0032s
default_hnsw ef=64 overlap=5/5 latency=0.0030s
bad_hnsw ef=64 overlap=5/5 latency=0.0028s
default_hnsw ef=128 overlap=5/5 latency=0.0029s
bad_hnsw ef=128 overlap=5/5 latency=0.0032s
==================================================
What are the latest space shuttle missions?
Exact: [153, 3665, 5880, 4312, 1665]
default_hnsw ef=16 overlap=5/5 latency=0.0034s
bad_hnsw ef=16 overlap=5/5 latency=0.0030s
default_hnsw ef=64 overlap=5/5 latency=0.0024s
bad_hnsw ef=64 overlap=5/5 latency=0.0024s
default_hnsw ef=128 overlap=5/5 latency=0.0025s
bad_hnsw ef=128 overlap=5/5 latency=0.0027s
==================================================
How can I improve my baseball batting skills?
Exact: [1589, 1485, 4115, 4214, 5100]
default_hnsw ef=16 overlap=5/5 latency=0.0025s
bad_hnsw ef=16 overlap=5/5 latency=0.0026s
default_hnsw ef=64 overlap=5/5 latency=0.0024s
bad_hnsw ef=64 overlap=5/5 latency=0.0023s
default_hnsw ef=128 overlap=5/5 latency=0.0024s
bad_hnsw ef=128 overlap=5/5 latency=0.0023s
==================================================
What is the best way to maintain a motorcycle?
Exact: [3201, 5377, 5673, 2216, 3934]
default_hnsw ef=16 overlap=5/5 latency=0.0027s
bad_hnsw ef=16 overlap=5/5 latency=0.0024s
default_hnsw ef=64 overlap=5/5 latency=0.0022s
bad_hnsw ef=64 overlap=5/5 latency=0.0021s
default_hnsw ef=128 overlap=5/5 latency=0.0024s
bad_hnsw ef=128 overlap=5/5 latency=0.0024s
Saved results.

# IVF Comparison

| nprobe | Average Latency | Notes |
|---------|-----------------|-------|
| 1 | To be filled | Fastest, searches one cluster |
| 8 | To be filled | More accurate, searches more clusters |

Building IVF index...
Created 40 clusters.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|████████████| 103/103 [00:00<00:00, 8356.97it/s]
==================================================
How do I install a graphics card driver?
nprobe=1 latency=0.0006s
nprobe=8 latency=0.0007s
==================================================
My computer keeps crashing after installing Windows.
nprobe=1 latency=0.0002s
nprobe=8 latency=0.0006s
==================================================
What are the latest space shuttle missions?
nprobe=1 latency=0.0002s
nprobe=8 latency=0.0008s
==================================================
How can I improve my baseball batting skills?
nprobe=1 latency=0.0002s
nprobe=8 latency=0.0007s
==================================================
What is the best way to maintain a motorcycle?
nprobe=1 latency=0.0003s
nprobe=8 latency=0.0009s
IVF results saved.