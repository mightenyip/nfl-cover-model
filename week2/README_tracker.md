# Week 2 2025 Model Performance Tracker

This directory contains tools to track and analyze the performance of the NFL cover model for Week 2 2025 predictions.

## Files Overview

### Core Tracker Files
- **`week2_model_tracker.py`** - Main tracker class with analysis functions
- **`setup_week2_tracker.py`** - Setup script to create results template
- **`demo_tracker.py`** - Demo script showing how the tracker works

### Data Files
- **`week2_underdog_predictions_updated.csv`** - Model predictions for Week 2
- **`week2_results_template.csv`** - Template for recording actual game results
- **`week2_results_sample.csv`** - Sample data for demonstration

### Output Files (Generated)
- **`week2_model_performance.png`** - Visualizations of model performance
- **`week2_model_performance_report.md`** - Detailed markdown report
- **`week2_detailed_results.csv`** - Exported analysis data

## How to Use the Tracker

### Step 1: Setup (One-time)
```bash
python3 setup_week2_tracker.py
```
This creates `week2_results_template.csv` with all the games to track.

### Step 2: Record Game Results
Fill in the actual game results in `week2_results_template.csv`:

| Column | Description | Example |
|--------|-------------|---------|
| `actual_home_score` | Final home team score | `24` |
| `actual_away_score` | Final away team score | `21` |
| `actual_cover` | Did underdog cover? | `True` or `False` |
| `actual_winner` | Who won? | `home` or `away` |
| `actual_underdog_win` | Did underdog win outright? | `True` or `False` |
| `game_completed` | Is game finished? | `True` |
| `notes` | Any additional notes | `"Raiders covered +3.5"` |

### Step 3: Run Analysis
```bash
# Rename template to results file
mv week2_results_template.csv week2_results.csv

# Run the tracker
python3 week2_model_tracker.py
```

### Step 4: View Results
The tracker generates:
- **Visualizations**: `week2_model_performance.png`
- **Detailed Report**: `week2_model_performance_report.md`
- **Export Data**: `week2_detailed_results.csv`

## Demo Mode

To see how the tracker works with sample data:
```bash
python3 demo_tracker.py
```

## What the Tracker Measures

### 1. Spread Coverage Accuracy
- **Question**: Did the underdog cover the spread?
- **Model Prediction**: Based on cover_probability > 0.5
- **Actual Result**: Whether underdog actually covered

### 2. Outright Win Accuracy
- **Question**: Did the underdog win the game outright?
- **Model Prediction**: Based on cover_probability > 0.5
- **Actual Result**: Whether underdog actually won

### 3. Confidence Level Performance
- **HIGH Confidence**: Expected 75%+ accuracy
- **MEDIUM Confidence**: Expected 50% accuracy
- **LOW Confidence**: Expected 25% accuracy

## Sample Results

From the demo data:
- **Overall Spread Accuracy**: 52.9% (9/17 games)
- **High Confidence**: 100% (5/5 games) ✅
- **Medium Confidence**: 40% (4/10 games) ⚠️
- **Low Confidence**: 0% (0/2 games) ❌

## Key Insights

### Model Strengths
- High confidence predictions are very accurate
- The model correctly identifies strong underdog opportunities
- EPA-based features provide good predictive power

### Areas for Improvement
- Medium and low confidence predictions need work
- Model may be too conservative on some matchups
- Consider adjusting confidence thresholds

## Troubleshooting

### Common Issues
1. **"Could not load predictions"**: Make sure `week2_underdog_predictions_updated.csv` exists
2. **"No completed games"**: Set `game_completed = True` for finished games
3. **Column errors**: Check that all required columns are filled in

### Getting Help
- Check the demo script for examples
- Review the sample data format
- Ensure all games have `game_completed = True` before analysis

## Future Enhancements

Potential improvements to the tracker:
- Real-time score updates
- Automated result fetching
- Historical performance tracking
- Model comparison tools
- Betting ROI calculations

