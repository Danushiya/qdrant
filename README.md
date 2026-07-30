# Qdrant Search Algorithm Comparison

## Requirements

- Python 3.10+
- Docker
- Qdrant

## Install

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Start Qdrant

```bash
docker compose up -d
```

## Build Dataset

```bash
python data.py
```

## Generate Embeddings

```bash
python embed.py
```

## Create Qdrant Collections

```bash
python qdrant_setup.py
```

## Run Comparison

```bash
python compare.py
```