# Physical memory

The meter is Darwin `ri_phys_footprint` from `proc_pid_rusage`, the Activity Monitor class resident envelope, recorded on a Mac. We report minimum, median, and maximum over interval polls of the generation process. The samples column is the number of those polls, not the number of benchmark items. The product surface is iPhone 12 and later, A14 Bionic and later chips and devices. Transfer of this envelope to those devices is not measured here.

A 500 MB line is a product budget. It is not the measured maximum. Medians sit between 450.2 MB and 514.5 MB. Maxima go above 500 MB at 32K (543.3), 64K (522.4), 1M (766.6), and MRCR (520.7). Only the 128K sweep stays under 500 MB at peak (492.9).

At 1M the maximum is a short sawtooth, a few 10 second intervals, then back near 500 MB. The median 514.5 MB is the generate envelope. It is not a rounding of 766.6. MRCR’s 520.7 MB peak is printed as measured.

RULER 4K, 8K, and 16K polls exist in the lab record but come from an earlier mixed watcher. They are omitted here, as in Appendix B of the paper.

NIAH was not densely footprinted. Six polls on 32K to 1M are too sparse to treat as a sweep. NIAH quality remains the 110 cell ladder.

Other systems’ footprints are not inferred from cache formulae. This table is ours only.

| sweep | samples | min_mb | median_mb | max_mb |
|---|---:|---:|---:|---:|
| RULER 32K | 839 | 445.5 | 479.5 | 543.3 |
| RULER 64K | 904 | 437.0 | 482.9 | 522.4 |
| RULER 128K | 257 | 387.1 | 450.2 | 492.9 |
| RULER 1M | 827 | 399.9 | 514.5 | 766.6 |
| MRCR 512K–1M | 69 | 482.5 | 520.6 | 520.7 |
