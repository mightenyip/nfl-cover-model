# NFL Cover Model - Model Architecture

This directory contains different model approaches for NFL underdog spread predictions.

## 📁 Structure

```
models/
├── model_a/                    # Current proven model
│   ├── model_a_sumersports.py  # SumerSports EPA-based model
│   └── model_a_week3_predictions.csv  # Week 3 predictions
├── model_b/                    # New experimental model (TBD)
└── README.md                   # This file
```

## 🤖 Model A: SumerSports EPA Model

**Current Status**: Production Model  
**Methodology**: SumerSports EPA data with proven Week 2 methodology (81.2% accuracy)  
**Key Features**:
- Net EPA differential analysis
- Opponent defense quality assessment
- Spread-based adjustments
- Confidence level classification

**Performance**:
- Week 2: 81.2% accuracy (13/16 correct)
- Week 3: 31.3% accuracy (5/16 correct)

## 🤖 Model B: [To Be Designed]

**Status**: Experimental  
**Methodology**: TBD  
**Planned Features**: TBD

## 📊 Model Comparison

| Model | Week 2 Accuracy | Week 3 Accuracy | Methodology |
|-------|----------------|-----------------|-------------|
| Model A | 81.2% (13/16) | 31.3% (5/16) | SumerSports EPA |
| Model B | TBD | TBD | TBD |

## 🚀 Usage

### Run Model A:
```bash
cd models/model_a
python model_a_sumersports.py
```

### Run Model B:
```bash
cd models/model_b
python model_b_[name].py
```

## 📈 Future Enhancements

- [ ] Model B implementation
- [ ] Ensemble methods combining A + B
- [ ] Advanced feature engineering
- [ ] Machine learning approaches
- [ ] Real-time performance tracking
