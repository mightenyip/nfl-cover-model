# NFL Cover Model - Underdog Spread Analysis

A comprehensive analysis tool for predicting NFL underdog performance against the spread using Expected Points Added (EPA) metrics and opponent defensive analysis.

## 🎯 Key Findings

### Net EPA is the Most Comprehensive Team Strength Metric
- **Net EPA** (offensive EPA - defensive EPA allowed) provides better predictive power than separate EPA features
- **Real NFL data validation**: Tested on 1,000 matchups based on 2023-2024 team performance (89,019 plays)
- **Net EPA differential** is the most important predictive feature
- **Top teams by Net EPA**: Ravens (+0.156), Bills (+0.134), Lions (+0.123), Packers (+0.079)

### Opponent Defensive EPA is the #1 Predictor
- **Perfect correlation** (r = 1.000) between underdog offensive EPA and opponent defensive EPA allowed
- **Underdogs vs WEAK defenses**: 75% cover rate
- **Underdogs vs STRONG defenses**: 25% cover rate
- **The matchup matters more than the underdog's inherent offensive ability**

## 📁 Repository Structure

```
nfl-cover-model/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── nfl_cover_model_starter.py         # Main analysis script
├── week1/                             # Week 1 2025 analysis
│   ├── week1_2025_odds.csv           # Week 1 odds and spreads
│   └── week1_2025_results_analysis.md # Week 1 results and EPA analysis
├── week2/                             # Week 2 2025 predictions
│   ├── week2_2025_odds.csv           # Week 2 odds and spreads
│   ├── week2_2025_predictions_analysis.md # Week 2 predictions analysis
│   ├── week2_underdog_predictions.csv # Week 2 predictions (original)
│   ├── week2_underdog_predictions_updated.csv # Week 2 predictions (updated)
│   ├── week2_predictions.py          # Week 2 predictions script (original)
│   └── week2_predictions_updated.py  # Week 2 predictions script (updated)
└── images/                            # Data files
    └── play_by_play_2025.parquet     # NFL play-by-play data
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Week 1 Analysis
```bash
python3 nfl_cover_model_starter.py
```

### 3. Generate Week 2 Predictions
```bash
cd week2
python3 week2_predictions_updated.py
```

## 📊 Analysis Results

### Week 1 2025 Results
- **Total underdogs**: 16
- **Underdogs who covered**: 8 (50.0%)
- **Home underdogs**: 50.0% cover rate
- **Away underdogs**: 50.0% cover rate

### Week 2 2025 Results
- **Total underdogs**: 16
- **Underdogs who covered**: 7 (43.8%)
- **Model spread accuracy**: 43.8% (worse than random)
- **Model outright accuracy**: 31.2%

## 🎯 Week 2 2025 Underdog Cover Predictions

### Complete Week 2 Predictions (Updated with Net EPA)

| Game | Underdog | Spread | Net EPA Diff | Opponent Defense | Expected Cover Rate | Confidence |
|------|----------|--------|--------------|------------------|-------------------|------------|
| **Chargers at Raiders** | Raiders | +3.5 | -0.131 | WEAK (+0.131 EPA) | **80.3%** | HIGH |
| **Bills at Jets** | Jets | +6.5 | -0.085 | WEAK (+0.340 EPA) | **77.8%** | HIGH |
| **Eagles at Chiefs** | Chiefs | +0.5 | +0.083 | WEAK (+0.139 EPA) | **74.9%** | HIGH |
| **Bears at Lions** | Bears | +5.5 | -0.192 | AVERAGE (0.000 EPA) | 52.4% | MEDIUM |
| **Browns at Ravens** | Browns | +11.5 | -0.114 | AVERAGE (0.000 EPA) | 51.5% | MEDIUM |
| **Buccaneers at Texans** | Buccaneers | +2.5 | -0.046 | AVERAGE (0.000 EPA) | 50.7% | MEDIUM |
| **Jaguars at Bengals** | Jaguars | +3.5 | +0.000 | AVERAGE (0.000 EPA) | 50.0% | MEDIUM |
| **Patriots at Dolphins** | Patriots | +1.5 | +0.000 | AVERAGE (0.000 EPA) | 50.0% | MEDIUM |
| **49ers at Saints** | Saints | +4.5 | +0.107 | AVERAGE (0.000 EPA) | 49.3% | MEDIUM |
| **Falcons at Vikings** | Falcons | +4.5 | +0.065 | AVERAGE (0.000 EPA) | 48.4% | MEDIUM |
| **Seahawks at Steelers** | Seahawks | +3.0 | +0.094 | AVERAGE (0.000 EPA) | 47.6% | MEDIUM |
| **Giants at Cowboys** | Giants | +5.5 | +0.153 | AVERAGE (0.000 EPA) | 45.9% | MEDIUM |
| **Panthers at Cardinals** | Panthers | +6.5 | +0.197 | AVERAGE (0.000 EPA) | 45.1% | MEDIUM |
| **Broncos at Colts** | Colts | +2.5 | -0.279 | STRONG (-0.219 EPA) | 35.3% | LOW |
| **Commanders at Packers** | Commanders | +3.5 | +0.000 | STRONG (-0.054 EPA) | 25.0% | LOW |
| **Rams at Titans** | Titans | +5.5 | +0.109 | STRONG (-0.121 EPA) | 24.3% | LOW |

### 🎯 High Confidence Picks (vs WEAK defenses - 75%+ expected)
1. **Jets +6.5 vs Bills** (77.3% expected) - Bills allowed +0.340 defensive EPA
2. **Chiefs +0.5 vs Eagles** (77.3% expected) - Eagles allowed +0.139 defensive EPA
3. **Raiders +3.5 vs Chargers** (76.1% expected) - Chargers allowed +0.131 defensive EPA

### ❌ Avoid These (vs STRONG defenses - 25% expected)
1. **Colts +2.5 vs Broncos** (29.9% expected) - Broncos allowed -0.219 defensive EPA
2. **Titans +5.5 vs Rams** (24.5% expected) - Rams allowed -0.121 defensive EPA
3. **Commanders +3.5 vs Packers** (24.2% expected) - Packers allowed -0.054 defensive EPA

## 🚨 Week 2 2025 Model Performance - MAJOR FAILURE

### Model Accuracy Results
The model performed **significantly worse than random chance** in Week 2:

- **Spread prediction accuracy**: 43.8% (7/16 correct) - **Worse than 50% random**
- **Outright prediction accuracy**: 31.2% (5/16 correct) - **Much worse than random**

### Confidence Level Performance (Completely Broken)
| Confidence Level | Games | Accuracy | Performance |
|------------------|-------|----------|-------------|
| **HIGH** | 3 | **0.0%** | Predicted 3 covers, got 0 - **Complete failure** |
| **MEDIUM** | 10 | **50.0%** | Exactly random chance |
| **LOW** | 3 | **66.7%** | Actually performed best |

### Key Model Failures

#### 1. **High Confidence Picks Were All Wrong**
- **Jets +6.5** (77.8% predicted) → Lost by 20, did NOT cover
- **Chiefs +0.5** (74.9% predicted) → Lost by 3, did NOT cover  
- **Raiders +3.5** (80.3% predicted) → Lost by 11, did NOT cover

#### 2. **EPA Metrics Were Not Predictive**
- Covered underdogs had **worse** net EPA (-0.109) than non-covered underdogs (-0.052)
- The core feature engineering completely failed

#### 3. **Opponent Defense Logic Partially Reversed**
- **WEAK defenses**: 0% cover rate (0/3) - Model predicted these would be good
- **STRONG defenses**: 66.7% cover rate (2/3) - Model predicted these would be bad
- **AVERAGE defenses**: 50% cover rate (5/10) - Only these performed as expected

### What This Means
The model's confidence calibration is **fundamentally broken**. You would have performed better by:
- **Betting AGAINST** the model's high-confidence picks
- **Betting ON** the model's low-confidence picks
- This is the **opposite** of what a good model should do

### Comparison: Week 1 vs Week 2
| Metric | Week 1 | Week 2 | Change |
|--------|--------|--------|--------|
| Model Accuracy | Good | 43.8% | **Major decline** |
| EPA Predictive Value | Strong | None | **Complete failure** |
| Confidence Calibration | Working | Broken | **Reversed** |
| Opponent Defense Logic | 75% vs 25% | 0% vs 67% | **Partially reversed** |

## 📈 Methodology

### EPA Analysis
- **Offensive EPA**: Points added by team's offense per play
- **Defensive EPA**: Points allowed by team's defense per play
- **Net EPA**: Offensive EPA - Defensive EPA allowed

### Prediction Model
1. **Opponent defensive EPA** (primary factor - 75% vs 25% cover rates)
2. **EPA differential** (secondary factor)
3. **Home field advantage** (minimal impact)
4. **Spread size** (larger underdogs tend to cover more)

## 🔍 Key Insights

### Week 1 Findings (Model Worked)
1. **Defense Quality Matters Most**: Underdogs facing weak defenses had 3x higher cover rate than those facing strong defenses
2. **Perfect Correlation**: Underdog offensive EPA perfectly correlated with opponent defensive EPA allowed
3. **Matchup Over Skill**: The opponent's defensive performance was more important than the underdog's offensive ability
4. **Realistic Cover Rates**: 50% overall cover rate provided a realistic baseline

### Week 2 Findings (Model Failed)
1. **Model Performance Collapsed**: 43.8% accuracy - worse than random chance
2. **Confidence Calibration Broken**: High confidence picks had 0% accuracy, low confidence had 66.7%
3. **EPA Metrics Not Predictive**: Covered underdogs had worse net EPA than non-covered underdogs
4. **Opponent Defense Logic Reversed**: Strong defenses favored underdogs (67% cover rate), weak defenses failed (0% cover rate)
5. **Model Would Perform Better Inverted**: Betting against high-confidence picks and for low-confidence picks

## 📋 Data Sources

- **Play-by-Play Data**: [nflverse GitHub repository](https://github.com/nflverse/nflverse-data/releases/tag/pbp) (2023-2024 seasons)
- **Odds Data**: Manual compilation from Week 1 and Week 2 spreads
- **Analysis Period**: Week 1 2025 results (model worked), Week 2 2025 results (model failed)
- **Validation Data**: 89,019 plays from 2023-2024 regular season (1,088 team-game observations)

## 🛠️ Technical Details

### Dependencies
- pandas: Data manipulation and analysis
- numpy: Numerical computations
- scipy: Statistical analysis
- pyarrow: Parquet file reading

### File Formats
- **CSV**: Odds data and predictions
- **Parquet**: Play-by-play data (efficient storage)
- **Markdown**: Analysis reports and documentation

## 📝 Usage Examples

### Generate Predictions
```python
from week2.week2_predictions_updated import make_week2_predictions
predictions = make_week2_predictions()
```

### Analyze Week 1 Results
```python
import pandas as pd
week1_results = pd.read_csv('week1/week1_2025_results_analysis.md')
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your analysis or improvements
4. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please ensure compliance with any applicable terms of service for data sources.

## 🔮 Future Enhancements

- [ ] Add more weeks of data
- [ ] Implement machine learning models
- [ ] Add real-time odds integration
- [ ] Create visualization dashboards
- [ ] Add historical performance tracking

---

**Disclaimer**: This analysis is for educational purposes only. Sports betting involves risk, and past performance does not guarantee future results.