# RULER protocol

We used the public NVIDIA suite as published by Hsieh et al., arXiv:2404.06654, client at https://github.com/NVIDIA/RULER.

The pipeline is theirs. `prepare.py` writes tokenized synthetic items. Completions are stored as `pred/{task}.jsonl` with `input`, `pred`, and gold `outputs`. `evaluate.py` writes `summary.csv`. We do not substitute a private judge.

The thirteen synthetic v1 tasks are `niah_single_1`, `niah_single_2`, `niah_single_3`, `niah_multikey_1`, `niah_multikey_2`, `niah_multikey_3`, `niah_multivalue`, `niah_multiquery`, `vt`, `cwe`, `fwe`, `qa_1`, `qa_2`.

The headline score is the unweighted mean of those thirteen. NIAH-8 is the mean of the eight retrieval tasks (the `niah_*` names). Those two numbers answer different questions. At 1M they part company.

Lengths in this pack: 4,096; 8,192; 16,384; 32,768; 65,536; 131,072; 1,048,576. NVIDIA’s public table stops at 128K. The 1M cell is a separate board. Do not average them into a single “RULER score.”

Sample count is 10 per task per length. The original paper typically uses 500. Qwen’s 1M card uses 20. Greedy decode makes each of our items stable. It does not buy the statistical power of 500. Expanding n later is a new measurement on the same host, not a silent edit of these files.

Decode matches NVIDIA’s published defaults: temperature 0, `top_p` 1.0, `top_k` 32. The chat wrapper is template `base`. See `protocols/decoding.yaml`.

Null answers were 0/10 on every task at every length in this pack.

A later run at 32K, 64K, and 1M reproduced the same thirteen task rows and was used only to attach a trustworthy memory meter. Those reruns are not new quality claims.
