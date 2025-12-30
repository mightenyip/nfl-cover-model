#!/usr/bin/env python3
"""
Create cumulative Model A/B/E performance from Week 1..17 (so far) using
weekly analysis files in data/week{N}_actual_results_analysis.csv.

Important:
- Uses the repo's "underdog covered" perspective.
- Excludes pushes (rows where actual cover is missing/NA).
- Handles multiple schemas:
  - Weeks 1-13 style: model_a_correct/model_b_correct/model_e_correct columns
  - Weeks 16+ style: model_a_prediction/model_b_prediction/model_e_prediction and actual_cover boolean

Output:
- data/model_performance/cumulative_model_abe_performance.csv
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def pred_is_underdog_cover(pred: str) -> bool | None:
    if pd.isna(pred):
        return None
    if pred in ("Cover", "Underdog Cover"):
        return True
    if pred in ("No Cover", "Favorite Cover"):
        return False
    raise ValueError(f"Unknown prediction label: {pred}")


def compute_model_stats(df: pd.DataFrame, model_key: str) -> tuple[int, int, int]:
    """
    Return (total, correct, incorrect) for model_key in {'a','b','e'}.
    Total counts only games where we have a model prediction/correctness AND a non-push actual.
    """
    # Identify pushes
    if "actual_cover" in df.columns:
        non_push = df[df["actual_cover"].notna()].copy()
    elif "consensus_correct" in df.columns:
        non_push = df[df["consensus_correct"].notna()].copy()
    else:
        non_push = df.copy()

    # Schema 1: explicit correctness column
    correct_col = f"model_{model_key}_correct"
    if correct_col in non_push.columns:
        usable = non_push[non_push[correct_col].notna()].copy()
        total = int(len(usable))
        correct = int((usable[correct_col] == True).sum())
        incorrect = total - correct
        return total, correct, incorrect

    # Schema 2: prediction labels + actual_cover boolean
    pred_col = f"model_{model_key}_prediction"
    if pred_col in non_push.columns and "actual_cover" in non_push.columns:
        usable = non_push[non_push[pred_col].notna()].copy()
        total = int(len(usable))
        correct = 0
        for p, a in zip(usable[pred_col], usable["actual_cover"]):
            if a is None or pd.isna(a):
                continue
            if pred_is_underdog_cover(p) == bool(a):
                correct += 1
        incorrect = total - correct
        return total, correct, incorrect

    return 0, 0, 0


def pct(correct: int, total: int) -> str:
    if total == 0:
        return ""
    return f"{(correct / total) * 100:.1f}%"


def main() -> None:
    out_path = Path("data/model_performance/cumulative_model_abe_performance.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for week in range(1, 18):
        week_path = Path(f"data/week{week}_actual_results_analysis.csv")
        if not week_path.exists():
            rows.append(
                {
                    "Week": week,
                    "ModelA_Total_Games": "",
                    "ModelA_Correct": "",
                    "ModelA_Incorrect": "",
                    "ModelA_Accuracy": "",
                    "ModelB_Total_Games": "",
                    "ModelB_Correct": "",
                    "ModelB_Incorrect": "",
                    "ModelB_Accuracy": "",
                    "ModelE_Total_Games": "",
                    "ModelE_Correct": "",
                    "ModelE_Incorrect": "",
                    "ModelE_Accuracy": "",
                }
            )
            continue

        df = pd.read_csv(week_path)
        a_total, a_correct, a_incorrect = compute_model_stats(df, "a")
        b_total, b_correct, b_incorrect = compute_model_stats(df, "b")
        e_total, e_correct, e_incorrect = compute_model_stats(df, "e")

        rows.append(
            {
                "Week": week,
                "ModelA_Total_Games": a_total if a_total else "",
                "ModelA_Correct": a_correct if a_total else "",
                "ModelA_Incorrect": a_incorrect if a_total else "",
                "ModelA_Accuracy": pct(a_correct, a_total),
                "ModelB_Total_Games": b_total if b_total else "",
                "ModelB_Correct": b_correct if b_total else "",
                "ModelB_Incorrect": b_incorrect if b_total else "",
                "ModelB_Accuracy": pct(b_correct, b_total),
                "ModelE_Total_Games": e_total if e_total else "",
                "ModelE_Correct": e_correct if e_total else "",
                "ModelE_Incorrect": e_incorrect if e_total else "",
                "ModelE_Accuracy": pct(e_correct, e_total),
            }
        )

    out = pd.DataFrame(rows)

    # TOTAL row (per-model denominators)
    def sum_int(col: str) -> int:
        return int(pd.to_numeric(out[col], errors="coerce").fillna(0).sum())

    a_total = sum_int("ModelA_Total_Games")
    b_total = sum_int("ModelB_Total_Games")
    e_total = sum_int("ModelE_Total_Games")

    a_correct = sum_int("ModelA_Correct")
    b_correct = sum_int("ModelB_Correct")
    e_correct = sum_int("ModelE_Correct")

    total_row = {
        "Week": "TOTAL",
        "ModelA_Total_Games": a_total,
        "ModelA_Correct": a_correct,
        "ModelA_Incorrect": a_total - a_correct,
        "ModelA_Accuracy": pct(a_correct, a_total),
        "ModelB_Total_Games": b_total,
        "ModelB_Correct": b_correct,
        "ModelB_Incorrect": b_total - b_correct,
        "ModelB_Accuracy": pct(b_correct, b_total),
        "ModelE_Total_Games": e_total,
        "ModelE_Correct": e_correct,
        "ModelE_Incorrect": e_total - e_correct,
        "ModelE_Accuracy": pct(e_correct, e_total),
    }

    out = pd.concat([out, pd.DataFrame([total_row])], ignore_index=True)
    out.to_csv(out_path, index=False)
    print(f"✅ Wrote {out_path}")
    print(out.tail(5).to_string(index=False))


if __name__ == "__main__":
    main()


