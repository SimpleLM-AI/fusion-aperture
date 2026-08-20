#!/usr/bin/env python3
# Copyright (c) 2026 Fusion Aperture. SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""Rebuild headline averages from the score files in this pack."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NIAH8 = 8
TASKS = [
    "niah_single_1",
    "niah_single_2",
    "niah_single_3",
    "niah_multikey_1",
    "niah_multikey_2",
    "niah_multikey_3",
    "niah_multivalue",
    "niah_multiquery",
    "vt",
    "cwe",
    "fwe",
    "qa_1",
    "qa_2",
]
LENGTHS = [
    ("4K", "4096", 4096),
    ("8K", "8192", 8192),
    ("16K", "16384", 16384),
    ("32K", "32768", 32768),
    ("64K", "65536", 65536),
    ("128K", "131072", 131072),
    ("1M", "1048576", 1048576),
]


def parse_summary(path: Path) -> dict:
    rows = list(csv.reader(path.open(encoding="utf-8")))
    by_name = {r[0]: r[1:] for r in rows}
    names = by_name["Tasks"]
    scores = [float(x) for x in by_name["Score"]]
    nulls = by_name["Nulls"]
    if names != TASKS:
        raise SystemExit(f"unexpected task order in {path}")
    return {
        "scores": dict(zip(names, scores)),
        "nulls": dict(zip(names, nulls)),
        "mean": sum(scores) / len(scores),
        "niah8": sum(scores[:NIAH8]) / NIAH8,
    }


def approx(a: float, b: float, tol: float = 0.051) -> bool:
    return abs(a - b) <= tol


def main() -> int:
    failed = 0
    ladder_path = ROOT / "results" / "ruler" / "context_ladder.csv"
    ladder = {}
    with ladder_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ladder[row["ctx"]] = row

    print("RULER")
    for label, folder, _tokens in LENGTHS:
        summary = ROOT / "results" / "ruler" / folder / "summary.csv"
        parsed = parse_summary(summary)
        if any(v != "0/10" for v in parsed["nulls"].values()):
            print("  nulls not 0/10 at", label)
            failed += 1
        row = ladder[label]
        if not approx(parsed["mean"], float(row["mean"])):
            print("  mean mismatch", label, parsed["mean"], row["mean"])
            failed += 1
        if not approx(parsed["niah8"], float(row["niah8"])):
            print("  niah8 mismatch", label, parsed["niah8"], row["niah8"])
            failed += 1
        print(
            f"  {label:4} mean {parsed['mean']:.2f}  niah8 {parsed['niah8']:.2f}  nulls 0/10"
        )

    per_task = ROOT / "results" / "ruler" / "per_task_128k_1m.csv"
    s128 = parse_summary(ROOT / "results" / "ruler" / "131072" / "summary.csv")
    s1m = parse_summary(ROOT / "results" / "ruler" / "1048576" / "summary.csv")
    with per_task.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["task"] == "mean":
                continue
            if not approx(s128["scores"][row["task"]], float(row["score_128k"])):
                print("  per-task 128K mismatch", row["task"])
                failed += 1
            if not approx(s1m["scores"][row["task"]], float(row["score_1m"])):
                print("  per-task 1M mismatch", row["task"])
                failed += 1

    niah = json.loads((ROOT / "results" / "niah" / "ladder_summary.json").read_text())
    print("NIAH")
    if niah["n_cells"] != 110 or niah["passes"] != 107 or niah["misses"] != 3:
        print("  cell counts")
        failed += 1
    if not approx(niah["overall_cell_macro"] * 100, 97.27, tol=0.02):
        print("  macro")
        failed += 1
    if len(niah["misses_at_1m"]) != 3:
        print("  miss list")
        failed += 1
    print(f"  {niah['passes']}/{niah['n_cells']}  macro {niah['overall_cell_macro']}")

    mrcr = json.loads((ROOT / "results" / "mrcr" / "summary.json").read_text())
    mean = mrcr["512k-1M"]["mean"]
    n = mrcr["512k-1M"]["n"]
    print("MRCR")
    if n != 91:
        print("  n")
        failed += 1
    if not approx(mean, 0.326, tol=0.001):
        print("  mean", mean)
        failed += 1
    print(f"  n={n} mean {mean:.6f}")

    print("failed" if failed else "ok")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
