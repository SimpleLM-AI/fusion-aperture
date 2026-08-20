# Hashes

`hashes.sha256` lists SHA-256 of UTF-8 file bytes (or raw bytes for PDF and PNG).

RULER `summary.csv` files and `results/mrcr/summary.json` are the same bytes named in Appendix A of the paper.

`results/niah/ladder_summary.json` is the public extract named in Appendix A (`d1978137…81de9e`). The lab sidecar (`58aca1ec…c95299`) is listed in that appendix and is not in this folder. It contained a local filesystem path and a wall clock block. Cell counts, per length means, and the three miss depths are unchanged.

If you hold the lab sidecar, check it against the not-shipped row in Appendix A. For this folder, check the public extract against `hashes.sha256`.
