# OpenAI MRCR v1 protocol

Dataset: https://huggingface.co/datasets/openai/mrcr

This pack is two needle items in the (512K, 1M] bin, 91 conversations. The skill is multi round coreference, not needle retrieval.

Official grade, as OpenAI published it: if the completion does not start with `random_string_to_prepend`, the score is 0. Otherwise those prefixes are stripped and `difflib.SequenceMatcher.ratio` is the score.

The stored mean is 0.32562461707672186, reported in the paper as 0.326. `results/mrcr/summary.json` is the file whose SHA-256 is in the paper appendix.

MiniCPM-SALA’s 28.62 figure is 128K two needle. It is not this bin. GPT-4.1 numbers on the OpenAI post are the neighbourhood for this board, with the usual unmatched host and n caveats.
