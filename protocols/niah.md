# Needle ladder protocol

This is a Kamradt style grid: ten context lengths and eleven depths, 110 cells, Paul Graham essay haystack. A cell is pass or fail.

Lengths: 1K, 4K, 8K, 16K, 32K, 64K, 128K, 256K, 512K, 1M.

The headline 97.27% is 107 passes out of 110. From 1K through 512K every cell passed (99 of 99). At 1M eight of eleven passed. The three misses are listed in `results/niah/misses_1m.csv` and in `limitations/error_examples.md`.

This grid is not Gemini’s internal needle test. Gemini’s published single needle figure at 1M is a different protocol and does not belong on the same axis. It is also not RULER’s NIAH-8, which is eight synthetic retrieval tasks inside NVIDIA’s suite.

Physical memory was not densely recorded on this ladder. Six interval polls exist in the lab record. That is too few to publish as a sweep, so NIAH does not appear in `measurements/memory.md`.
