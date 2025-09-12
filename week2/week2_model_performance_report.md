# Week 2 2025 Model Performance Report

Generated on: 2025-09-12 15:28:05

## Executive Summary

The model made predictions for 16 completed games in Week 2 2025.

### Overall Performance
- **Spread Coverage Accuracy**: 50.0% (8/16)
- **Outright Win Accuracy**: 56.2% (9/16)

### Performance by Confidence Level

| Confidence | Games | Accuracy | Correct |
|------------|-------|----------|---------|
| HIGH | 4 | 100.0% | 4 |
| MEDIUM | 10 | 40.0% | 4 |
| LOW | 2 | 0.0% | 0 |

## Detailed Game Results

| Game | Underdog | Favorite | Spread | Predicted Prob | Predicted | Actual Cover | Correct | Confidence |
|------|----------|----------|--------|----------------|-----------|--------------|---------|------------|
| Chargers at Raiders | Raiders | Chargers | 3.5 | 80.3% | Cover | Cover | ✓ | HIGH |
| Chargers at Raiders | Raiders | Chargers | 3.5 | 80.3% | Cover | Cover | ✓ | HIGH |
| Bills at Jets | Jets | Bills | 6.5 | 77.8% | Cover | Cover | ✓ | HIGH |
| Eagles at Chiefs | Chiefs | Eagles | 0.5 | 74.9% | Cover | Cover | ✓ | HIGH |
| Bears at Lions | Bears | Lions | 5.5 | 52.4% | Cover | No Cover | ✗ | MEDIUM |
| Browns at Ravens | Browns | Ravens | 11.5 | 51.5% | Cover | No Cover | ✗ | MEDIUM |
| Buccaneers at Texans | Buccaneers | Texans | 2.5 | 50.7% | Cover | Cover | ✓ | MEDIUM |
| Jaguars at Bengals | Jaguars | Bengals | 3.5 | 50.0% | No Cover | Cover | ✗ | MEDIUM |
| Patriots at Dolphins | Patriots | Dolphins | 1.5 | 50.0% | No Cover | Cover | ✗ | MEDIUM |
| 49ers at Saints | Saints | 49ers | 4.5 | 49.3% | No Cover | Cover | ✗ | MEDIUM |
| Falcons at Vikings | Falcons | Vikings | 4.5 | 48.4% | No Cover | No Cover | ✓ | MEDIUM |
| Seahawks at Steelers | Seahawks | Steelers | 3.0 | 47.6% | No Cover | Cover | ✗ | MEDIUM |
| Giants at Cowboys | Giants | Cowboys | 5.5 | 45.9% | No Cover | No Cover | ✓ | MEDIUM |
| Panthers at Cardinals | Panthers | Cardinals | 6.5 | 45.1% | No Cover | No Cover | ✓ | MEDIUM |
| Broncos at Colts | Colts | Broncos | 2.5 | 35.3% | No Cover | Cover | ✗ | LOW |
| Rams at Titans | Titans | Rams | 5.5 | 24.3% | No Cover | Cover | ✗ | LOW |

## Key Insights

### Model Strengths
- The model achieved 50.0% accuracy on spread predictions
- High confidence predictions had 100.0% accuracy
- The model correctly predicted 9 outright underdog wins

### Areas for Improvement
- Low confidence predictions had 0.0% accuracy
- The model missed 8 spread predictions

### Recommendations
1. **Focus on High Confidence Picks**: The model performs best on high confidence predictions
2. **Review Low Confidence Logic**: Low confidence predictions need improvement
3. **Monitor Opponent Defense**: Continue tracking opponent defensive EPA as a key predictor

## Methodology

This analysis compares model predictions against actual game results for:
- **Spread Coverage**: Whether the underdog covered the spread
- **Outright Wins**: Whether the underdog won the game outright
- **Confidence Levels**: Performance breakdown by prediction confidence

The model uses EPA-based features with a focus on opponent defensive performance as the primary predictor.

## Data Sources
- **Predictions**: week2_underdog_predictions_updated.csv
- **Results**: week2_results.csv
- **Analysis Date**: 2025-09-12
