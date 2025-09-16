# Corrected EPA Analysis - Week 1+2 2025

## Data Correction

**Previous Issue**: Our "Week 1+2" analysis was actually Week 1 data only, causing significant discrepancies.

**Resolution**: Successfully pulled latest data from [nflverse GitHub releases](https://github.com/nflverse/nflverse-data/releases/tag/pbp) which now includes both Week 1 and Week 2 games.

## Updated Data Summary

- **Total plays**: 5,527 (vs 2,738 previously)
- **Weeks included**: 1 and 2 (vs 1 only previously)
- **Games**: 32 total (16 per week)
- **Data source**: Latest nflverse release

## Bills EPA Correction

### Previous (Week 1 Only)
- **Defensive EPA allowed**: +0.340 per play
- **Context**: Terrible Week 1 performance vs Ravens

### Corrected (Week 1+2)
- **Defensive EPA allowed**: +0.098 per play
- **Context**: Improved significantly in Week 2
- **Net EPA**: +0.094 per play

This explains the discrepancy with online sources showing ~0.06 defensive EPA - they were using cumulative data through Week 2.

## Updated Team Rankings

### Top 10 Teams by Net EPA (Week 1+2)
| Rank | Team | Net EPA | Off EPA/Play | Def EPA/Play |
|------|------|---------|--------------|--------------|
| 1 | **Ravens** | +0.212 | +0.216 | +0.004 |
| 2 | **Colts** | +0.176 | +0.203 | +0.027 |
| 3 | **Packers** | +0.166 | +0.104 | -0.062 |
| 4 | **Falcons** | +0.143 | +0.011 | -0.132 |
| 5 | **Chargers** | +0.136 | +0.073 | -0.063 |
| 6 | **Bills** | +0.094 | +0.193 | +0.098 |
| 7 | **Raiders** | +0.092 | +0.082 | -0.010 |
| 8 | **Eagles** | +0.088 | +0.171 | +0.083 |
| 9 | **Steelers** | +0.085 | +0.209 | +0.124 |
| 10 | **Jaguars** | +0.080 | +0.090 | +0.010 |

### Bottom 10 Teams by Net EPA (Week 1+2)
| Rank | Team | Net EPA | Off EPA/Play | Def EPA/Play |
|------|------|---------|--------------|--------------|
| 23 | **Vikings** | -0.155 | -0.207 | -0.052 |
| 24 | **Jets** | -0.181 | +0.012 | +0.193 |
| 25 | **Browns** | -0.181 | -0.158 | +0.022 |
| 26 | **Bears** | -0.240 | -0.116 | +0.124 |
| 27 | **Dolphins** | -0.244 | -0.024 | +0.220 |

## Key Insights

### Major Improvers from Week 1 to Week 2
1. **Bills** - Defense improved from +0.340 to +0.098 EPA allowed
2. **Falcons** - Strong defensive performance in Week 2
3. **Packers** - Consistent performance across both weeks

### Teams Still Struggling
1. **Dolphins** - Terrible on both sides through 2 weeks
2. **Bears** - Major offensive and defensive issues
3. **Browns** - Offense struggling significantly

### Defensive Standouts (Low EPA Allowed)
1. **Falcons** (-0.132 EPA allowed per play)
2. **Packers** (-0.062 EPA allowed per play)
3. **Chargers** (-0.063 EPA allowed per play)

### Defensive Concerns (High EPA Allowed)
1. **Dolphins** (+0.220 EPA allowed per play)
2. **Jets** (+0.193 EPA allowed per play)
3. **Bears** (+0.124 EPA allowed per play)

## Implications for Model Performance

### Why Week 2 Model Failed
The model used **Week 1 EPA metrics** to predict Week 2 outcomes, but:
- **Bills defense improved** significantly (0.340 → 0.098)
- **Team performance changed** dramatically between weeks
- **EPA rankings shifted** substantially

### Updated Opponent Defense Rankings
**Strong Defenses (Target for underdog picks):**
1. Falcons (-0.132 EPA allowed)
2. Packers (-0.062 EPA allowed)
3. Chargers (-0.063 EPA allowed)

**Weak Defenses (Avoid for underdog picks):**
1. Dolphins (+0.220 EPA allowed)
2. Jets (+0.193 EPA allowed)
3. Bears (+0.124 EPA allowed)

## Data Files

- **Corrected EPA Data**: `corrected_team_epa_week1_week2.csv`
- **Source**: Latest nflverse release with Week 1+2 data
- **Generated**: 2025-01-27

## Conclusion

The corrected data shows that team performance varies significantly between weeks. The Week 2 model failure was largely due to using outdated Week 1 metrics. Future predictions should use the most recent cumulative EPA data available.

**Key Takeaway**: EPA metrics are dynamic and change week-to-week. Models need to be updated with the latest data to maintain accuracy.
