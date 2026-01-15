#!/usr/bin/env python3
"""
Backfill missing Model A/B predictions (and recompute consensus) into:
- data/actual_results/week2/week2_actual_results_analysis.csv
- data/actual_results/week6/week6_actual_results_analysis.csv

And create:
- data/actual_results/week10/week10_actual_results_analysis.csv

Why:
Some early weekly analysis files have game results (actual_cover) but are missing
Model A/B picks due to earlier prediction export issues (e.g., blank predicted_cover).

This script keeps the *existing early-week schema* used by weeks 1-13:
game,score,spread,underdog,actual_cover,model_a_pred,model_a_correct,...,model_e_pred,model_e_correct,consensus_pred,consensus_correct

All predictions and grading are from the **underdog-cover** perspective.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_model_preds(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Normalize common columns
    if "predicted_cover" in df.columns:
        df = df.rename(columns={"predicted_cover": "pred"})
    elif "pred" in df.columns:
        pass
    else:
        raise ValueError(f"Unknown model prediction schema in {path}")

    if "game" not in df.columns:
        raise ValueError(f"Missing game column in {path}")
    return df[["game", "pred"]].copy()


def load_model_a_preds_with_fallback(path: str) -> pd.DataFrame:
    """Model A sometimes has blank predicted_cover; fallback to probability > 0.5."""
    df = pd.read_csv(path)
    if "game" not in df.columns:
        raise ValueError(f"Missing game column in {path}")

    if "predicted_cover" in df.columns:
        pred = df["predicted_cover"]
        if pred.isna().any() and "probability" in df.columns:
            # Fill missing predicted_cover using probability threshold
            filled = pred.copy()
            mask = filled.isna()
            filled = filled.astype("object")
            filled.loc[mask] = (df.loc[mask, "probability"].astype(float) > 0.5).astype(bool)
            df["predicted_cover"] = filled.astype(bool)
        df = df.rename(columns={"predicted_cover": "pred"})
        return df[["game", "pred"]].copy()

    raise ValueError(f"Unknown Model A schema in {path}")


def consensus_vote(a: bool, b: bool, e: bool) -> bool:
    return (int(a) + int(b) + int(e)) >= 2


def update_week_analysis_in_place(week: int) -> None:
    path = Path(f"data/actual_results/week{week}/week{week}_actual_results_analysis.csv")
    if not path.exists():
        raise FileNotFoundError(str(path))

    df = pd.read_csv(path)
    if "game" not in df.columns or "actual_cover" not in df.columns:
        raise ValueError(f"Unexpected schema in {path}")

    # Drop any pre-existing model/consensus columns to avoid duplicate names after merges
    drop_cols = [
        "model_a_pred",
        "model_a_correct",
        "model_b_pred",
        "model_b_correct",
        "model_e_pred",
        "model_e_correct",
        "consensus_pred",
        "consensus_correct",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")

    ma = load_model_a_preds_with_fallback(f"models/model_a/model_a_week{week}_predictions.csv")
    mb = load_model_preds(f"models/model_b/model_b_week{week}_predictions.csv")
    me = load_model_preds(f"models/model_e/model_e_week{week}_predictions.csv")

    merged = df.merge(ma, on="game", how="left").rename(columns={"pred": "model_a_pred"})
    merged = merged.merge(mb, on="game", how="left").rename(columns={"pred": "model_b_pred"})
    merged = merged.merge(me, on="game", how="left").rename(columns={"pred": "model_e_pred"})

    # Compute correctness where predictions exist and not a push (push is possible via NA actual_cover in some weeks)
    def correct(pred, actual):
        if pd.isna(pred) or pd.isna(actual):
            return None
        return bool(pred) == bool(actual)

    merged["model_a_correct"] = [correct(p, a) for p, a in zip(merged["model_a_pred"], merged["actual_cover"])]
    merged["model_b_correct"] = [correct(p, a) for p, a in zip(merged["model_b_pred"], merged["actual_cover"])]
    merged["model_e_correct"] = [correct(p, a) for p, a in zip(merged["model_e_pred"], merged["actual_cover"])]

    # Consensus (A/B/E)
    cons = []
    cons_correct = []
    for a, b, e, actual in zip(
        merged["model_a_pred"], merged["model_b_pred"], merged["model_e_pred"], merged["actual_cover"]
    ):
        if pd.isna(a) or pd.isna(b) or pd.isna(e):
            cons.append(None)
            cons_correct.append(None if pd.isna(actual) else None)
            continue
        c = consensus_vote(bool(a), bool(b), bool(e))
        cons.append(c)
        cons_correct.append(None if pd.isna(actual) else (c == bool(actual)))

    merged["consensus_pred"] = cons
    merged["consensus_correct"] = cons_correct

    # Keep original column order (base columns) then append model/consensus columns
    cols = list(df.columns) + [
        "model_a_pred",
        "model_a_correct",
        "model_b_pred",
        "model_b_correct",
        "model_e_pred",
        "model_e_correct",
        "consensus_pred",
        "consensus_correct",
    ]
    merged = merged[cols].copy()
    merged.to_csv(path, index=False)
    print(f"✅ Updated {path}")


def create_week10_analysis() -> None:
    """
    Week 10 doesn't have a week10_actual_results_analysis.csv in the repo.
    We create it from data/ats_results/week10/week10_ats_results.csv (has spread + underdog_covered) and model prediction CSVs.
    """
    ats_path = Path("data/ats_results/week10/week10_ats_results.csv")
    if not ats_path.exists():
        raise FileNotFoundError(str(ats_path))

    ats = pd.read_csv(ats_path)
    # NOTE: week10_ats_results.csv already has a `game` column in away @ home format.

    sched = pd.read_csv("schedule/week10_2025_odds.csv")
    sched["game"] = sched["away_team"] + " @ " + sched["home_team"]

    # Build a lookup by game label (matches schedule/model files)
    ats_key = {str(r["game"]): r for _, r in ats.iterrows()}

    rows = []
    missing = []
    for _, r in sched.iterrows():
        key = str(r["game"])
        if key not in ats_key:
            missing.append(f"{r['away_team']} @ {r['home_team']}")
            continue
        ar = ats_key[key]
        rows.append(
            {
                "game": r["game"],
                "score": ar["final_score"],
                "spread": ar["spread"],
                "underdog": ar["underdog"],
                "actual_cover": bool(ar["underdog_covered"]),
            }
        )

    if missing:
        raise ValueError(f"Missing Week 10 ATS results for games: {missing}")

    df = pd.DataFrame(rows)

    ma = load_model_a_preds_with_fallback("models/model_a/model_a_week10_predictions.csv").rename(
        columns={"pred": "model_a_pred"}
    )
    mb = load_model_preds("models/model_b/model_b_week10_predictions.csv").rename(columns={"pred": "model_b_pred"})
    me = load_model_preds("models/model_e/model_e_week10_predictions.csv").rename(columns={"pred": "model_e_pred"})

    df = df.merge(ma, on="game", how="left").merge(mb, on="game", how="left").merge(me, on="game", how="left")

    def correct(pred, actual):
        if pd.isna(pred):
            return None
        return bool(pred) == bool(actual)

    df["model_a_correct"] = [correct(p, a) for p, a in zip(df["model_a_pred"], df["actual_cover"])]
    df["model_b_correct"] = [correct(p, a) for p, a in zip(df["model_b_pred"], df["actual_cover"])]
    df["model_e_correct"] = [correct(p, a) for p, a in zip(df["model_e_pred"], df["actual_cover"])]

    cons = []
    cons_correct = []
    for a, b, e, actual in zip(df["model_a_pred"], df["model_b_pred"], df["model_e_pred"], df["actual_cover"]):
        if pd.isna(a) or pd.isna(b) or pd.isna(e):
            cons.append(None)
            cons_correct.append(None)
            continue
        c = consensus_vote(bool(a), bool(b), bool(e))
        cons.append(c)
        cons_correct.append(c == bool(actual))

    df["consensus_pred"] = cons
    df["consensus_correct"] = cons_correct

    out_path = Path("data/actual_results/week10/week10_actual_results_analysis.csv")
    df.to_csv(out_path, index=False)
    print(f"✅ Created {out_path}")


def main() -> None:
    update_week_analysis_in_place(2)
    update_week_analysis_in_place(6)
    create_week10_analysis()


if __name__ == "__main__":
    main()


