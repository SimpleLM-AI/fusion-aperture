Score files in this folder are the checkable objects.

RULER `summary.csv` files are the unmodified output of NVIDIA `evaluate.py`. Their SHA-256 values match Appendix A of the paper.

`context_ladder.csv` and `per_task_128k_1m.csv` are derived from those summaries. If they disagree with the summaries, the summaries win.

NIAH `ladder_summary.json` is a public extract of the 110 cell result. It omits lab sidecar fields (local paths, wall clock). Appendix A hashes both that public extract and the lab sidecar (not shipped). The cell counts and miss depths are the same.

MRCR `summary.json` is byte identical to the paper appendix.

`manifests/` records what a future prediction jsonl release would contain. Those jsonl files are not in this clone.
