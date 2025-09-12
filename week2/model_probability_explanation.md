# How the NFL Cover Model Calculates Probabilities

## 🧮 **Model Architecture: Logistic Regression**

The model uses **Logistic Regression** from scikit-learn to predict cover probabilities.

### **📊 Step-by-Step Process:**

## 1. **Feature Engineering**
The model creates features for each team-game combination:

### **Core Features:**
- `is_home` - Home field advantage (1 = home, 0 = away)
- `team_line` - Spread from team's perspective
- `total_line` - Over/under total

### **EPA Features:**
- `net_epa` - Offensive EPA - Defensive EPA allowed
- `net_success_rate` - Offensive success rate - Defensive success rate allowed
- `epa_off` - Offensive EPA per play
- `epa_def_allowed` - Defensive EPA allowed per play
- `success_off` - Offensive success rate
- `success_def_allowed` - Defensive success rate allowed
- `explosiveness_off` - Offensive explosiveness
- `explosiveness_def_allowed` - Defensive explosiveness allowed
- `pass_rate_off` - Pass rate
- `sacks_off` - Sacks per game
- `sacks_def` - Sacks allowed per game
- `penalties_off` - Penalties per game
- `penalties_def` - Penalties allowed per game

### **Rolling Features:**
- `net_epa_roll3` - 3-game rolling average of net EPA
- `net_epa_roll5` - 5-game rolling average of net EPA
- `epa_off_roll3` - 3-game rolling average of offensive EPA
- `epa_off_roll5` - 5-game rolling average of offensive EPA
- And similar rolling features for all other metrics

## 2. **Training Data Creation**
For each team-game, the model creates a label:
- `cover_label = 1` if team margin + team_line > 0 (covered)
- `cover_label = 0` if team margin + team_line ≤ 0 (didn't cover)

## 3. **Model Training**
```python
clf = LogisticRegression(max_iter=2000, random_state=42)
clf.fit(X_train, y_train)
```

The model learns coefficients for each feature that best predict cover outcomes.

## 4. **Probability Calculation**

### **Logistic Regression Formula:**
```
z = β₀ + β₁×feature₁ + β₂×feature₂ + ... + βₙ×featureₙ
probability = 1 / (1 + e^(-z))
```

Where:
- `β₀` = intercept (bias term)
- `β₁, β₂, ..., βₙ` = learned coefficients for each feature
- `e` = Euler's number (≈2.718)
- `z` = linear combination of features

### **Example Calculation:**
For a team with:
- `is_home = 1` (home team)
- `net_epa = 0.131`
- `team_line = 3.5` (getting 3.5 points)
- Other features...

The model calculates:
```
z = β₀ + β₁×1 + β₂×0.131 + β₃×3.5 + ... + βₙ×featureₙ
probability = 1 / (1 + e^(-z))
```

## 5. **Prediction Process**
```python
p_test = clf.predict_proba(X_test)[:, 1]
```

This returns probabilities between 0 and 1, where:
- **0.0** = 0% chance to cover (certain not to cover)
- **0.5** = 50% chance to cover (coin flip)
- **1.0** = 100% chance to cover (certain to cover)

## 🔍 **Key Insights:**

### **Feature Importance:**
The model learns which features are most predictive:
- **Net EPA** is typically the strongest predictor
- **Home field advantage** provides a small boost
- **Rolling averages** capture recent form
- **Opponent defensive EPA** is crucial for underdogs

### **Probability Interpretation:**
- **> 0.7** = High confidence cover
- **0.5-0.7** = Medium confidence cover
- **< 0.5** = Low confidence cover (favorite likely covers)

### **Model Limitations:**
- Assumes linear relationships between features
- Doesn't account for injuries, weather, etc.
- Based only on EPA metrics from play-by-play data
- Trained on historical data (2023-2024)

## 🎯 **Why Some Predictions Seem Off:**

1. **Data Quality Issues**: Incorrect net EPA calculations
2. **Feature Engineering**: Missing important factors
3. **Model Assumptions**: Linear relationships may not hold
4. **Training Data**: Limited to 2 seasons of data
5. **Overfitting**: Model may be too complex for available data

The model is essentially learning patterns from historical games and applying them to new matchups based on EPA performance metrics.
