# Model B EPA Data Update

## Update Information
- **Date:** October 7, 2025
- **Source:** [SumerSports.com](https://sumersports.com)
  - Offensive Data: https://sumersports.com/teams/offensive/
  - Defensive Data: https://sumersports.com/teams/defensive/
- **Last Updated by SumerSports:** 10-07-2025 11:02 AM EST

## What Changed

Model B uses **detailed EPA data** with pass/rush breakdowns for more nuanced predictions. The data has been updated with the latest statistics through Week 5 of the 2025 NFL season.

### Data Structure

Each team now has:
- **Offensive EPA per Play** - Overall offensive efficiency
- **Pass EPA** - Passing game efficiency
- **Rush EPA** - Running game efficiency  
- **Defensive EPA Allowed per Play** - Overall defensive efficiency
- **Pass Defense EPA** - Pass defense efficiency
- **Rush Defense EPA** - Run defense efficiency
- **Net EPA** - Overall team quality (Offense - Defense)

## Updated Rankings (as of Oct 7, 2025)

### 🔴 Top 5 Offenses (EPA/Play)
1. **Baltimore Ravens** - 0.21 (Elite passing: 0.28, Strong rushing: 0.12)
2. **Buffalo Bills** - 0.18 (Balanced: 0.23 pass, 0.15 rush)
3. **Indianapolis Colts** - 0.16 (Pass-heavy: 0.23 pass, 0.07 rush)
4. **Detroit Lions** - 0.15 (Elite passing: 0.30, Weak rushing: -0.02)
5. **Green Bay Packers** - 0.15 (Elite passing: 0.28, Average rushing: 0.0)

### 🛡️ Top 5 Defenses (EPA Allowed/Play - Lower is Better)
1. **Minnesota Vikings** - -0.13 (Elite pass D: -0.30, Weak rush D: 0.05)
2. **Houston Texans** - -0.12 (Strong pass D: -0.19, Elite rush D: -0.01)
3. **Detroit Lions** - -0.10 (Good pass D: -0.05, Elite rush D: -0.18)
4. **Denver Broncos** - -0.09 (Balanced: -0.07 pass, -0.11 rush)
5. **Indianapolis Colts** - -0.08 (Balanced: -0.09 pass, -0.06 rush)

### 📈 Top 5 Overall Teams (Net EPA)
1. **Detroit Lions** - 0.25 (Complete team on both sides)
2. **Indianapolis Colts** - 0.24 (Strong O, good D)
3. **Buffalo Bills** - 0.16 (Strong O, average D)
4. **Green Bay Packers** - 0.14 (Good O, average D)
5. **Kansas City Chiefs** - 0.13 (Good O, good D)

### 💀 Bottom 5 Teams (Net EPA)
28. **New York Jets** - -0.28 (Bad O: -0.13, Terrible D: 0.15)
29. **Dallas Cowboys** - -0.07 (Good O: 0.12, Terrible D: 0.19)
30. **Cincinnati Bengals** - -0.13 (Bad O: -0.02, Terrible D: 0.11)
31. **Baltimore Ravens** - -0.04 (Elite O: 0.21, but Worst D: 0.17) 🚩
32. **Miami Dolphins** - -0.18 (Average O: 0.05, Worst D: 0.23) 🚩

## Notable Insights

### 🏆 Complete Teams
- **Detroit Lions**: #4 offense, #3 defense = #1 overall
- **Indianapolis Colts**: #3 offense, #5 defense = #2 overall

### ⚠️ Unbalanced Teams
- **Baltimore Ravens**: Elite offense (#1) but worst defense (#32) = #27 overall
- **Minnesota Vikings**: Weak offense (#26) but best defense (#1) = #8 overall
- **Dallas Cowboys**: Good offense (#7) but worst-3 defense (#31) = #28 overall

### 🎯 Pass vs Rush Specialization

**Best Pass Offenses:**
1. Detroit Lions: 0.30
2. Green Bay Packers: 0.28
3. Baltimore Ravens: 0.28

**Best Rush Offenses:**
1. Buffalo Bills: 0.15
2. Washington Commanders: 0.13
3. Jacksonville Jaguars: 0.13

**Best Pass Defenses:**
1. Minnesota Vikings: -0.30 (Elite!)
2. Houston Texans: -0.19
3. Detroit Lions: -0.05

**Best Rush Defenses:**
1. Cleveland Browns: -0.22
2. Detroit Lions: -0.18
3. Seattle Seahawks: -0.18

## How Model B Uses This Data

Model B analyzes **matchup-specific** EPA:

1. **Pass Matchup Analysis**
   - Underdog's pass offense EPA vs. Favorite's pass defense EPA
   - Example: If Ravens (0.28 pass O) face Vikings (-0.30 pass D), it's a clash of strengths

2. **Rush Matchup Analysis**
   - Underdog's rush offense EPA vs. Favorite's rush defense EPA
   - Example: Bills (0.15 rush O) vs. Browns (-0.22 rush D) favors defense

3. **Overall Matchup**
   - Combined EPA differentials weighted by play type tendencies
   - Better matchups = higher cover probability for underdog

4. **Confidence Levels**
   - VERY_HIGH: EPA advantage > 0.25
   - HIGH: EPA advantage 0.15-0.25
   - MEDIUM: EPA advantage 0.05-0.15
   - LOW: EPA advantage 0.0-0.05
   - VERY_LOW: EPA disadvantage

## Comparison to Model A

| Aspect | Model A | Model B |
|--------|---------|---------|
| **Data Source** | SumerSports Overall EPA | SumerSports Pass/Rush Split |
| **Granularity** | Overall offense/defense | Pass vs Rush specific |
| **Analysis** | Team quality comparison | Matchup-specific analysis |
| **Strengths** | Simple, proven approach | Identifies favorable matchups |
| **Week 5 Accuracy** | 71.4% (10/14) | 71.4% (10/14) |

Both models performed identically in Week 5, but they approached predictions differently and agreed on only 71% of games.

## Changes from Previous Version

### Previous Data (Oct 3, 2025)
- Based on early Week 5 estimates
- Some teams had incomplete data

### New Data (Oct 7, 2025)
- Complete Week 5 results incorporated
- All 32 teams with full pass/rush breakdown
- More accurate defensive EPA (includes all Week 5 games)

### Notable Changes
- **Lions**: Net EPA increased from 0.20 to 0.25 (moved to #1 overall)
- **Vikings**: Defense improved to -0.13 (now #1 defense)
- **Ravens**: Defense worsened to 0.17 (concerns for future picks)

## Using This Data

To run predictions with updated data:

```bash
cd models/model_b
python3 model_b_v2_week6.py  # When Week 6 odds are available
```

The script automatically uses `detailed_epa_data.csv` which has been updated with this latest information.

## Sources & Citations

- **Offensive EPA Data**: [SumerSports Offensive Stats](https://sumersports.com/teams/offensive/)
- **Defensive EPA Data**: [SumerSports Defensive Stats](https://sumersports.com/teams/defensive/)
- **Last Updated**: October 7, 2025, 11:02 AM EST
- **Update Script**: `/scripts/update_sumersports_model_b_data.py`

## Next Steps

1. Monitor Model B's performance in Week 6 with updated data
2. Compare accuracy against Model A
3. Consider weighting adjustments based on Week 3-5 performance
4. Track if pass/rush splits provide predictive advantage

