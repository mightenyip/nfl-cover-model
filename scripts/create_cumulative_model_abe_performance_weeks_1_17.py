#!/usr/bin/env python3
"""
Create cumulative Model A/B/E performance from Week 1..18 (so far) using
weekly analysis files in data/week{N}_actual_results_analysis.csv.

Important:
- Uses the repo's "underdog covered" perspective.
- Tracks pushes as ties (rows where actual cover is missing/NA).
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
    Return (total, wins, losses, pushes) for model_key in {'a','b','e'}.
    Total counts only games where we have a model prediction/correctness.
    Pushes (actual_cover is NA/blank) count as ties.
    """
    # Identify ties (pushes)
    if "actual_cover" in df.columns:
        pushes_mask = df["actual_cover"].isna()
    elif "consensus_correct" in df.columns:
        pushes_mask = df["consensus_correct"].isna()
    else:
        pushes_mask = pd.Series([False] * len(df))

    # Schema 1: explicit correctness column
    correct_col = f"model_{model_key}_correct"
    if correct_col in df.columns:
        usable = df[df[correct_col].notna()].copy()
        total = int(len(usable))
        pushes = int(pushes_mask.loc[usable.index].sum())
        wins = int((usable[correct_col] == True).sum())
        losses = int((usable[correct_col] == False).sum())
        # If older files have NA correctness for pushes, they won't be in usable anyway.
        # Still, prefer the computed pushes count (usually 0 for schema1 weeks).
        return total, wins, losses, pushes

    # Schema 2: prediction labels + actual_cover boolean
    pred_col = f"model_{model_key}_prediction"
    if pred_col in df.columns:
        usable = df[df[pred_col].notna()].copy()
        total = int(len(usable))
        pushes = int(pushes_mask.loc[usable.index].sum())
        wins = 0
        losses = 0
        if "actual_cover" in usable.columns:
            for p, a in zip(usable[pred_col], usable["actual_cover"]):
                if a is None or pd.isna(a):
                    continue
                if pred_is_underdog_cover(p) == bool(a):
                    wins += 1
                else:
                    losses += 1
        return total, wins, losses, pushes

    return 0, 0, 0, 0


def pct(correct: int, total: int) -> str:
    if total == 0:
        return ""
    return f"{(correct / total) * 100:.1f}%"

def pct_with_pushes(wins: int, losses: int, pushes: int) -> str:
    total = wins + losses + pushes
    if total == 0:
        return ""
    return f"{((wins + 0.5 * pushes) / total) * 100:.1f}%"


def main() -> None:
    out_path = Path("data/model_performance/cumulative_model_abe_performance.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for week in range(1, 19):
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
        a_total, a_wins, a_losses, a_pushes = compute_model_stats(df, "a")
        b_total, b_wins, b_losses, b_pushes = compute_model_stats(df, "b")
        e_total, e_wins, e_losses, e_pushes = compute_model_stats(df, "e")

        rows.append(
            {
                "Week": week,
                "ModelA_Total_Games": a_total if a_total else "",
                "ModelA_Correct": a_wins if a_total else "",
                "ModelA_Incorrect": a_losses if a_total else "",
                "ModelA_Pushes": a_pushes if a_total else "",
                "ModelA_Accuracy": pct_with_pushes(a_wins, a_losses, a_pushes),
                "ModelB_Total_Games": b_total if b_total else "",
                "ModelB_Correct": b_wins if b_total else "",
                "ModelB_Incorrect": b_losses if b_total else "",
                "ModelB_Pushes": b_pushes if b_total else "",
                "ModelB_Accuracy": pct_with_pushes(b_wins, b_losses, b_pushes),
                "ModelE_Total_Games": e_total if e_total else "",
                "ModelE_Correct": e_wins if e_total else "",
                "ModelE_Incorrect": e_losses if e_total else "",
                "ModelE_Pushes": e_pushes if e_total else "",
                "ModelE_Accuracy": pct_with_pushes(e_wins, e_losses, e_pushes),
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
    a_pushes = sum_int("ModelA_Pushes") if "ModelA_Pushes" in out.columns else 0
    b_pushes = sum_int("ModelB_Pushes") if "ModelB_Pushes" in out.columns else 0
    e_pushes = sum_int("ModelE_Pushes") if "ModelE_Pushes" in out.columns else 0

    total_row = {
        "Week": "TOTAL",
        "ModelA_Total_Games": a_total,
        "ModelA_Correct": a_correct,
        "ModelA_Incorrect": sum_int("ModelA_Incorrect"),
        "ModelA_Pushes": a_pushes,
        "ModelA_Accuracy": pct_with_pushes(a_correct, sum_int("ModelA_Incorrect"), a_pushes),
        "ModelB_Total_Games": b_total,
        "ModelB_Correct": b_correct,
        "ModelB_Incorrect": sum_int("ModelB_Incorrect"),
        "ModelB_Pushes": b_pushes,
        "ModelB_Accuracy": pct_with_pushes(b_correct, sum_int("ModelB_Incorrect"), b_pushes),
        "ModelE_Total_Games": e_total,
        "ModelE_Correct": e_correct,
        "ModelE_Incorrect": sum_int("ModelE_Incorrect"),
        "ModelE_Pushes": e_pushes,
        "ModelE_Accuracy": pct_with_pushes(e_correct, sum_int("ModelE_Incorrect"), e_pushes),
    }

    out = pd.concat([out, pd.DataFrame([total_row])], ignore_index=True)
    out.to_csv(out_path, index=False)
    print(f"✅ Wrote {out_path}")
    print(out.tail(5).to_string(index=False))


if __name__ == "__main__":
    main()


