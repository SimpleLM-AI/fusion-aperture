# Fusion Aperture long context evaluation pack

Fusion Aperture · 19 August 2026

This folder documents a locked evaluation of Fusion Aperture. The stack itself is not in this folder.

You can check that the published tables match the hashed score files and that the headline averages recompute from those files. You cannot rebuild generation from what is here, and nothing here is an implementation of the stack.

The measurement paper lives in `paper/`. Everything else exists so a careful reader can audit that paper without being handed the engine.

## What you can check

The RULER `summary.csv` files and the MRCR summary are byte identical to the artifacts named in Appendix A of the paper. SHA-256 of those files is in `metadata/hashes.sha256`.

`verification/verify_hashes.py` confirms the files on disk still match that list.

`verification/recompute_aggregates.py` reads the NVIDIA summaries, rebuilds the unweighted 13 task mean and the eight task retrieval mean, and checks the NIAH and MRCR headlines. If a table in the paper disagrees with those recomputations, the paper is wrong.

Stock scorers are NVIDIA `evaluate.py` for RULER and OpenAI’s published MRCR grade (hash prefix, then `difflib.SequenceMatcher.ratio`). This pack does not reimplement those graders. It checks that our stored outputs of those graders are internally consistent.

## What you cannot do here

There is no binary, no container, no server, and no recipe that would let you regenerate a million token completion. Prediction jsonl files (prompt, completion, gold) are the item level audit trail for RULER. They are large. They are not in this clone. When we publish a release archive they will be listed in `results/manifests/` with hashes. Until that archive exists, the checkable objects are the summaries, the paper, and the derived tables.

Physical memory is reported as Darwin `ri_phys_footprint` of the generation process on a Mac. The product surface is iPhone 12 and later, A14 Bionic and later chips and devices. Those two sentences are not the same measurement.

## The operating point, in one paragraph

A frozen Qwen3.5-2B checkpoint, quantized to Q4_K_M, with no extra long context training, is evaluated greedy on stock public harnesses. RULER scores 80.3 at 128K and 72.0 at 1M. The retrieval slice of RULER (NIAH-8) is 94.7 at 1M. A 110 cell needle ladder is 97.27% overall and perfect from 1K through 512K. OpenAI MRCR, two needle, 512K to 1M, is 0.326 on 91 items. Physical footprint medians sit between 450 MB and 515 MB. The 128K peak is 492.9 MB. Several sweeps, including 1M at 766.6 MB, go above 500 MB at maximum. Fusion Aperture achieves state-of-the-art quality–memory efficiency among training-free long-context inference systems at the 2B Q4, mobile, half-gigabyte-class operating point. That sentence is scoped. It is not a claim of the highest RULER mean among trained 30B to 235B models.

## How the folders are meant to be read

`paper/` is the manuscript. Read it first.

`protocols/` says which public harness we ran and which decode defaults we locked. Those defaults are NVIDIA’s published RULER defaults, not a private recipe.

`results/` holds the score files. RULER lengths are named by token count. NIAH is a public summary of 110 cells, not a copy of a lab sidecar. MRCR is the two needle bin we actually ran.

`measurements/memory.md` is our footprint table. Sample counts there are operating system polls, not benchmark items. NIAH was not densely sampled and is omitted from that table on purpose.

`comparisons/` repeats published scores with URLs, lengths, and sample counts. `comparison_policy.md` is the rule for that folder. Other systems’ memory is not estimated.

`limitations/` names the miss cells and the tasks that pull the 1M mean down. It does not explain the engine.

`metadata/` is host, device, and hashes.

`verification/` is the only code. It audits files. It does not run a model.

## Citation

Please cite the paper, not this folder by itself. See `CITATION.cff`.

Hsieh et al., RULER, arXiv:2404.06654, and the NVIDIA RULER repository are the protocol for the 13 task suite. OpenAI’s GPT-4.1 post and the `openai/mrcr` dataset are the protocol for MRCR. Needle practice follows the Kamradt style grid described in the paper, which is not Gemini’s internal needle test.

## License

Copyright 2026 Fusion Aperture. All rights reserved except as granted in `LICENSE`.

This folder does not contain Fusion Aperture. The stack, binaries, kernels, and unpublished methods are not licensed here. No patent, trademark, or reverse-engineering right is granted for them.

The Evaluation Materials in this folder (manuscript, tables, figures, manifests, hashes, protocol notes, and verification scripts) are licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International. SPDX identifier: `CC-BY-NC-ND-4.0`. Cover terms are in `LICENSE`. The canonical legal code is `LICENSES/CC-BY-NC-ND-4.0.txt`.

You may share this archive verbatim for non-commercial purposes, with the attribution that license requires. You may not share a modified pack. You may not use the Evaluation Materials primarily for commercial advantage. “Fusion Aperture” may be used for accurate citation only.

Qwen3.5-2B, NVIDIA RULER, and openai/mrcr remain with their owners. This file does not relicense those works.

If you cite the numbers, cite the paper named in `CITATION.cff`.

## Status

Private evaluation archive. 19 August 2026.
