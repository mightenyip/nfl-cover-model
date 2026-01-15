# Model C: ATS Trends-Based Predictions

## Overview

Model C uses **Against The Spread (ATS) trends** to make predictions. It analyzes historical performance of different team categories (Away Favorites, Home Favorites, Home Dogs, etc.) and applies rules based on their success rates.

## Data Sources

### Master ATS Trends Data
- **File**: `data/ats_trends/master_ats_trends.csv`
- **Content**: All games from Week 1-7 with ATS results
- **Updated**: Automatically when new week data is added
- **Format**: 108 games with detailed ATS performance

### Key Metrics Tracked
- **Overall**: 49/108 underdog covers (45.4%)
- **Away Favorites**: 10/33 (30.3%) - **WEAKEST TREND**
- **Home Favorites**: 38/74 (51.4%) - **NEUTRAL**
- **Home Dogs**: 1/1 (100.0%) - **STRONGEST TREND**

## Model C Rules (Updated Weekly)

### Current Rules (Week 1-7 Data)

1. **Away Favorites (30.3% success)**
   - **Action**: FADE (bet against them)
   - **Confidence**: HIGH
   - **Probability**: 69.7% underdog covers
   - **Rule**: When away team is favorite, bet the underdog

2. **Home Favorites (51.4% success)**
   - **Action**: NEUTRAL
   - **Confidence**: LOW
   - **Probability**: 50.0% (no clear edge)
   - **Rule**: Use other factors for home favorites

3. **Home Dogs (100.0% success)**
   - **Action**: PICK (bet them)
   - **Confidence**: HIGH
   - **Probability**: 100.0% underdog covers
   - **Rule**: When home team is underdog, bet them

## Weekly Update Process

### 1. Add New Week Data
```bash
# Add new week results to master_ats_trends.csv
# Run the weekly ATS calculation script
python3 scripts/weekX_ats_manual_calculation.py
```

### 2. Update Model C Trends
```bash
# Run the Model C updater
python3 models/model_c/model_c_weekly_updater.py
```

### 3. Generate Predictions
```bash
# Model C will automatically generate predictions for the next week
# Based on current ATS trends
```

## Files Structure

```
models/model_c/
├── README.md                           # This file
├── model_c_weekly_updater.py          # Main updater script
├── model_c_updated_predictions.csv     # Latest predictions
└── ATS_TRENDS_WEEK5.md                # Historical trends documentation

data/
├── master_ats_trends.csv              # Master ATS data (Week 1-7)
├── combined_week1_week7_ats.csv        # Combined analysis
└── model_c_updated_trends.csv         # Current trends summary

scripts/
├── update_model_c_ats_trends.py       # Trends calculator
├── weekX_ats_manual_calculation.py    # Weekly ATS calculators
└── combined_week1_weekX_ats.py        # Combined analysis scripts
```

## How Model C Works

### 1. Data Collection
- Collects game results and odds for each week
- Calculates ATS performance (did underdog cover?)
- Categorizes games by team status (Away/Home, Favorite/Underdog)

### 2. Trend Analysis
- Calculates success rates for each category
- Identifies strongest and weakest trends
- Updates rules based on current performance

### 3. Prediction Generation
- Applies rules to upcoming games
- Assigns confidence levels (HIGH/MEDIUM/LOW)
- Generates probability estimates

## Current Performance (Week 1-7)

### Overall ATS Performance
- **Underdog Covers**: 49/108 (45.4%)
- **Favorite Covers**: 59/108 (54.6%)
- **Slight favorite bias**

### Week-by-Week Breakdown
- **Week 1**: 50.0% underdog covers
- **Week 2**: 43.8% underdog covers
- **Week 3**: 37.5% underdog covers
- **Week 4**: 43.8% underdog covers
- **Week 5**: 57.1% underdog covers
- **Week 6**: 60.0% underdog covers
- **Week 7**: 26.7% underdog covers

### Recent Trend (Week 5-7)
- **Recent 3 weeks**: 21/44 underdog covers (47.7%)
- **Balanced performance**

## Model C Advantages

1. **Data-Driven**: Based on real ATS performance
2. **Adaptive**: Updates weekly with new data
3. **Transparent**: Clear rules and confidence levels
4. **Historical**: Uses comprehensive historical data

## Model C Limitations

1. **Small Sample Sizes**: Some categories have limited data
2. **Week-to-Week Variance**: Performance can vary significantly
3. **Market Changes**: Trends may not persist
4. **Overfitting Risk**: Rules based on limited historical data

## Usage Instructions

### For Weekly Updates:
1. Add new week game results to `data/game_results/master_games_results_weekX.csv`
2. Run `scripts/weekX_ats_manual_calculation.py`
3. Run `models/model_c/model_c_weekly_updater.py`
4. Review predictions in `model_c_updated_predictions.csv`

### For Analysis:
1. Check `data/ats_trends/combined/combined_week1_weekX_ats.csv` for overall trends
2. Review `data/trends/model_c_updated_trends.csv` for current rules
3. Use `scripts/update_model_c_ats_trends.py` for detailed analysis

## Future Improvements

1. **Larger Sample Sizes**: Collect more historical data
2. **Advanced Analytics**: Add regression analysis
3. **Market Factors**: Include weather, injuries, etc.
4. **Machine Learning**: Implement ML-based trend detection

---

*Model C is updated weekly with the latest ATS trends to ensure accurate predictions.*
