#!/usr/bin/env python3
"""
Create Week 15 actual results analysis by combining:
- schedule/week15_2025_odds.csv (spreads)
- predictions/week15_predictions_final.csv (model picks)
- hardcoded Week 15 final scores (from user-provided results)

Outputs: data/actual_results/week15/week15_actual_results_analysis.csv
"""

from __future__ import annotations

import pandas as pd


WEEK = 15
SEASON = 2025


def compute_underdog_cover(
    favorite_team: str,
    underdog_team: str,
    spread_line: float,
    away_team: str,
    home_team: str,
    away_score: int,
    home_score: int,
) -> bool | None:
    """Return True if underdog covered, False if favorite covered, None if push."""
    scores = {away_team: away_score, home_team: home_score}
    fav_score = scores[favorite_team]
    dog_score = scores[underdog_team]

    adj_dog = dog_score + abs(float(spread_line))
    if adj_dog > fav_score:
        return True
    if adj_dog < fav_score:
        return False
    return None


def main() -> None:
    schedule_path = f"schedule/week{WEEK}_2025_odds.csv"
    predictions_path = f"predictions/week{WEEK}_predictions_final.csv"
    output_path = f"data/actual_results/week{WEEK}/week{WEEK}_actual_results_analysis.csv"

    schedule_df = pd.read_csv(schedule_path)
    preds_df = pd.read_csv(predictions_path)

    # User-provided Week 15 final scores: (away_team, home_team) -> (away_score, home_score)
    results = {
        ("Falcons", "Buccaneers"): (29, 28),
        ("Browns", "Bears"): (3, 31),
        ("Ravens", "Bengals"): (24, 0),
        ("Chargers", "Chiefs"): (16, 13),
        ("Bills", "Patriots"): (35, 31),
        ("Commanders", "Giants"): (29, 21),
        ("Raiders", "Eagles"): (0, 31),
        ("Jets", "Jaguars"): (20, 48),
        ("Cardinals", "Texans"): (20, 40),
        ("Packers", "Broncos"): (26, 34),
        ("Lions", "Rams"): (34, 41),
        ("Panthers", "Saints"): (17, 20),
        ("Titans", "49ers"): (24, 37),
        ("Colts", "Seahawks"): (16, 18),
        ("Vikings", "Cowboys"): (34, 26),
        ("Dolphins", "Steelers"): (15, 28),
    }

    schedule_df["game"] = schedule_df["away_team"] + " @ " + schedule_df["home_team"]
    preds_keep = [
        "game",
        "consensus_prediction",
        "consensus_probability",
        "agreement",
        "model_a_prediction",
        "model_b_prediction",
        "model_e_prediction",
    ]
    preds_df = preds_df[preds_keep].copy()

    df = schedule_df.merge(preds_df, on="game", how="left")

    away_scores = []
    home_scores = []
    missing = []
    for _, row in df.iterrows():
        key = (row["away_team"], row["home_team"])
        if key not in results:
            missing.append(row["game"])
            away_scores.append(None)
            home_scores.append(None)
        else:
            a, h = results[key]
            away_scores.append(int(a))
            home_scores.append(int(h))

    if missing:
        raise ValueError(f"Missing results for games: {missing}")

    df["away_score"] = away_scores
    df["home_score"] = home_scores
    df["score"] = df["away_score"].astype(int).astype(str) + "-" + df["home_score"].astype(int).astype(str)

    df["actual_cover"] = [
        compute_underdog_cover(
            favorite_team=row["favorite_team"],
            underdog_team=row["underdog_team"],
            spread_line=float(row["spread_line"]),
            away_team=row["away_team"],
            home_team=row["home_team"],
            away_score=int(row["away_score"]),
            home_score=int(row["home_score"]),
        )
        for _, row in df.iterrows()
    ]

    def pred_is_underdog_cover(pred: str) -> bool | None:
        if pd.isna(pred):
            return None
        if pred in ("Cover", "Underdog Cover"):
            return True
        if pred in ("No Cover", "Favorite Cover"):
            return False
        raise ValueError(f"Unknown prediction label: {pred}")

    def correct(pred: str, actual: bool | None) -> bool | None:
        if actual is None or pd.isna(pred):
            return None
        return pred_is_underdog_cover(pred) == actual

    df["consensus_correct"] = [correct(p, a) for p, a in zip(df["consensus_prediction"], df["actual_cover"])]

    ordered_cols = [
        "game",
        "away_team",
        "home_team",
        "favorite_team",
        "underdog_team",
        "spread_line",
        "total_line",
        "score",
        "away_score",
        "home_score",
        "actual_cover",
        "consensus_prediction",
        "consensus_probability",
        "consensus_correct",
        "model_a_prediction",
        "model_b_prediction",
        "model_e_prediction",
        "agreement",
    ]
    df = df[ordered_cols].copy()
    df.to_csv(output_path, index=False)
    print(f"✅ Wrote {output_path} ({len(df)} games)")


if __name__ == "__main__":
    main()


