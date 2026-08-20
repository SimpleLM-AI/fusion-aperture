# Error examples

These are failures as logged. They are not a diagnosis of the stack.

## RULER at 1M

The unweighted mean is 72.0. NIAH-8 is 94.7. The mean is pulled by aggregation and QA, not by needle retrieval.

| task | 128K | 1M |
|---|---:|---:|
| vt | 20 | 8 |
| cwe | 39 | 1 |
| qa_1 | 60 | 40 |
| qa_2 | 60 | 30 |
| fwe | 100 | 100 |

Frequent word extraction stays at 100. A causal account of CWE at 1M is outside this pack.

## Needle ladder at 1M

Three cells failed, all at 1,048,576 tokens. Completions followed haystack distractors rather than the needle.

| depth_pct | score | response_head |
|---:|---:|---|
| 33.91 | 0 | Based on the text provided, the best thing to do in San Francisco is to plant a university there. |
| 66.09 | 0 | Based on the text provided, the best thing to do in San Francisco is to live somewhere with personality. |
| 89.57 | 0 | Based on the text provided, the best thing to do in San Francisco is eat a steak. |

The other 107 cells passed. From 1K through 512K the grid is perfect.
