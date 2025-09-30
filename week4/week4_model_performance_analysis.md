# Week 4 Model Performance Analysis

## Actual Week 4 Results

| Game | Final Score | Underdog | Spread | Actual Cover | Winner |
|------|-------------|----------|--------|--------------|---------|
| SEA @ ARI | SEA 23 - ARI 20 | Cardinals +1.5 | 1.5 | ❌ No (ARI lost by 3) | Seahawks |
| MIN @ PIT | MIN 21 - PIT 24 | Steelers +2.5 | 2.5 | ✅ Yes (PIT won by 3) | Steelers |
| WAS @ ATL | WAS 27 - ATL 34 | Falcons +1.5 | 1.5 | ✅ Yes (ATL won by 7) | Falcons |
| NO @ BUF | NO 19 - BUF 31 | Saints +16.5 | 16.5 | ❌ No (NO lost by 12) | Bills |
| CLE @ DET | CLE 10 - DET 34 | Browns +8.5 | 8.5 | ❌ No (CLE lost by 24) | Lions |
| TEN @ HOU | TEN 0 - HOU 26 | Titans +7.0 | 7.0 | ❌ No (TEN lost by 26) | Texans |
| CAR @ NE | CAR 13 - NE 42 | Panthers +5.5 | 5.5 | ❌ No (CAR lost by 29) | Patriots |
| LAC @ NYG | LAC 18 - NYG 21 | Giants +6.5 | 6.5 | ✅ Yes (NYG won by 3) | Giants |
| PHI @ TB | PHI 31 - TB 25 | Buccaneers +3.5 | 3.5 | ❌ No (TB lost by 6) | Eagles |
| IND @ LAR | IND 20 - LAR 27 | Colts +3.5 | 3.5 | ❌ No (IND lost by 7) | Rams |
| JAX @ SF | JAC 26 - SF 21 | Jaguars +3.0 | 3.0 | ✅ Yes (JAC won by 5) | Jaguars |
| BAL @ KC | BAL 20 - KC 37 | Chiefs +2.5 | 2.5 | ❌ No (KC lost by 17) | Ravens |
| CHI @ LV | CHI 25 - LV 24 | Bears +1.5 | 1.5 | ✅ Yes (CHI won by 1) | Bears |
| GB @ DAL | GB 40 - DAL 40 | Cowboys +7.0 | 7.0 | ❌ No (DAL lost by 0) | Tie |
| NYJ @ MIA | NYJ 21 - MIA 27 | Jets +2.5 | 2.5 | ❌ No (NYJ lost by 6) | Dolphins |
| CIN @ DEN | CIN 3 - DEN 28 | Bengals +7.0 | 7.0 | ❌ No (CIN lost by 25) | Broncos |

## Week 4 Reality Summary
- **Total Games**: 16
- **Underdogs Covered**: 5 games (31.25%)
- **Favorites Covered**: 11 games (68.75%)
- **Outright Underdog Wins**: 4 games (25%)
- **Ties**: 1 game (6.25%)

## Model Performance Analysis

### Model A (SumerSports EPA)
| Prediction | Correct | Incorrect | Total |
|------------|---------|-----------|-------|
| Underdog Cover | 2 | 6 | 8 |
| Favorite Cover | 3 | 5 | 8 |
| **Overall** | **5** | **11** | **16** |

**Accuracy: 31.25% (5/16 correct)**

### Model B v2 (Matchup-Specific EPA)
| Prediction | Correct | Incorrect | Total |
|------------|---------|-----------|-------|
| Underdog Cover | 3 | 7 | 10 |
| Favorite Cover | 2 | 4 | 6 |
| **Overall** | **5** | **11** | **16** |

**Accuracy: 31.25% (5/16 correct)**

### Model C Updated (Spread Rules + ATS Trends)
| Prediction | Correct | Incorrect | Total |
|------------|---------|-----------|-------|
| Underdog Cover | 2 | 2 | 4 |
| Favorite Cover | 9 | 3 | 12 |
| **Overall** | **11** | **5** | **16** |

**Accuracy: 68.75% (11/16 correct)**

### Model D (Total Rules)
| Prediction | Correct | Incorrect | Total |
|------------|---------|-----------|-------|
| Underdog Cover | 2 | 8 | 10 |
| Favorite Cover | 9 | 3 | 12 |
| **Overall** | **11** | **5** | **16** |

**Accuracy: 68.75% (11/16 correct)**

## Model Performance Ranking

| Rank | Model | Accuracy | vs Reality | Key Insight |
|------|-------|----------|------------|-------------|
| **#1** | **Model C Updated** | **68.75%** | **+37.5%** | ⭐ **Best performer - correctly predicted favorite-heavy week** |
| **#1** | **Model D** | **68.75%** | **+37.5%** | ⭐ **Tied for best - total rules worked well** |
| **#3** | **Model A** | **31.25%** | **0%** | ❌ **Matched reality but wrong direction** |
| **#3** | **Model B v2** | **31.25%** | **0%** | ❌ **Heavy underdog bias was wrong** |

## Key Insights

### Week 4 Was a FAVORITE HEAVY Week
- **Reality**: Only 31.25% underdog cover rate (5/16)
- **Models A & B v2**: Predicted 50%+ underdog covers → **WRONG DIRECTION**
- **Models C & D**: Predicted 25-37.5% underdog covers → **CORRECT DIRECTION**

### Model C Updated & Model D Success
- **Model C Updated**: 68.75% accuracy by correctly identifying favorite trends
- **Model D**: 68.75% accuracy using total-based rules
- **Both models**: Predicted fewer underdog covers, matching the reality

### EPA Models Struggled
- **Model A**: 31.25% accuracy (matched reality rate but wrong picks)
- **Model B v2**: 31.25% accuracy (heavy underdog bias was costly)
- **Issue**: EPA models favored underdogs in a favorite-heavy week

### Notable Games
- **Steelers +2.5** ✅: MIN @ PIT (PIT won 24-21) - Both EPA models correct
- **Giants +6.5** ✅: LAC @ NYG (NYG won 21-18) - Both EPA models correct  
- **Jaguars +3.0** ✅: JAX @ SF (JAC won 26-21) - Both EPA models correct
- **Bears +1.5** ✅: CHI @ LV (CHI won 25-24) - Both EPA models correct
- **Falcons +1.5** ✅: WAS @ ATL (ATL won 34-27) - Only Model A correct

## Conclusion
Week 4 was a **favorite-heavy week** (68.75% favorite covers), and the **rule-based models (C & D) significantly outperformed** the EPA-based models by correctly identifying this trend. The EPA models' underdog bias proved costly in a week where favorites dominated.
