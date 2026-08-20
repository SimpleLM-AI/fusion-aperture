# Verification

Two scripts. Neither loads a model.

From the root of this folder:

```
python3 verification/verify_hashes.py
python3 verification/recompute_aggregates.py
```

`verify_hashes.py` reads `metadata/hashes.sha256` and checks SHA-256 of UTF-8 file bytes on disk.

`recompute_aggregates.py` parses each NVIDIA `summary.csv`, rebuilds the unweighted 13 task mean and NIAH-8, checks that every null cell is `0/10`, and compares those values to `results/ruler/context_ladder.csv`. It then checks the NIAH public summary (110 cells, 107 passes, three 1M misses) and the MRCR mean against `results/mrcr/summary.json`.

A third party who holds the item level `pred/{task}.jsonl` files can run NVIDIA `evaluate.py` and OpenAI’s MRCR grade independently. Those jsonl files are not in this clone. When a release archive is attached, `results/manifests/` will name them.

Do not add a script that starts inference. That would be a different repository, and it is not this one.
