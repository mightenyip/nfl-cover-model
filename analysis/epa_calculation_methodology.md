# EPA (Expected Points Added) Calculation Methodology

## What is EPA?

**Expected Points Added (EPA)** is an advanced metric that measures the value of each play in a football game by quantifying how much a play changes a team's expected points on that drive.

## How EPA is Calculated from Play-by-Play Data

### Core Concept

EPA is based on the concept of **Expected Points (EP)** - the average number of points a team can expect to score given a specific game situation.

### Game Situation Variables

Expected Points are calculated based on:
1. **Field Position** (yard line)
2. **Down** (1st, 2nd, 3rd, 4th)
3. **Distance** (yards to go for first down)
4. **Time Remaining** (in certain models)

### Expected Points Framework

Historical data shows expected points values. For example:
- **1st & 10 at own 20-yard line:** ~0.5 expected points
- **1st & 10 at own 40-yard line:** ~1.5 expected points
- **1st & 10 at opponent 30-yard line:** ~4.0 expected points
- **1st & 10 at opponent 10-yard line:** ~6.0 expected points

### EPA Calculation Per Play

**EPA = EP (after play) - EP (before play)**

#### Example 1: Successful Play
- **Before Play:** 1st & 10 at own 25-yard line → EP = 0.8
- **After Play:** Completion for 15 yards → 1st & 10 at own 40-yard line → EP = 1.5
- **EPA = 1.5 - 0.8 = +0.7** (positive EPA, good play!)

#### Example 2: Unsuccessful Play
- **Before Play:** 2nd & 5 at own 45-yard line → EP = 2.0
- **After Play:** Incomplete pass → 3rd & 5 at own 45-yard line → EP = 1.4
- **EPA = 1.4 - 2.0 = -0.6** (negative EPA, bad play)

#### Example 3: Touchdown
- **Before Play:** 1st & 10 at opponent 15-yard line → EP = 5.5
- **After Play:** Touchdown → EP = 7.0 (actual points scored)
- **EPA = 7.0 - 5.5 = +1.5** (high positive EPA!)

## How We Calculate Team EPA Metrics

### Data Source
We use play-by-play data from **nflverse** (nfl_data_py package), which includes pre-calculated EPA values for every play.

### Our Calculations

```python
# For Offensive EPA per Play
offensive_epa = df.groupby('posteam').agg({
    'epa': 'mean'  # Average EPA when team has possession
})

# For Defensive EPA Allowed per Play  
defensive_epa = df.groupby('defteam').agg({
    'epa': 'mean'  # Average EPA when team is on defense
})

# Net EPA per Play
net_epa = offensive_epa - defensive_epa
```

### Key Metrics

1. **Offensive EPA per Play** (`epa_off_per_play`)
   - Average EPA when team has the ball
   - **Higher is better** (more points expected per play)
   - Top teams: Colts (+0.169), Bills (+0.152), Cowboys (+0.150)

2. **Defensive EPA Allowed per Play** (`epa_def_allowed_per_play`)
   - Average EPA allowed to opponents
   - **Lower (more negative) is better** (fewer points allowed)
   - Top defenses: Texans (-0.148), Vikings (-0.096), Lions (-0.057)

3. **Net EPA per Play** (`net_epa_per_play`)
   - Offensive EPA - Defensive EPA
   - Best overall measure of team quality
   - Top teams: Colts (+0.224), Lions (+0.186), Texans (+0.162)

## Why EPA is Superior to Traditional Stats

### 1. Context-Aware
- A 5-yard gain on 3rd & 3 is more valuable than on 3rd & 10
- EPA captures this; total yards don't

### 2. Accounts for Situation
- A 30-yard completion at your own 20 is different than at opponent's 20
- EPA values them appropriately based on scoring probability

### 3. Includes All Play Types
- Passing, rushing, penalties, turnovers all measured consistently
- Everything converted to common "expected points" currency

### 4. Predictive Power
- EPA is more predictive of future wins than yards or points
- Teams with higher EPA typically win more games

## Example from Our Data

### Indianapolis Colts (Best Offense)
- **Offensive EPA/Play:** +0.1686 (Rank #1)
- **Interpretation:** On average, each Colts offensive play increases their expected points by 0.17
- Over 60 plays per game, that's ~10 expected points above average

### Houston Texans (Best Defense)
- **Defensive EPA/Play:** -0.1477 (Rank #1)
- **Interpretation:** On average, each play against the Texans decreases opponent's expected points by 0.15
- Over 60 defensive plays per game, that's preventing ~9 expected points

### Cleveland Browns (Worst Offense)
- **Offensive EPA/Play:** -0.1599 (Rank #32)
- **Interpretation:** Each Browns play DECREASES their expected points by 0.16
- They're actively hurting their own scoring chances

## Success Rate

We also track **Success Rate** - the percentage of plays that are "successful":
- **1st down:** Gain 50%+ of yards needed
- **2nd down:** Gain 70%+ of yards needed  
- **3rd/4th down:** Gain 100% of yards needed (convert)

Success Rate complements EPA by showing consistency vs. big plays.

## How Model A Uses EPA

Model A incorporates EPA metrics in its predictions:

1. **Offensive Matchup Analysis**
   - Underdog's offensive EPA vs. Favorite's defensive EPA
   - Better matchup = higher cover probability

2. **Net EPA Differential**
   - Compares overall team quality (Net EPA)
   - Larger differential favors the better team

3. **Defense Quality Tiers**
   - STRONG: EPA allowed < -0.05 → Boosts underdog
   - AVERAGE: EPA allowed -0.05 to +0.10 → Slight boost
   - WEAK: EPA allowed > +0.10 → Hurts underdog

4. **Weighting**
   - EPA metrics combined with spread, home/away, and recent performance
   - Creates probability that underdog covers the spread

## Data Quality Notes

- EPA data through **Week 5 of 2024 season**
- Includes all regular season games (Weeks 1-5)
- Play-by-play data sourced from nflverse (official NFL statistics)
- Updated automatically from https://github.com/nflverse/nflverse-data
- Excludes special teams plays (kickoffs, punts) for cleaner offensive/defensive metrics

## Mathematical Note

EPA is a **zero-sum metric** across the league:
- Every positive EPA for offense = negative EPA for defense
- League average EPA should be ~0
- This makes it ideal for comparative analysis

