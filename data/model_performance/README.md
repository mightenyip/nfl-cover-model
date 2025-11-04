# Model Performance Data Archive

This directory contains all model performance tracking data organized by week.

## Structure

- `cumulative_model_performance.csv` - Current cumulative performance across all weeks
- `historical/` - Archive of weekly performance snapshots
- `weekly/` - Individual week performance files

## Files

### Cumulative Performance
- **cumulative_model_performance.csv**: Aggregated performance across all weeks for all models (A, B, C, D, E, Consensus)

### Historical Archives
Snapshots of cumulative performance saved at key points:
- `cumulative_model_performance_week{X}_final.csv` - Final snapshot after each week

### Weekly Performance
Individual week analysis files:
- `week{X}_model_performance.csv` - Detailed performance breakdown for each week

## Model Performance Summary

**Last Updated:** After Week 9

| Model | Correct | Games | Accuracy |
|-------|---------|-------|----------|
| Model B | 73 | 134 | 54.5% |
| Model C | 73 | 134 | 54.5% |
| Model A | 70 | 134 | 52.2% |
| Model E | 20 | 42 | 47.6%* |
| Consensus | 32 | 57 | 56.1%* |
| Model D | 60 | 134 | 44.8% |

*Model E and Consensus have fewer games due to limited historical data

## Notes

- Model E predictions started from Week 1 (post-hoc)
- Consensus predictions available for Weeks 1, 2, 4, 6, 7, 8, 9
- All models have complete data for Weeks 1-9 except where noted

