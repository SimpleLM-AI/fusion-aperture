# Sources

Retrieved 19 August 2026. These are the documents behind `comparisons/*.csv`. We did not re-run other systems.

Hsieh et al., RULER, arXiv:2404.06654. NVIDIA public table and repository: https://github.com/NVIDIA/RULER

Jiang et al., MInference 1.0, arXiv:2407.02490. Llama-3-8B-262K RULER at 128K: StreamingLLM 9.4, InfLLM 39.5, MInference 77.6.

Xiao et al., InfLLM, arXiv:2402.04617.

Xiao, Tian, Chen, Han, Lewis, StreamingLLM, arXiv:2309.17453.

Quest, arXiv:2406.10774. 74.9 at 96K on Llama-3.1-8B-Instruct as cited in the paper.

MagicPIG, arXiv:2410.16179. 81.7 at 96K as cited in the paper.

MiniCPM-SALA, arXiv:2602.11761. RULER 89.4 at 128K, 86.3 at 1M. MRCR 28.62 is 128K two needle.

Qwen3-Next-80B-A3B-Instruct model card, https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct. RULER at 1M, n=20: Next-80B 80.3, Qwen3-235B 84.5, Qwen3-30B 72.8.

Gemini 1.5, arXiv:2403.05530. Vendor needle protocol. Not used as a RULER or 110 cell peer.

OpenAI, Introducing GPT-4.1 in the API, 2025. Dataset https://huggingface.co/datasets/openai/mrcr. Two needle at 1M: GPT-4.1 0.463, mini 0.333, nano 0.120.

NVIDIA README also lists Qwen2.5-14B-Instruct-1M at 92.2 on the 128K column, not as a 1M RULER cell. GPT-4-1106-preview is 81.2 on that 128K column. Llama-3.1-8B-Instruct is 77.0. Qwen3-8B is 77.4.
