# Training-Free Long-Context Inference at a 2B-Quantized Mobile Memory Operating Point

**Fusion Aperture**  
19 August 2026

---

## Abstract

Long-context language models are typically demonstrated with large trained hosts, server-class memory, or both. We evaluate **Fusion Aperture** on a frozen **Qwen3.5-2B** checkpoint quantized to **Q4_K_M**, with **no additional long-context training**. Decoding is greedy. Quality is measured with stock public harnesses: NVIDIA RULER (13 synthetic tasks, $n=10$ per task), a Kamradt-style needle-in-a-haystack (NIAH) ladder of 110 cells, and OpenAI-MRCR (2-needle, 512K–1M). Memory is macOS physical footprint (`ri_phys_footprint`), reported as min / median / max.

On RULER, the host scores **80.3** at 128K and **72.0** at 1M. The retrieval slice (NIAH-8) remains **94.7** at 1M; the mean decline is concentrated in aggregation and QA tasks, not in needle retrieval. The NIAH ladder is **97.27%** overall and **100%** from 1K through 512K. OpenAI-MRCR 2-needle in the 512K–1M bin is **0.326** ($n=91$). Physical memory at 128K peaks at **492.9 MB**; at 1M the median generate envelope is **514.5 MB**, with a short peak of **766.6 MB**.

**Fusion Aperture** achieves state-of-the-art quality–memory efficiency among training-free long-context inference systems at the 2B Q4, mobile, half-gigabyte-class operating point. Trained 30B–235B hosts occupy a different compute and training regime.

---

## 1. Introduction

Claimed context length and delivered long-context quality have diverged. RULER [1] showed that many models advertised at 32K–128K fall well below a short-context baseline long before their nominal window, even when vanilla needle retrieval remains high. Subsequent systems attacked the gap with extra long-context training, larger sparse or hybrid hosts, or server-side KV management [2–6]. Those routes are effective. They are not the operating point of a phone-class assistant.

**Fusion Aperture** is an on-device inference stack. Conversations using it are capped at $10^6$ tokens in the long setting and 8,192 in the short setting. This paper does not specify Fusion Aperture’s internals. It reports a locked evaluation of the stack as shipped, on a single frozen quantized host, under public protocols, with physical memory treated as a first-class result.

The empirical question is narrow. Can a **2B-class 4-bit** model, **without** long-context continued pretraining or instruction tuning for million-token windows, sustain retrieval-grade long-context tests through 128K and 1M while remaining in a **half-gigabyte-class** physical envelope? If so, the relevant comparison is not MiniCPM-SALA or Qwen3-Next-80B on RULER@1M. It is training-free long-context inference at a mobile memory envelope.

We make four measurements.

1. **RULER**, stock NVIDIA client, greedy decode, $n=10$, lengths 4K–128K and a separate 1M cell.

2. **NIAH**, 10 lengths × 11 depths (110 cells) on Paul Graham essay haystacks.

3. **OpenAI-MRCR** v1, 2-needle, 512K–1M.

4. **Physical footprint** of the generation process during those runs, including dedicated RAM reruns at 32K, 64K, and 1M that reproduce the official score rows.

The resulting picture is a 2B Q4 host that tracks GPT-4-1106 on the NVIDIA RULER@128K leaderboard (80.3 vs 81.2) at a different scale and $n$, keeps RULER retrieval in the mid-90s at 1M, and runs in a half-gigabyte-class physical envelope. At 128K the peak is 492.9 MB. At 32K, 64K, 1M, and MRCR the recorded maxima sit above 500 MB. That is the quality–memory operating point this paper characterises.

---

## 2. Related work

**RULER.** Hsieh et al. [1] replace single-needle retrieval with 13 synthetic tasks spanning retrieval, multi-hop tracing, aggregation, and QA. The public NVIDIA table reports 4K–128K. Inference in the paper is greedy. Default sample count in that protocol is 500 per task per length. We follow the task set, the unweighted 13-task mean, and greedy decoding. We use $n=10$. NVIDIA does not publish a 1M column; 1M RULER figures in the literature come from model cards and later papers [5, 6].

**Training-free long-context methods.** StreamingLLM [4], InfLLM [3], MInference [2], Quest, and MagicPIG study inference-time sparsity or sliding windows, typically on 7B–8B hosts. On MInference’s Llama-3-8B-262K RULER@128K table, StreamingLLM is 9.4, InfLLM 39.5, and MInference 77.6 [2]. MagicPIG reports 81.7 at **96K**, Quest 74.9 at **96K**. None of these papers, to our reading, publish RULER at 1,048,576 or a Darwin physical-footprint envelope for a 2B Q4 mobile host.

**Trained long-context specialists.** MiniCPM-SALA [5] reports RULER@128K 89.4 and RULER@1M 86.3 on a trained 9B hybrid. Qwen3-Next-80B-A3B-Instruct reports RULER@1M 80.3 at $n=20$ [6]; Qwen3-235B 84.5 and Qwen3-30B 72.8 on the same card. Qwen2.5-14B-Instruct-1M appears on the NVIDIA README at 92.2 **@128K**, not as a 1M RULER cell. These systems answer a different question: quality at scale after long-context training.

**NIAH and MRCR.** Vendor NIAH (Gemini 1.5 [7]) and OpenAI-MRCR [8] are distinct protocols. Gemini’s >99.7% single-needle figure at 1M is not RULER and is not our 110-cell grid. OpenAI-MRCR grades with a mandatory hash prefix and `difflib.SequenceMatcher`; GPT-4.1 scores 0.463 on 2-needle @1M, mini 0.333, nano 0.120 [8].

**Memory.** Public long-context tables almost never report min / median / max physical footprint next to 1M-class quality. We treat that omission as a measurement gap, not as licence to invent other systems’ RAM.

---

## 3. Experimental setup

### 3.1 Host

All quality numbers in this paper use one frozen checkpoint: **Qwen3.5-2B**, **Q4_K_M**, memory-mapped. No extra long-context training is applied. Decode is temperature 0, matching NVIDIA RULER defaults (`top_p=1.0`, `top_k=32`). The RULER chat wrapper is template `base`. Generation is local on Apple silicon. Fusion Aperture’s product surface is iPhone 12 and later, A14 Bionic and later chips and devices; the memory meter in §4.4 is **macOS** physical footprint of the generation process.

### 3.2 RULER

We run the stock NVIDIA pipeline: `prepare.py` writes tokenized synthetic items; the model produces `pred/{task}.jsonl` containing `input`, `pred`, and gold `outputs`; `evaluate.py` writes `summary.csv`. Tasks are the 13 synthetic v1 names (`niah_single_*`, `niah_multikey_*`, `niah_multivalue`, `niah_multiquery`, `vt`, `cwe`, `fwe`, `qa_1`, `qa_2`). **NIAH-8** is the mean of the eight retrieval tasks. The headline mean is the unweighted mean of all 13. Lengths: 4K, 8K, 16K, 32K, 64K, 128K, and 1,048,576. Sample count: **10 per task per length**. Null answers: **0/10** at every length.

A RAM-only regeneration at 32K, 64K, and 1M (watcher attached to the generation process) reproduced the official 13-task rows. Those reruns supply the trusted memory traces at those lengths; they are not new quality claims.

### 3.3 NIAH

A Kamradt-style grid: 10 lengths (1K–1M) and 11 depths, 110 cells, Paul Graham essay haystack. A cell is a pass/fail. This protocol is not Gemini’s internal needle test [7] and not RULER’s NIAH-8.

### 3.4 OpenAI-MRCR

We use [openai/mrcr](https://huggingface.co/datasets/openai/mrcr). Official grade: if the completion does not start with `random_string_to_prepend`, the score is 0; otherwise prefixes are stripped and `SequenceMatcher.ratio` is the score [8]. This pack is **2-needle**, bin **(512K, 1M]**, $n=91$.

### 3.5 Physical memory

The meter is Darwin `ri_phys_footprint` from `proc_pid_rusage`, the Activity Monitor-class resident envelope. RSS on these runs reaches the 1.6–1.9 GB class and is discarded as a product figure. We report min, median, and max over interval samples of the generation process. The **samples** column in Table 5 is the number of those polls, not the number of benchmark items. Dense traces exist for RULER 32K–1M and for MRCR. NIAH quality is Table 3; NIAH was not densely footprinted and is omitted from Table 5. Cousin footprints are not estimated.

---

## 4. Results

### 4.1 RULER

**Table 1.** Unweighted 13-task mean and selected tasks. $n=10$. Nulls $0/10$.

| ctx | mean | NIAH-8 | vt | cwe | fwe | qa_1 | qa_2 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4K | 85.0 | 97.2 | 22 | 85 | 100 | 90 | 30 |
| 8K | 85.1 | 96.6 | 16 | 84 | 93.33 | 80 | 60 |
| 16K | 82.0 | 95.9 | 8 | 90 | 100 | 60 | 40 |
| 32K | 85.7 | 96.3 | 16 | 88 | 100 | 80 | 60 |
| 64K | 80.8 | 97.5 | 4 | 57 | 100 | 60 | 50 |
| 128K | **80.3** | 95.6 | 20 | 39 | 100 | 60 | 60 |
| 1M | **72.0** | **94.7** | 8 | 1 | 100 | 40 | 30 |

At 128K the mean sits beside GPT-4-1106 (81.2) on the NVIDIA column and above Llama-3.1-8B-Instruct (77.0) and Qwen3-8B (77.4) on that table [1]. Hosts and $n$ are unmatched; the comparison is neighbourhood, not a controlled bake-off.

At 1M, NIAH-8 is 94.7. The mean of 72.0 is pulled by CWE (1), VT (8), and QA (40 / 30). Frequent-word extraction remains 100. The length trend is therefore not a retrieval cliff. StreamingLLM’s 9.4 at 128K on an 8B host [2] is the opposite shape.

**Table 2.** Per-task scores at 128K and 1M.

| task | 128K | 1M |
|---|---:|---:|
| niah_single_1 | 100 | 100 |
| niah_single_2 | 100 | 100 |
| niah_single_3 | 100 | 90 |
| niah_multikey_1 | 100 | 100 |
| niah_multikey_2 | 70 | 100 |
| niah_multikey_3 | 100 | 70 |
| niah_multivalue | 97.5 | 97.5 |
| niah_multiquery | 97.5 | 100 |
| vt | 20 | 8 |
| cwe | 39 | 1 |
| fwe | 100 | 100 |
| qa_1 | 60 | 40 |
| qa_2 | 60 | 30 |
| mean | 80.3 | 72.0 |

On the separate 1M RULER literature board, MiniCPM-SALA reports 86.3 [5], Qwen3-235B 84.5, Qwen3-Next-80B 80.3, Qwen3-30B 72.8 ($n=20$) [6]. Our 72.0 is $n=10$, 2B Q4, training-free. The numbers can be read on one page; they do not share a training or parameter regime.

### 4.2 NIAH

**Table 3.** 110-cell ladder.

| | |
|---|---|
| Cells | 110 |
| Passes | 107 |
| Macro | 97.27% |
| 1K–512K | 100% (99/99) |
| 1M | 72.73% (8/11) |

The three misses are at 1M only, depths 33.91%, 66.09%, and 89.57%. Completions at those cells followed haystack distractors rather than the needle. We log them as failures.

### 4.3 OpenAI-MRCR

**Table 4.** 2-needle, 512K–1M.

| $n$ | mean |
|---:|---:|
| 91 | 0.326 |

GPT-4.1 is 0.463 on the corresponding blog cell; GPT-4.1 mini is 0.333 [8]. MiniCPM-SALA’s 28.62 is 128K-2N [5], a different length.

### 4.4 Physical memory

**Table 5.** Darwin `ri_phys_footprint`, MB. Sample counts are OS polls of the generation process.

| sweep | samples | min | median | max |
|---|---:|---:|---:|---:|
| RULER 32K | 839 | 445.5 | 479.5 | 543.3 |
| RULER 64K | 904 | 437.0 | 482.9 | 522.4 |
| RULER 128K | 257 | 387.1 | 450.2 | 492.9 |
| RULER 1M | 827 | 399.9 | 514.5 | 766.6 |
| MRCR 512K–1M | 69 | 482.5 | 520.6 | 520.7 |

A 500 MB line is not a hard envelope. Medians sit in 450.2–514.5 MB. Maxima exceed 500 MB at 32K (543.3), 64K (522.4), 1M (766.6), and MRCR (520.7). Only the 128K sweep stays under 500 MB at peak (492.9). The 1M maximum is a short sawtooth (a few 10 s intervals) returning near 500 MB; the 1M median 514.5 MB is the generate envelope, not a rounding of 766.6. MRCR’s 520.7 MB peak is stated, not rounded. RULER 4K–16K traces exist but come from an earlier mixed watcher and are omitted here (Appendix B).

---

## 5. Discussion

**Operating point.** Fusion Aperture on this host is not the strongest published RULER@1M mean. Trained 9B–235B systems sit higher [5, 6]. The comparison that matches the product is training-free inference at 2B Q4 and a half-gigabyte-class mobile memory envelope. In that class, published training-free RULER@128K numbers on 8B hosts either collapse with length (StreamingLLM 9.4, InfLLM 39.5) or require a larger model (MInference 77.6) [2], and they do not come with a 2B Q4 physical-footprint series through 1M. Under that joint constraint, the measured quality–memory pair is state of the art.

**The 500 MB line.** Table 5 does not support a hard sub-500 MB bound. 128K peaks at 492.9 MB. 32K, 64K, 1M, and MRCR each record a maximum above 500 MB. At 1M the typical generate envelope is already 514.5 MB (median); 766.6 MB is the recorded peak, not the typical cell. The product budget and the measured envelope are therefore not the same number.

**Retrieval versus mean.** RULER’s 1M mean of 72.0 would read as context death if NIAH-8 were omitted. It is not: NIAH-8 is 94.7. Aggregation and QA are the residual. That partition is the result. A causal account of CWE at 1M is outside this paper.

**$n=10$.** Greedy decode makes each item stable. It does not replace the paper’s $n=500$ [1] or Qwen’s $n=20$ at 1M [6]. Confidence intervals are therefore wider than those studies. Expanding $n$ is future measurement on the same host, not a silent revision of Table 1.

**Device.** Quality and RAM are measured on Mac. The product surface is iPhone 12 and later (A14 Bionic and later chips and devices). Transfer of the physical envelope across devices is left to a follow-up measurement.

**Other systems’ memory.** We compare against published scores and stated training and size regimes. We do not impute other systems’ physical memory from KV formulae.

---

## 6. Conclusion

**Fusion Aperture**, on a frozen 2B Q4 host without extra long-context training, evaluated under stock RULER, NIAH, and OpenAI-MRCR, delivers 80.3 at RULER@128K, 72.0 / 94.7 (mean / NIAH-8) at RULER@1M, 97.27% on a 110-cell NIAH ladder, and 0.326 on MRCR 2-needle 512K–1M. Physical footprint medians sit in 450–515 MB; the 128K peak is 492.9 MB; several sweeps, including 1M (766.6 MB), exceed 500 MB at max. Among training-free long-context inference systems at this size, quantization, and half-gigabyte-class mobile envelope, that is state-of-the-art quality–memory efficiency.

---

## Acknowledgements

RULER, NIAH practice, and OpenAI-MRCR are used as published. Fusion Aperture’s implementation is not described in this manuscript. Evaluation materials that accompany this paper are licensed CC BY-NC-ND 4.0; the stack is not.

---

## References

[1] C.-P. Hsieh et al., “RULER: What’s the Real Context Size of Your Long-Context Language Models?,” arXiv:2404.06654, 2024. [NVIDIA/RULER](https://github.com/NVIDIA/RULER).

[2] H. Jiang et al., “MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention,” arXiv:2407.02490, 2024.

[3] C. Xiao et al., “InfLLM: Unveiling the Intrinsic Capacity of LLMs for Understanding Extremely Long Sequences with Training-Free Memory,” arXiv:2402.04617, 2024.

[4] G. Xiao, Y. Tian, B. Chen, S. Han, and M. Lewis, “Efficient Streaming Language Models with Attention Sinks,” arXiv:2309.17453, 2023.

[5] MiniCPM-SALA, arXiv:2602.11761, 2026.

[6] Qwen Team, [Qwen3-Next-80B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) model card, 1M RULER table, $n=20$.

[7] G. Team, “Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context,” arXiv:2403.05530, 2024.

[8] OpenAI, “Introducing GPT-4.1 in the API,” 2025; dataset [openai/mrcr](https://huggingface.co/datasets/openai/mrcr).

[9] “Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference,” arXiv:2406.10774, 2024.

[10] “MagicPIG: LSH Sampling for Efficient LLM Generation,” arXiv:2410.16179, 2024.

---

## Appendix A. Artifact hashes

SHA-256 of official summary files (UTF-8 bytes). Prediction jsonl with prompt, output, and gold accompany each RULER length and are the audit trail. The NIAH lab sidecar is not in this pack; it contained a local filesystem path and a wall-clock block. Cell counts, per-length means, and the three miss depths in the public extract are unchanged.

| artifact | SHA-256 |
|---|---|
| RULER 4K summary.csv | `2b9f31820b0c3b47890ed91a7c413c67ca423e8dab7d92e7ff6cfbb90b0177fb` |
| RULER 8K summary.csv | `aa4e13493b72d55b346bfc164b182ce15f97282daf8d46c0ecdc59fdec652957` |
| RULER 16K summary.csv | `2d70d373c386bab28e5f021c5a3bb13c7952a21477d583a1c96d7a06dcf36892` |
| RULER 32K summary.csv | `3bdf21b7793a114cd57ff4b98c0d74638e946a9ab7400bf0196451a9d7eedd37` |
| RULER 64K summary.csv | `2ff88b66ece3e0f80f1436424eda08363930a7b69d907496f9a246086e3f97de` |
| RULER 128K summary.csv | `0c649e7954d51becf4c13b9885470db67152893fc024ce1096e16888a889e5ba` |
| RULER 1M summary.csv | `a7b0fd1a149ae754cbc86e7361f09564af9e73da47b775f663b3ca89779b06f2` |
| NIAH public ladder summary (this pack) | `d1978137d7303bbe38c217ef6ea37ecf2d25a3b78c6bb2ba273482044f81de9e` |
| NIAH lab sidecar (not shipped) | `58aca1ecfd60870e474119c8413f123d0fb9a135c2aff2fcfe26fa7726c95299` |
| MRCR SUMMARY_2needle.json | `728cd4ec9484b97f30742275ada52329c05a1163497db9b5640d28cb52fb6023` |

---

## Appendix B. Additional memory traces

RULER 4K / 8K / 16K physical samples (mixed earlier watcher; caution): 4K min/median/max 435.6 / 439.8 / 444.0 ($n=128$); 8K 435.6 / 435.6 / 435.6 ($n=129$); 16K 444.0 / 444.0 / 444.0 ($n=30$ usable). They are not used in Table 5.

NIAH 32K–1M: six interval samples (436.0 / 456.0 / 461.0 MB). That is too sparse to report as a sweep; NIAH quality remains Table 3.
