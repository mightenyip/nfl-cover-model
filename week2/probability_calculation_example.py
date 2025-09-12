#!/usr/bin/env python3
"""
Example of how the model calculates cover probabilities
"""

import numpy as np

def logistic_function(z):
    """Logistic function: 1 / (1 + e^(-z))"""
    return 1 / (1 + np.exp(-z))

def example_calculation():
    """Show how the model calculates probabilities"""
    
    print("=== NFL Cover Model Probability Calculation Example ===")
    print()
    
    # Example: Raiders vs Chargers
    print("Example: Chargers at Raiders")
    print("Raiders are underdogs getting +3.5 points")
    print()
    
    # Hypothetical coefficients (these would be learned from training data)
    coefficients = {
        'intercept': -0.5,           # Base bias
        'is_home': 0.3,              # Home field advantage
        'net_epa': 2.0,              # Net EPA impact (strong predictor)
        'team_line': 0.1,            # Spread impact
        'opponent_def_epa': -1.5,    # Opponent defense impact
        'net_epa_roll3': 1.0,        # Recent form
        'total_line': 0.05           # Total points impact
    }
    
    # Raiders features (underdog perspective)
    raiders_features = {
        'is_home': 1,                # Raiders at home
        'net_epa': 0.131,            # Raiders net EPA
        'team_line': 3.5,            # Getting 3.5 points
        'opponent_def_epa': 0.131,   # Chargers defensive EPA allowed
        'net_epa_roll3': 0.131,      # Recent form (same as current)
        'total_line': 47.5           # Total points
    }
    
    print("Raiders Features:")
    for feature, value in raiders_features.items():
        print(f"  {feature}: {value}")
    print()
    
    # Calculate z (linear combination)
    z = coefficients['intercept']
    print("Calculating z (linear combination):")
    print(f"  z = {coefficients['intercept']:.3f}")  # intercept
    
    for feature, value in raiders_features.items():
        if feature in coefficients:
            contribution = coefficients[feature] * value
            z += contribution
            print(f"    + {coefficients[feature]:.3f} × {value} = {contribution:.3f}  # {feature}")
    
    print(f"  z = {z:.3f}")
    print()
    
    # Calculate probability
    probability = logistic_function(z)
    
    print("Calculating probability:")
    print(f"  probability = 1 / (1 + e^(-z))")
    print(f"  probability = 1 / (1 + e^(-{z:.3f}))")
    print(f"  probability = 1 / (1 + {np.exp(-z):.3f})")
    print(f"  probability = {probability:.3f} ({probability*100:.1f}%)")
    print()
    
    print("🎯 Model Prediction: Raiders have {:.1f}% chance to cover +3.5".format(probability*100))
    
    # Show what happens with different net EPA values
    print("\n" + "="*60)
    print("IMPACT OF NET EPA ON PROBABILITY")
    print("="*60)
    
    net_epa_values = [-0.2, -0.1, 0.0, 0.1, 0.2, 0.3]
    
    print(f"{'Net EPA':<10} {'Z Value':<10} {'Probability':<12} {'Cover %'}")
    print("-" * 45)
    
    for net_epa in net_epa_values:
        # Recalculate z with different net EPA
        z_new = z - (coefficients['net_epa'] * raiders_features['net_epa']) + (coefficients['net_epa'] * net_epa)
        prob_new = logistic_function(z_new)
        
        print(f"{net_epa:<10.1f} {z_new:<10.3f} {prob_new:<12.3f} {prob_new*100:<8.1f}%")
    
    print("\n💡 Key Insight: Net EPA has a HUGE impact on cover probability!")
    print("   A 0.1 increase in net EPA can change probability by 10-15%")

if __name__ == "__main__":
    example_calculation()
