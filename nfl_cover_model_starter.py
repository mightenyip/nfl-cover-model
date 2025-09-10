#!/usr/bin/env python3
"""
NFL ATS (Against the Spread) Cover Probability Model — Starter Template (pandas)

What this script does:
1) Loads nflverse play-by-play (pbp) and schedule/lines for selected seasons
2) Builds per-team, per-game feature rows based on EPA and related metrics
3) Adds rolling-window features (form) from prior games
4) Creates a labeled training table: did the team cover the spread?
5) Trains a simple logistic regression and evaluates (log loss, Brier, accuracy)
6) Saves feature table and model artifacts for iteration

Dependencies (install as needed):
    pip install pandas pyarrow scikit-learn matplotlib tqdm

Notes:
- The HTTP links used here point to the public nflverse/nflfastR mirrors on GitHub.
- For speed/reliability, you may want to download Parquet/CSV locally or use the nflverse R packages.
- This is a **starter**: edit feature engineering, windows, model choice, and evaluation to taste.
"""

from __future__ import annotations
import io
import os
import sys
from typing import List, Tuple

import pandas as pd
import numpy as np
import pyarrow
from tqdm import tqdm

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, brier_score_loss, accuracy_score
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt


# -----------------------------
# Configuration
# -----------------------------

SEASONS = list(range(2015, 2025))  # edit as desired
DATA_DIR = os.environ.get("NFL_DATA_DIR", ".")  # optional: set to a local data folder
SAVE_FEATURES_CSV = "team_game_features.csv"
SAVE_MODEL = "logreg_model.pkl"  # optional: if you want to persist


# -----------------------------
# Data Access Helpers
# -----------------------------

def load_pbp_for_seasons(seasons: List[int]) -> pd.DataFrame:
    """
    Load nflverse play-by-play parquet for the given seasons.
    Uses GitHub-hosted parquet files by default. Consider caching locally.
    """
    # Parquet mirrors: https://github.com/nflverse/nflverse-data/releases
    dfs = []
    for yr in seasons:
        # Parquet URL pattern as of 2024+; adjust if structure changes
        url = f"https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{yr}.parquet"
        print(f"Loading PBP {yr} from {url} ...")
        try:
            df = pd.read_parquet(url, engine="pyarrow")
        except Exception as e:
            print(f"WARNING: Could not load {url} ({e}). Trying local fallback if present...")
            local_path = os.path.join(DATA_DIR, f"play_by_play_{yr}.parquet")
            df = pd.read_parquet(local_path, engine="pyarrow")
        dfs.append(df)
    pbp = pd.concat(dfs, ignore_index=True)
    # Keep only regular season + playoffs
    pbp = pbp[pbp["season_type"].isin(["REG", "POST"])]
    return pbp


def create_week1_2025_schedule() -> pd.DataFrame:
    """
    Create Week 1 2025 NFL schedule with correct spreads from CSV file.
    Simple, clean approach without web scraping.
    """
    # Load from CSV file
    csv_path = os.path.join(os.path.dirname(__file__), "week1_2025_odds.csv")
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(f"Loaded Week 1 2025 odds from {csv_path}")
    else:
        print(f"CSV file not found at {csv_path}, using fallback data")
        # Fallback data if CSV doesn't exist
        games = [
            {'away_team': 'Raiders', 'home_team': 'Patriots', 'spread_line': 2.5, 'total_line': 44.5},
            {'away_team': 'Steelers', 'home_team': 'Jets', 'spread_line': -3.0, 'total_line': 37.5},
            {'away_team': 'Dolphins', 'home_team': 'Colts', 'spread_line': 1.5, 'total_line': 47.5},
            {'away_team': 'Cardinals', 'home_team': 'Saints', 'spread_line': -6.0, 'total_line': 44.5},
            {'away_team': 'Giants', 'home_team': 'Commanders', 'spread_line': 6.0, 'total_line': 45.5},
            {'away_team': 'Panthers', 'home_team': 'Jaguars', 'spread_line': 4.5, 'total_line': 46.5},
            {'away_team': 'Bengals', 'home_team': 'Browns', 'spread_line': -5.5, 'total_line': 47.5},
            {'away_team': 'Buccaneers', 'home_team': 'Falcons', 'spread_line': -1.5, 'total_line': 47.5},
            {'away_team': 'Titans', 'home_team': 'Broncos', 'spread_line': 8.5, 'total_line': 42.5},
            {'away_team': '49ers', 'home_team': 'Seahawks', 'spread_line': -1.5, 'total_line': 43.5},
            {'away_team': 'Lions', 'home_team': 'Packers', 'spread_line': 1.5, 'total_line': 47.5},
            {'away_team': 'Texans', 'home_team': 'Rams', 'spread_line': 3.0, 'total_line': 43.5},
            {'away_team': 'Ravens', 'home_team': 'Bills', 'spread_line': -1.5, 'total_line': 50.5},
            {'away_team': 'Vikings', 'home_team': 'Bears', 'spread_line': -1.5, 'total_line': 43.5},
        ]
        df = pd.DataFrame(games)
    
    # Add metadata
    df['season'] = 2025
    df['week'] = 1
    df['game_date'] = None
    df['game_id'] = df.apply(lambda x: f"2025_01_{x['away_team']}_{x['home_team']}", axis=1)
    
    return df


def load_schedule_with_lines(seasons: List[int]) -> pd.DataFrame:
    """
    Load schedule + betting lines.
    For 2025 Week 1, use the hardcoded schedule. For other seasons, try local CSV files.
    """
    dfs = []
    
    for yr in seasons:
        print(f"Loading schedule+lines for {yr}...")
        
        # For 2025 Week 1, use our hardcoded schedule
        if yr == 2025:
            df = create_week1_2025_schedule()
            # Add dummy scores for now (you'd need to get these from another source)
            df['home_score'] = np.nan
            df['away_score'] = np.nan
            dfs.append(df)
            print(f"Loaded Week 1 2025 schedule with {len(df)} games")
            continue
        
        # For other seasons, try local CSV files
        try:
            local_path = os.path.join(DATA_DIR, f"sched_{yr}.csv")
            if os.path.exists(local_path):
                df = pd.read_csv(local_path)
                dfs.append(df)
                print(f"Loaded local schedule for {yr}")
            else:
                print(f"No local schedule file found for {yr}")
        except Exception as e:
            print(f"Could not load local schedule for {yr}: {e}")
    
    if not dfs:
        raise ValueError("No schedule data could be loaded for any season")
    
    sched = pd.concat(dfs, ignore_index=True)
    
    # Keep only played games with scores (if available and not NaN)
    if 'home_score' in sched.columns and 'away_score' in sched.columns:
        # Only filter if we have actual scores, not dummy NaN values
        if not sched["home_score"].isna().all():
            sched = sched[(~sched["home_score"].isna()) & (~sched["away_score"].isna())]
    
    # Derive game_date for ordering (if available)
    if 'gameday' in sched.columns:
        sched["game_date"] = pd.to_datetime(sched["gameday"])
    else:
        # Create dummy dates if not available
        sched["game_date"] = pd.to_datetime(sched['season'].astype(str) + "-01-01")
    
    # Keep needed columns
    cols = [
        "game_id", "season", "week", "game_date",
        "home_team", "away_team", "home_score", "away_score",
        "spread_line", "total_line"
    ]
    
    # Only keep columns that exist
    available_cols = [col for col in cols if col in sched.columns]
    sched = sched[available_cols]
    
    return sched


# -----------------------------
# Feature Engineering
# -----------------------------

def build_team_game_rows(pbp: pd.DataFrame) -> pd.DataFrame:
    """
    Create per-team, per-game aggregates from play-by-play.
    We compute offensive and defensive EPA/play, success rates, pass rates, etc.

    Returns: DataFrame with one row per (game_id, team) with offensive/defensive features.
    """
    # Basic filters: non-NA epa, meaningful plays
    df = pbp.copy()

    # Harmonize booleans
    for col in ["pass", "rush", "qb_scramble", "qb_hit", "sack", "penalty", "accepted_penalty"]:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    # Success = EPA > 0
    df["success"] = (df["epa"] > 0).astype(int)

    # Early-down flag
    df["early_down"] = df["down"].isin([1, 2]).astype(int)

    # Explosive flag: yardage-based fallback (air_yards missing sometimes)
    # Define explosive as >= 15 yards gained (you can tweak)
    df["explosive"] = (df["yards_gained"] >= 15).astype(int)

    # Special teams indicator by play_type
    st_types = {"punt", "kickoff", "field_goal", "extra_point", "qb_kneel", "qb_spike"}
    df["special_teams_play"] = df["play_type"].isin(st_types).astype(int)

    # --- Offensive aggregation (by posteam) ---
    off = (
        df.groupby(["game_id", "posteam"], dropna=False)
          .agg(
              plays_off=("play_id", "count"),
              epa_off=("epa", "mean"),
              success_off=("success", "mean"),
              explosiveness_off=("explosive", "mean"),
              pass_rate_off=("pass", "mean"),
              rush_rate_off=("rush", "mean"),
              early_down_pass_rate=("pass", lambda s: (s * df.loc[s.index, "early_down"]).sum() / max(1, df.loc[s.index, "early_down"].sum())),
              sacks_off=("sack", "sum"),
              penalties_off=("accepted_penalty", "sum"),
              st_epa_off=("epa", lambda s: s[df.loc[s.index, "special_teams_play"] == 1].mean() if (df.loc[s.index, "special_teams_play"] == 1).any() else 0.0),
          )
          .reset_index()
          .rename(columns={"posteam": "team"})
    )

    # --- Defensive aggregation (by defteam) ---
    # Here epa_def_allowed is opponent's offensive epa against this defense.
    deff = (
        df.groupby(["game_id", "defteam"], dropna=False)
          .agg(
              plays_def=("play_id", "count"),
              epa_def_allowed=("epa", "mean"),
              success_def_allowed=("success", "mean"),
              explosiveness_def_allowed=("explosive", "mean"),
              sacks_def=("sack", "sum"),     # sacks made (since sack is tied to the play regardless of posteam/defteam)
              penalties_def=("accepted_penalty", "sum"),
              st_epa_def=("epa", lambda s: s[df.loc[s.index, "special_teams_play"] == 1].mean() if (df.loc[s.index, "special_teams_play"] == 1).any() else 0.0),
          )
          .reset_index()
          .rename(columns={"defteam": "team"})
    )

    # Merge offense + defense on (game_id, team)
    team_game = pd.merge(off, deff, on=["game_id", "team"], how="outer")
    
    # Calculate net EPA (offensive EPA - defensive EPA allowed)
    team_game["net_epa"] = team_game["epa_off"] - team_game["epa_def_allowed"]
    
    # Calculate net success rate
    team_game["net_success_rate"] = team_game["success_off"] - team_game["success_def_allowed"]

    return team_game


def join_schedule(team_game: pd.DataFrame, sched: pd.DataFrame) -> pd.DataFrame:
    """
    Merge team-game features with schedule to get opponents, scores, spreads.
    We explode schedule to two rows per game: home and away, then attach features.
    """
    # Explode schedule into team-centric rows
    home_rows = sched.rename(columns={"home_team": "team", "away_team": "opp"}).copy()
    home_rows["is_home"] = 1
    away_rows = sched.rename(columns={"away_team": "team", "home_team": "opp"}).copy()
    away_rows["is_home"] = 0

    team_sched = pd.concat([home_rows, away_rows], ignore_index=True)

    # Compute team score and opponent score per row
    team_sched["team_score"] = np.where(team_sched["is_home"] == 1, team_sched["home_score"], team_sched["away_score"])
    team_sched["opp_score"] = np.where(team_sched["is_home"] == 1, team_sched["away_score"], team_sched["home_score"])

    # Team-specific spread line: nflfastR's spread_line is for HOME team (negative = favored)
    # So if team is home: team_line = spread_line
    # If team is away: team_line = -spread_line (opposite sign)
    team_sched["team_line"] = np.where(team_sched["is_home"] == 1, team_sched["spread_line"], -team_sched["spread_line"])

    # Join features
    x = pd.merge(team_sched, team_game, on=["game_id", "team"], how="left")

    # Basic extra context
    x["margin"] = x["team_score"] - x["opp_score"]

    # Define cover label: 1 if team margin + team_line > 0; push excluded (labeled 0, or drop if you prefer)
    x["cover_label"] = (x["margin"] + x["team_line"] > 0).astype(int)
    x["push"] = (x["margin"] + x["team_line"] == 0).astype(int)

    # Keep only rows with features present (you may drop fewer cols as needed)
    x = x.dropna(subset=["epa_off", "epa_def_allowed"])

    return x


def add_rolling_features(team_game_sched: pd.DataFrame, windows: Tuple[int, ...] = (3, 5)) -> pd.DataFrame:
    """
    For each team-season, compute rolling means of selected features over prior games.
    """
    df = team_game_sched.copy()

    df = df.sort_values(["team", "season", "game_date"]).reset_index(drop=True)

    feature_cols = [
        "net_epa", "net_success_rate", "epa_off", "success_off", "explosiveness_off", "pass_rate_off", "rush_rate_off",
        "early_down_pass_rate", "sacks_off", "penalties_off", "st_epa_off",
        "epa_def_allowed", "success_def_allowed", "explosiveness_def_allowed",
        "sacks_def", "penalties_def", "st_epa_def"
    ]

    for w in windows:
        group = df.groupby(["team", "season"], group_keys=False)
        rolled = group[feature_cols].apply(lambda g: g.shift(1).rolling(w, min_periods=1).mean())
        rolled = rolled.add_suffix(f"_roll{w}")
        for col in rolled.columns:
            df[col] = rolled[col]

    # Optional opponent rolling features (last w games for opponent entering matchup)
    for w in windows:
        opp_cols = [f"{c}_roll{w}" for c in feature_cols]
        # Merge opponent features by aligning opponent row on same game
        opp = df[["game_id", "team"] + opp_cols].copy()
        opp = opp.rename(columns={c: f"opp_{c}" for c in opp_cols})
        df = pd.merge(df, opp, left_on=["game_id", "opp"], right_on=["game_id", "team"], how="left", suffixes=("", "_drop"))
        df = df.drop(columns=["team_drop"], errors="ignore")

    # Drop first-game rows where no history exists? We'll keep them; model can learn NA handling if imputed.
    df = df.reset_index(drop=True)
    return df


def finalize_training_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean/impute and select final features for modeling.
    """
    # Example: simple imputation (median) for rolling features that are NA at early season
    feature_cols = [c for c in df.columns if c.endswith(("roll3", "roll5"))]
    for col in feature_cols:
        df[col] = df[col].fillna(df[col].median())

    # Core numeric features
    base_cols = [
        "is_home", "team_line", "total_line"
    ]

    X_cols = base_cols + feature_cols
    y_col = "cover_label"

    # Drop pushes to focus on binary cover/not-cover (optional)
    out = df[df["push"] == 0].copy()

    # Keep only rows with all needed features
    out = out.dropna(subset=X_cols + [y_col])

    return out, X_cols, y_col


def create_underdog_model(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a model focused on underdog teams and their EPA-based cover probability.
    """
    # Identify underdog teams (positive team_line means they're underdogs)
    underdog_df = df[df["team_line"] > 0].copy()
    
    print(f"Found {len(underdog_df)} underdog team-game observations")
    
    # Add underdog-specific features
    underdog_df["underdog_margin"] = underdog_df["team_line"]  # How much of an underdog
    underdog_df["is_underdog"] = 1
    
    # EPA-based features for underdogs (prioritize net EPA)
    epa_features = [
        "net_epa", "net_success_rate", "epa_off", "epa_def_allowed", "success_off", "success_def_allowed",
        "explosiveness_off", "explosiveness_def_allowed", "pass_rate_off",
        "sacks_off", "sacks_def", "penalties_off", "penalties_def"
    ]
    
    # Rolling EPA features
    rolling_features = [c for c in underdog_df.columns if c.endswith(("roll3", "roll5"))]
    
    # Underdog-specific feature set (prioritize net EPA)
    underdog_features = [
        "is_home", "underdog_margin", "total_line",
        "net_epa", "net_success_rate", "epa_off", "epa_def_allowed", "success_off", "success_def_allowed",
        "explosiveness_off", "explosiveness_def_allowed", "pass_rate_off",
        "sacks_off", "sacks_def", "penalties_off", "penalties_def"
    ] + rolling_features
    
    # Add opponent EPA features (how good is the opponent they're facing)
    opp_epa_features = [f"opp_{f}" for f in rolling_features if f.startswith(("epa_", "success_", "explosiveness_"))]
    underdog_features.extend(opp_epa_features)
    
    # Filter to available features
    available_features = [f for f in underdog_features if f in underdog_df.columns]
    
    # Clean data
    underdog_clean = underdog_df.dropna(subset=available_features + ["cover_label"]).copy()
    
    print(f"Clean underdog dataset: {len(underdog_clean)} observations")
    print(f"Cover rate for underdogs: {underdog_clean['cover_label'].mean():.3f}")
    
    return underdog_clean, available_features, "cover_label"


def train_underdog_model(df: pd.DataFrame, X_cols: List[str], y_col: str, test_seasons: Tuple[int, ...] = (2023, 2024)):
    """
    Train a model specifically for underdog spread coverage prediction.
    """
    # Split data
    train_df = df[~df["season"].isin(test_seasons)].copy()
    test_df = df[df["season"].isin(test_seasons)].copy()
    
    if len(train_df) == 0 or len(test_df) == 0:
        print("Warning: No test/train split possible with current data")
        return None, None, None
    
    X_train = train_df[X_cols].values
    y_train = train_df[y_col].values
    X_test = test_df[X_cols].values
    y_test = test_df[y_col].values
    
    # Train logistic regression
    clf = LogisticRegression(max_iter=2000, random_state=42)
    clf.fit(X_train, y_train)
    
    # Predictions
    p_train = clf.predict_proba(X_train)[:, 1]
    p_test = clf.predict_proba(X_test)[:, 1]
    
    # Metrics
    metrics = {
        "train_logloss": float(log_loss(y_train, p_train)),
        "test_logloss": float(log_loss(y_test, p_test)),
        "train_brier": float(brier_score_loss(y_train, p_train)),
        "test_brier": float(brier_score_loss(y_test, p_test)),
        "train_acc@0.5": float(accuracy_score(y_train, (p_train >= 0.5).astype(int))),
        "test_acc@0.5": float(accuracy_score(y_test, (p_test >= 0.5).astype(int))),
        "n_train": int(len(train_df)),
        "n_test": int(len(test_df)),
        "underdog_cover_rate": float(y_test.mean()),
    }
    
    print("Underdog Model Metrics:", metrics)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X_cols,
        'coefficient': clf.coef_[0],
        'abs_coefficient': np.abs(clf.coef_[0])
    }).sort_values('abs_coefficient', ascending=False)
    
    print("\nTop EPA Features for Underdog Cover Prediction:")
    print(feature_importance.head(10))
    
    # Calibration plot
    prob_true, prob_pred = calibration_curve(y_test, p_test, n_bins=10, strategy="quantile")
    plt.figure(figsize=(8, 6))
    plt.plot(prob_pred, prob_true, marker="o", label="Underdog Model")
    plt.plot([0, 1], [0, 1], linestyle="--", label="Perfect Calibration")
    plt.title("Underdog Cover Probability Calibration")
    plt.xlabel("Predicted Probability")
    plt.ylabel("Empirical Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig("underdog_calibration_plot.png")
    print("Saved underdog_calibration_plot.png")
    
    return clf, metrics, test_df.assign(pred=p_test)


# -----------------------------
# Modeling & Evaluation
# -----------------------------

def train_and_evaluate(df: pd.DataFrame, X_cols: List[str], y_col: str, test_seasons: Tuple[int, ...] = (2023, 2024)):
    """
    Train on seasons not in test_seasons, test on test_seasons.
    """
    train_df = df[~df["season"].isin(test_seasons)].copy()
    test_df = df[df["season"].isin(test_seasons)].copy()

    X_train = train_df[X_cols].values
    y_train = train_df[y_col].values
    X_test = test_df[X_cols].values
    y_test = test_df[y_col].values

    clf = LogisticRegression(max_iter=2000)
    clf.fit(X_train, y_train)

    p_train = clf.predict_proba(X_train)[:, 1]
    p_test = clf.predict_proba(X_test)[:, 1]

    metrics = {
        "train_logloss": float(log_loss(y_train, p_train)),
        "test_logloss": float(log_loss(y_test, p_test)),
        "train_brier": float(brier_score_loss(y_train, p_train)),
        "test_brier": float(brier_score_loss(y_test, p_test)),
        "train_acc@0.5": float(accuracy_score(y_train, (p_train >= 0.5).astype(int))),
        "test_acc@0.5": float(accuracy_score(y_test, (p_test >= 0.5).astype(int))),
        "n_train": int(len(train_df)),
        "n_test": int(len(test_df)),
    }

    print("Metrics:", metrics)

    # Calibration plot
    prob_true, prob_pred = calibration_curve(y_test, p_test, n_bins=10, strategy="quantile")
    plt.figure(figsize=(6, 6))
    plt.plot(prob_pred, prob_true, marker="o")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.title("Calibration (Test)")
    plt.xlabel("Predicted probability")
    plt.ylabel("Empirical frequency")
    plt.tight_layout()
    plt.savefig("calibration_plot.png")
    print("Saved calibration_plot.png")

    return clf, metrics, test_df.assign(pred=p_test)


# -----------------------------
# Orchestration
# -----------------------------

def main():
    print("=== Loading data ===")
    pbp = load_pbp_for_seasons(SEASONS)
    sched = load_schedule_with_lines(SEASONS)

    print("=== Building team-game features ===")
    team_game = build_team_game_rows(pbp)

    print("=== Joining schedule and labeling ===")
    df = join_schedule(team_game, sched)

    print("=== Adding rolling features ===")
    df_roll = add_rolling_features(df, windows=(3, 5))

    print("=== Finalizing training table ===")
    model_df, X_cols, y_col = finalize_training_table(df_roll)
    print(f"Feature count: {len(X_cols)} | Rows: {len(model_df)}")

    # Persist features for inspection
    model_df.to_csv(SAVE_FEATURES_CSV, index=False)
    print(f"Saved features to {SAVE_FEATURES_CSV}")

    print("=== Training & evaluation ===")
    clf, metrics, test_preds = train_and_evaluate(model_df, X_cols, y_col, test_seasons=(2023, 2024))

    # Save test predictions for inspection
    test_preds_out = test_preds[["season", "week", "team", "opp", "is_home", "team_line", "margin", "cover_label", "pred"]].copy()
    test_preds_out.to_csv("test_predictions.csv", index=False)
    print("Saved test_predictions.csv")

    print("\n" + "="*60)
    print("=== UNDERDOG EPA COVER MODEL ===")
    print("="*60)
    
    # Create underdog-focused model
    underdog_df, underdog_features, underdog_y = create_underdog_model(df_roll)
    
    if len(underdog_df) > 0:
        print("=== Training Underdog Model ===")
        underdog_clf, underdog_metrics, underdog_preds = train_underdog_model(
            underdog_df, underdog_features, underdog_y, test_seasons=(2023, 2024)
        )
        
        if underdog_clf is not None:
            # Save underdog predictions
            underdog_preds_out = underdog_preds[["season", "week", "team", "opp", "is_home", "team_line", "underdog_margin", "cover_label", "pred"]].copy()
            underdog_preds_out.to_csv("underdog_predictions.csv", index=False)
            print("Saved underdog_predictions.csv")
            
            # Save underdog model
            try:
                import pickle
                with open("underdog_model.pkl", "wb") as f:
                    pickle.dump({"model": underdog_clf, "features": underdog_features}, f)
                print("Saved underdog_model.pkl")
            except Exception as e:
                print(f"Could not save underdog model: {e}")
    else:
        print("No underdog data available for modeling")

    # Optional: save main model (pickle). Commented out by default.
    try:
        import pickle
        with open(SAVE_MODEL, "wb") as f:
            pickle.dump({"model": clf, "features": X_cols}, f)
        print(f"Saved model to {SAVE_MODEL}")
    except Exception as e:
        print(f"Could not save model: {e}")


if __name__ == "__main__":
    # For reproducibility in demos (you can remove this line in real use)
    np.random.seed(42)
    main()
