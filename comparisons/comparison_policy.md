# Comparison policy

This folder copies published scores so a reader does not have to hunt the URLs. It is not a controlled bake-off.

Length is mandatory. NVIDIA RULER at 128K and a 1M RULER cell are different boards. A 96K MagicPIG or Quest number is marked as 96K. MiniCPM’s MRCR 28.62 is 128K two needle, not our 512K to 1M bin.

Sample count is mandatory when the source states it. Ours is 10 per RULER task. Qwen’s 1M card is 20. NVIDIA’s paper default is 500. Those are not interchangeable.

Host size and training status are mandatory. Our eval host is a 2B 4-bit checkpoint with no extra long context training. MiniCPM-SALA and the Qwen 1M RULER rows are trained systems at a different scale.

Scores and URLs only. We do not invent other systems’ RAM. We do not put Gemini’s vendor needle figure on the RULER axis or on our 110 cell grid without saying the protocol differs, which in practice means we do not put it on a ranking CSV.

We do not write “we beat X because.” Neighbourhood is allowed. Mechanism is not.

If a source updates a card, `sources.md` should gain a retrieved date rather than a silent overwrite of a CSV without a changelog note.
