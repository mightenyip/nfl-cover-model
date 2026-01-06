#!/usr/bin/env python3
"""
Recompute cumulative consensus performance (Weeks 1..18) from weekly
`data/week{N}_actual_results_analysis.csv` files and overwrite:

- data/model_performance/cumulative_model_performance.csv

Notes:
- Uses the repo's "underdog covered" perspective.
- Tracks pushes as ties (rows where actual_cover is NA/blank OR consensus_correct is NA).
- Supports multiple schemas:
  - Weeks 1-10 style: consensus_pred boolean, consensus_correct boolean, actual_cover boolean
  - Weeks 11+ style: consensus_prediction string, consensus_correct boolean, actual_cover boolean

Column meaning in output:
- Consensus_Cover_Pred / Actual_Covers == UNDERDOG cover counts
- Consensus_No_Cover_Pred / Actual_No_Covers == FAVORITE cover counts
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def pred_is_underdog_cover(pred: object) -> bool | None:
    if pd.isna(pred):
        return None
    if isinstance(pred, bool):
        return bool(pred)
    s = str(pred).strip()
    if s in ("Cover", "Underdog Cover", "True"):
        return True
    if s in ("No Cover", "Favorite Cover", "False"):
        return False
    raise ValueError(f"Unknown prediction label: {pred}")


def pct(correct: int, total: int) -> str:
    if total == 0:
        return ""
    return f"{(correct / total) * 100:.1f}%"

def pct_with_pushes(wins: int, losses: int, pushes: int) -> str:
    total = wins + losses + pushes
    if total == 0:
        return ""
    return f"{((wins + 0.5 * pushes) / total) * 100:.1f}%"


def load_week_df(week: int) -> pd.DataFrame | None:
    p = Path(f"data/week{week}_actual_results_analysis.csv")
    if not p.exists():
        return None
    return pd.read_csv(p)


def compute_week_row(week: int, df: pd.DataFrame) -> dict[str, object]:
    # Determine pushes (ties) from actual_cover where available; fallback to consensus_correct NA.
    if "actual_cover" in df.columns:
        pushes = int(df["actual_cover"].isna().sum())
        graded = df[df["actual_cover"].notna()].copy()
    elif "consensus_correct" in df.columns:
        pushes = int(df["consensus_correct"].isna().sum())
        graded = df[df["consensus_correct"].notna()].copy()
    else:
        pushes = 0
        graded = df.copy()

    # Consensus W/L on non-push games
    if "consensus_correct" in graded.columns:
        wins = int((graded["consensus_correct"] == True).sum())
        losses = int((graded["consensus_correct"] == False).sum())
    else:
        wins = losses = 0

    # Consensus prediction counts (underdog vs favorite)
    cons_pred_col = "consensus_prediction" if "consensus_prediction" in df.columns else "consensus_pred"
    if cons_pred_col in df.columns:
        cons_is_dog = df[cons_pred_col].map(pred_is_underdog_cover)
        cons_cover_pred = int((cons_is_dog == True).sum())
        cons_no_cover_pred = int((cons_is_dog == False).sum())
    else:
        cons_cover_pred = cons_no_cover_pred = 0

    # Actual cover counts (underdog vs favorite)
    if "actual_cover" in df.columns:
        actual_cover = int((df["actual_cover"] == True).sum())
        actual_no_cover = int((df["actual_cover"] == False).sum())
        actual_pushes = int(df["actual_cover"].isna().sum())
    else:
        actual_cover = actual_no_cover = 0
        actual_pushes = pushes

    total = wins + losses + pushes

    return {
        "Week": week,
        "Total_Games": total,
        "Consensus_Correct": wins,
        "Consensus_Incorrect": losses,
        "Consensus_Pushes": pushes,
        "Consensus_Accuracy": pct_with_pushes(wins, losses, pushes),
        "Consensus_Cover_Pred": cons_cover_pred,
        "Consensus_No_Cover_Pred": cons_no_cover_pred,
        "Actual_Covers": actual_cover,
        "Actual_No_Covers": actual_no_cover,
        "Actual_Pushes": actual_pushes,
    }


def main() -> None:
    out_path = Path("data/model_performance/cumulative_model_performance.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    for week in range(1, 19):
        df = load_week_df(week)
        if df is None:
            continue
        rows.append(compute_week_row(week, df))

    out = pd.DataFrame(rows)

    # TOTAL row
    total_games = int(out["Total_Games"].sum())
    total_correct = int(out["Consensus_Correct"].sum())
    total_incorrect = int(out["Consensus_Incorrect"].sum())
    total_pushes = int(out["Consensus_Pushes"].sum()) if "Consensus_Pushes" in out.columns else 0
    total_cover_pred = int(out["Consensus_Cover_Pred"].sum())
    total_no_cover_pred = int(out["Consensus_No_Cover_Pred"].sum())
    total_actual_cover = int(out["Actual_Covers"].sum())
    total_actual_no_cover = int(out["Actual_No_Covers"].sum())
    total_actual_pushes = int(out["Actual_Pushes"].sum()) if "Actual_Pushes" in out.columns else 0

    total_row = {
        "Week": "TOTAL",
        "Total_Games": total_games,
        "Consensus_Correct": total_correct,
        "Consensus_Incorrect": total_incorrect,
        "Consensus_Pushes": total_pushes,
        "Consensus_Accuracy": pct_with_pushes(total_correct, total_incorrect, total_pushes),
        "Consensus_Cover_Pred": total_cover_pred,
        "Consensus_No_Cover_Pred": total_no_cover_pred,
        "Actual_Covers": total_actual_cover,
        "Actual_No_Covers": total_actual_no_cover,
        "Actual_Pushes": total_actual_pushes,
    }
    out = pd.concat([out, pd.DataFrame([total_row])], ignore_index=True)
    out.to_csv(out_path, index=False)
    print(f"✅ Wrote {out_path}")
    print(out.tail(5).to_string(index=False))


if __name__ == "__main__":
    main()


