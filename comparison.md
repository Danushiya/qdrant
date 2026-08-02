## Overall Comparison

| Method            | Configuration | Average Top-5 Overlap vs Exact | Average Latency (s) |
| ----------------- | ------------- | -----------------------------: | ------------------: |
| Exact Brute Force | Exact Search  |                        5.0 / 5 |           Reference |
| HNSW (Default)    | ef = 16       |                        5.0 / 5 |              0.0023 |
| HNSW (Bad Config) | ef = 16       |                        5.0 / 5 |              0.0052 |
| HNSW (Default)    | ef = 64       |                        5.0 / 5 |              0.0023 |
| HNSW (Bad Config) | ef = 64       |                        5.0 / 5 |              0.0022 |
| HNSW (Default)    | ef = 128      |                        5.0 / 5 |              0.0021 |
| HNSW (Bad Config) | ef = 128      |                        5.0 / 5 |              0.0020 |
| IVF               | nprobe = 1    |                        4.6 / 5 |              0.0003 |
| IVF               | nprobe = 8    |                        5.0 / 5 |              0.0010 |
