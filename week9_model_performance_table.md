# Week 9 Model Performance Table

## Game-by-Game Results

| Game | Spread | Actual Result | Model A | Model B | Model C | Model D | Model E | Consensus |
|------|--------|---------------|---------|---------|---------|---------|---------|-----------|
| Ravens @ Dolphins | -7.5 | FAVORITE ✅ | UNDERDOG ❌ | FAVORITE ✅ | FAVORITE ✅ | UNDERDOG ❌ | FAVORITE ✅ | FAVORITE ✅ |
| Bears @ Bengals | -2.5 | FAVORITE ✅ | FAVORITE ✅ | UNDERDOG ❌ | FAVORITE ✅ | UNDERDOG ❌ | FAVORITE ✅ | FAVORITE ✅ |
| Vikings @ Lions | -8.5 | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ | FAVORITE ❌ | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ |
| Panthers @ Packers | -12.5 | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ | FAVORITE ❌ | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ |
| Chargers @ Titans | -9.5 | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ | FAVORITE ❌ | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ |
| Falcons @ Patriots | -5.5 | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ | FAVORITE ❌ | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ |
| 49ers @ Giants | -2.5 | FAVORITE ✅ | UNDERDOG ❌ | UNDERDOG ❌ | FAVORITE ✅ | UNDERDOG ❌ | FAVORITE ✅ | UNDERDOG ❌ |
| Colts @ Steelers | -3.0 | FAVORITE ✅ | FAVORITE ✅ | FAVORITE ✅ | FAVORITE ✅ | UNDERDOG ❌ | FAVORITE ✅ | FAVORITE ✅ |
| Broncos @ Texans | -1.5 | UNDERDOG ✅ | UNDERDOG ✅ | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ | UNDERDOG ✅ | UNDERDOG ✅ |
| Jaguars @ Raiders | -3.0 | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ | FAVORITE ❌ | UNDERDOG ✅ | FAVORITE ❌ | FAVORITE ❌ |
| Saints @ Rams | -13.5 | FAVORITE ✅ | FAVORITE ✅ | FAVORITE ✅ | FAVORITE ✅ | UNDERDOG ❌ | FAVORITE ✅ | FAVORITE ✅ |
| Chiefs @ Bills | -1.5 | UNDERDOG ✅ | UNDERDOG ✅ | UNDERDOG ✅ | FAVORITE ❌ | UNDERDOG ✅ | FAVORITE ❌ | UNDERDOG ✅ |
| Seahawks @ Commanders | -3.5 | FAVORITE ✅ | FAVORITE ✅ | UNDERDOG ❌ | FAVORITE ✅ | UNDERDOG ❌ | FAVORITE ✅ | FAVORITE ✅ |

**Legend:** ✅ = Correct | ❌ = Incorrect

---

## Summary Statistics

| Model | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| **Model E** | 7 | 13 | **53.8%** |
| **Consensus** | 7 | 13 | **53.8%** |
| Model A | 6 | 13 | 46.2% |
| Model C | 6 | 13 | 46.2% |
| Model D | 6 | 13 | 46.2% |
| Model B | 5 | 13 | 38.5% |

---

## Detailed Breakdown by Model

### Model A
- **Overall:** 6/13 (46.2%)
- **Underdog Predictions:** 4 (2 correct)
- **Favorite Predictions:** 9 (5 correct)

### Model B
- **Overall:** 5/13 (38.5%)
- **Underdog Predictions:** 5 (2 correct)
- **Favorite Predictions:** 8 (5 correct)

### Model C
- **Overall:** 6/13 (46.2%)
- **Underdog Predictions:** 0 (0 correct) - *Always predicted favorites*
- **Favorite Predictions:** 13 (7 correct)

### Model D
- **Overall:** 6/13 (46.2%)
- **Underdog Predictions:** 12 (6 correct) - *Almost always predicted underdogs*
- **Favorite Predictions:** 1 (1 correct)
- **Key Strength:** Only model to correctly predict 5 underdog covers (Vikings, Panthers, Chargers, Falcons, Jaguars)

### Model E
- **Overall:** 7/13 (53.8%) ⭐ **BEST**
- **Underdog Predictions:** 1 (1 correct)
- **Favorite Predictions:** 12 (6 correct)

### Consensus
- **Overall:** 7/13 (53.8%) ⭐ **BEST** (tied with Model E)
- **Underdog Predictions:** 3 (2 correct)
- **Favorite Predictions:** 10 (5 correct)

---

## Key Observations

1. **Model D** was the only model to correctly predict the 5 major underdog upsets:
   - Vikings @ Lions (MIN covered +8.5)
   - Panthers @ Packers (CAR covered +12.5)
   - Chargers @ Titans (TEN covered +9.5)
   - Falcons @ Patriots (ATL covered +5.5)
   - Jaguars @ Raiders (LV covered +3.0)

2. **Model C** never predicted an underdog cover (0/13), but still achieved 46.2% accuracy by correctly predicting 7 favorite covers.

3. **Model E** achieved the best overall accuracy (53.8%) with a balanced approach, correctly predicting both favorite and underdog covers.

4. **Consensus model** tied Model E for best performance, demonstrating the value of combining multiple models.

5. **Model B** struggled the most, with only 38.5% accuracy, missing on both favorite and underdog predictions.

---

*Note: Cardinals @ Cowboys game pending (Monday Night Football)*

