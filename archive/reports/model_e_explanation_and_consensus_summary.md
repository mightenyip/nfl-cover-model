# Model E Explanation & Consensus Performance Summary

## 🤖 How Model E Works

**Model E: Advanced EPA Metrics (Pass/Rush Efficiency)**

Model E uses a simplified efficiency-based approach to predict whether the underdog will cover the spread.

### Methodology:

1. **Calculate Offensive Efficiency**
   - For both favorite and underdog teams:
   - `efficiency = (EPA/Pass + EPA/Rush) / 2`
   - This gives an average of pass and rush offensive efficiency

2. **Calculate Efficiency Difference**
   - `efficiency_diff = underdog_efficiency - favorite_efficiency`
   - Positive = underdog is more efficient
   - Negative = favorite is more efficient

3. **Prediction Logic** (Fixed thresholds):
   - **If efficiency_diff > 0.1**: Predict Cover (70% probability, HIGH confidence)
   - **If efficiency_diff > 0.05**: Predict Cover (60% probability, MEDIUM confidence)
   - **If efficiency_diff > -0.05**: Predict No Cover (55% probability, MEDIUM confidence)
   - **If efficiency_diff <= -0.05**: Predict No Cover (35% probability, HIGH confidence)

### Key Characteristics:

- **Simpler than Models A & B**: Uses only pass/rush efficiency comparison
- **Conservative**: Tends to predict "No Cover" more often (favoring favorites)
- **Fixed thresholds**: Doesn't adjust for spread size or other factors
- **Binary efficiency**: Averages pass and rush EPA equally (doesn't weight by play type)

### Example (Week 11 - Lions @ Eagles):

- **Favorite (Eagles)**: Pass EPA = 0.10, Rush EPA = -0.01 → Efficiency = 0.045
- **Underdog (Lions)**: Pass EPA = 0.26, Rush EPA = -0.01 → Efficiency = 0.125
- **Efficiency Diff**: 0.125 - 0.045 = 0.08
- **Prediction**: Cover (60% probability, MEDIUM confidence) ✅

---

## 📊 Consensus Performance Summary

### Week 10 Results (Most Recent Complete Week):

| Consensus Pair | Games Agreeing | Correct | Accuracy |
|----------------|----------------|---------|----------|
| **AB** (A & B) | 7 | 2 | **28.6%** |
| **AE** (A & E) | 8 | 4 | **50.0%** ⭐ |
| **BE** (B & E) | 5 | 2 | **40.0%** |

**Best Consensus: AE (50.0%)**

### Key Insights:

1. **Model E is conservative**: In Week 10, Model E predicted only 2 covers out of 14 games (14.3%), while Models A and B predicted 11 and 10 covers respectively.

2. **AE Consensus performs best**: When Models A and E agree, they achieved 50% accuracy (coin flip level), which is better than AB (28.6%) or BE (40.0%).

3. **Model E's conservative approach**: Model E's tendency to predict "No Cover" means:
   - When it agrees with Model A (AE consensus), it's often agreeing on "No Cover" predictions
   - This creates a more conservative consensus that may be more reliable

### Week 10 Detailed Breakdown:

**AE Consensus (8 games, 50% accuracy):**
- Giants @ Bears: No Cover ✅
- Ravens @ Vikings: No Cover ✅
- Jaguars @ Texans: No Cover ✅
- Cardinals @ Seahawks: No Cover ✅
- Steelers @ Chargers: No Cover ✅
- Eagles @ Packers: No Cover ❌
- Raiders @ Broncos: No Cover ❌
- Falcons @ Colts: No Cover ❌

**AB Consensus (7 games, 28.6% accuracy):**
- Bills @ Dolphins: Cover ✅
- Browns @ Jets: Cover ✅
- Patriots @ Buccaneers: Cover ✅
- Rams @ 49ers: Cover ❌
- Lions @ Commanders: Cover ❌
- Jaguars @ Texans: Cover ❌
- Cardinals @ Seahawks: Cover ❌

---

## 🎯 Recommendations:

1. **For conservative betting**: Use **AE consensus** - when Models A and E agree, you get 50% accuracy with a conservative approach

2. **For aggressive betting**: Use **AB consensus** - Models A and B tend to predict more covers, but accuracy was lower in Week 10 (28.6%)

3. **Model E's role**: Model E acts as a "reality check" - its conservative predictions help filter out overly optimistic cover predictions from Models A and B

4. **Best approach**: Consider using **unanimous picks (3/3)** when all three models agree - these are the highest confidence predictions

---

*Note: This analysis is based on Week 10 data. More weeks of data would provide better statistical significance.*

