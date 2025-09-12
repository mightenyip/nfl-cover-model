#!/usr/bin/env python3
"""
Week 2 2025 NFL Model Performance Tracker

This script tracks the performance of the NFL cover model for Week 2 2025,
monitoring both spread coverage predictions and outright win predictions.

Features:
- Tracks model predictions vs actual results
- Calculates accuracy metrics for spread coverage
- Calculates accuracy metrics for outright wins
- Provides detailed analysis and visualizations
- Exports results to CSV and markdown reports
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class Week2ModelTracker:
    def __init__(self):
        self.predictions_df = None
        self.results_df = None
        self.analysis_df = None
        
    def load_predictions(self):
        """Load the model predictions for Week 2"""
        predictions_path = "week2_underdog_predictions_updated.csv"
        
        if os.path.exists(predictions_path):
            self.predictions_df = pd.read_csv(predictions_path)
            print(f"Loaded predictions from {predictions_path}")
        else:
            print(f"Predictions file not found: {predictions_path}")
            return False
            
        return True
    
    def create_results_template(self):
        """Create a template for recording actual game results"""
        if self.predictions_df is None:
            print("Please load predictions first")
            return None
            
        # Create results template based on predictions
        results_template = self.predictions_df.copy()
        
        # Add columns for actual results
        results_template['actual_home_score'] = np.nan
        results_template['actual_away_score'] = np.nan
        results_template['actual_margin'] = np.nan
        results_template['actual_cover'] = np.nan
        results_template['actual_winner'] = np.nan
        results_template['actual_underdog_win'] = np.nan
        results_template['game_completed'] = False
        results_template['notes'] = ''
        
        # Save template
        results_template.to_csv("week2_results_template.csv", index=False)
        print("Created week2_results_template.csv - please fill in actual results")
        
        return results_template
    
    def load_results(self, results_file="week2_results.csv"):
        """Load actual game results"""
        if os.path.exists(results_file):
            self.results_df = pd.read_csv(results_file)
            print(f"Loaded results from {results_file}")
            return True
        else:
            print(f"Results file not found: {results_file}")
            print("Please create results file or use create_results_template()")
            return False
    
    def analyze_performance(self):
        """Analyze model performance against actual results"""
        if self.predictions_df is None or self.results_df is None:
            print("Please load both predictions and results first")
            return None
            
        # Merge predictions with results
        merge_columns = ['game', 'actual_home_score', 'actual_away_score', 
                        'actual_cover', 'actual_winner', 'actual_underdog_win', 
                        'game_completed', 'notes']
        
        # Add binary prediction columns if they exist
        if 'predicted_cover_binary' in self.results_df.columns:
            merge_columns.append('predicted_cover_binary')
        if 'predicted_winner' in self.results_df.columns:
            merge_columns.append('predicted_winner')
            
        self.analysis_df = pd.merge(
            self.predictions_df, 
            self.results_df[merge_columns], 
            on='game', 
            how='left'
        )
        
        # Filter to completed games only
        completed_games = self.analysis_df[self.analysis_df['game_completed'] == True].copy()
        
        if len(completed_games) == 0:
            print("No completed games found in results")
            return None
            
        # Calculate spread prediction accuracy
        spread_correct = (completed_games['cover_probability'] > 0.5) == completed_games['actual_cover']
        spread_accuracy = spread_correct.mean()
        
        # Calculate outright win prediction accuracy
        # For outright wins, we predict underdog wins when cover_probability > 0.5
        outright_correct = (completed_games['cover_probability'] > 0.5) == completed_games['actual_underdog_win']
        outright_accuracy = outright_correct.mean()
        
        # Calculate binary prediction accuracy if available
        binary_cover_accuracy = None
        winner_prediction_accuracy = None
        
        if 'predicted_cover_binary' in completed_games.columns:
            binary_cover_correct = (completed_games['predicted_cover_binary'] == 'Yes') == completed_games['actual_cover']
            binary_cover_accuracy = binary_cover_correct.mean()
            
        if 'predicted_winner' in completed_games.columns:
            # Handle both team names and home/away formats
            if completed_games['actual_winner'].isin(['home', 'away']).any():
                # Convert home/away to team names for comparison
                def convert_winner_to_team(row):
                    if row['actual_winner'] == 'home':
                        return row['home_team'] if 'home_team' in row else row['favorite']
                    elif row['actual_winner'] == 'away':
                        return row['away_team'] if 'away_team' in row else row['underdog']
                    return row['actual_winner']
                
                completed_games['actual_winner_team'] = completed_games.apply(convert_winner_to_team, axis=1)
                winner_correct = completed_games['predicted_winner'] == completed_games['actual_winner_team']
            else:
                # Direct team name comparison
                winner_correct = completed_games['predicted_winner'] == completed_games['actual_winner']
            winner_prediction_accuracy = winner_correct.mean()
        
        # Calculate confidence-based accuracy
        high_conf_games = completed_games[completed_games['confidence'] == 'HIGH']
        medium_conf_games = completed_games[completed_games['confidence'] == 'MEDIUM']
        low_conf_games = completed_games[completed_games['confidence'] == 'LOW']
        
        high_conf_accuracy = ((high_conf_games['cover_probability'] > 0.5) == high_conf_games['actual_cover']).mean() if len(high_conf_games) > 0 else np.nan
        medium_conf_accuracy = ((medium_conf_games['cover_probability'] > 0.5) == medium_conf_games['actual_cover']).mean() if len(medium_conf_games) > 0 else np.nan
        low_conf_accuracy = ((low_conf_games['cover_probability'] > 0.5) == low_conf_games['actual_cover']).mean() if len(low_conf_games) > 0 else np.nan
        
        # Create performance summary
        performance_summary = {
            'total_games': len(completed_games),
            'spread_accuracy': spread_accuracy,
            'outright_accuracy': outright_accuracy,
            'binary_cover_accuracy': binary_cover_accuracy,
            'winner_prediction_accuracy': winner_prediction_accuracy,
            'high_confidence_games': len(high_conf_games),
            'high_confidence_accuracy': high_conf_accuracy,
            'medium_confidence_games': len(medium_conf_games),
            'medium_confidence_accuracy': medium_conf_accuracy,
            'low_confidence_games': len(low_conf_games),
            'low_confidence_accuracy': low_conf_accuracy,
            'correct_spread_predictions': spread_correct.sum(),
            'correct_outright_predictions': outright_correct.sum()
        }
        
        return performance_summary, completed_games
    
    def create_visualizations(self, completed_games):
        """Create visualizations of model performance"""
        if completed_games is None or len(completed_games) == 0:
            print("No completed games to visualize")
            return
            
        # Set up the plotting style
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Week 2 2025 Model Performance Analysis', fontsize=16, fontweight='bold')
        
        # 1. Prediction vs Actual Cover
        ax1 = axes[0, 0]
        predicted_cover = (completed_games['cover_probability'] > 0.5).astype(int)
        actual_cover = completed_games['actual_cover'].astype(int)
        
        # Create confusion matrix
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(actual_cover, predicted_cover)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax1,
                   xticklabels=['Predicted No Cover', 'Predicted Cover'],
                   yticklabels=['Actual No Cover', 'Actual Cover'])
        ax1.set_title('Spread Coverage: Predicted vs Actual')
        ax1.set_xlabel('Predicted')
        ax1.set_ylabel('Actual')
        
        # 2. Confidence Level Performance
        ax2 = axes[0, 1]
        confidence_performance = []
        confidence_labels = []
        
        for conf in ['HIGH', 'MEDIUM', 'LOW']:
            conf_games = completed_games[completed_games['confidence'] == conf]
            if len(conf_games) > 0:
                accuracy = ((conf_games['cover_probability'] > 0.5) == conf_games['actual_cover']).mean()
                confidence_performance.append(accuracy)
                confidence_labels.append(f'{conf}\n({len(conf_games)} games)')
        
        bars = ax2.bar(confidence_labels, confidence_performance, 
                      color=['green', 'orange', 'red'], alpha=0.7)
        ax2.set_title('Accuracy by Confidence Level')
        ax2.set_ylabel('Accuracy Rate')
        ax2.set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, acc in zip(bars, confidence_performance):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{acc:.1%}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Predicted Probability vs Actual Outcome
        ax3 = axes[1, 0]
        colors = ['red' if not cover else 'green' for cover in completed_games['actual_cover']]
        ax3.scatter(completed_games['cover_probability'], 
                   completed_games['actual_cover'].astype(int),
                   c=colors, alpha=0.7, s=100)
        ax3.axvline(x=0.5, color='black', linestyle='--', alpha=0.5)
        ax3.set_xlabel('Predicted Cover Probability')
        ax3.set_ylabel('Actual Cover (1=Yes, 0=No)')
        ax3.set_title('Predicted Probability vs Actual Outcome')
        ax3.set_ylim(-0.1, 1.1)
        
        # 4. Game-by-Game Results
        ax4 = axes[1, 1]
        games = completed_games['game'].str.replace(' at ', ' @ ')
        predicted_covers = (completed_games['cover_probability'] > 0.5)
        actual_covers = completed_games['actual_cover']
        
        # Create comparison
        results_comparison = pd.DataFrame({
            'Game': games,
            'Predicted': predicted_covers,
            'Actual': actual_covers,
            'Correct': predicted_covers == actual_covers
        })
        
        # Plot as horizontal bars
        y_pos = np.arange(len(games))
        colors = ['green' if correct else 'red' for correct in results_comparison['Correct']]
        
        ax4.barh(y_pos, results_comparison['Predicted'].astype(int), 
                alpha=0.3, color='blue', label='Predicted')
        ax4.barh(y_pos, results_comparison['Actual'].astype(int), 
                alpha=0.7, color=colors, label='Actual')
        
        ax4.set_yticks(y_pos)
        ax4.set_yticklabels(games, fontsize=8)
        ax4.set_xlabel('Cover (1=Yes, 0=No)')
        ax4.set_title('Game-by-Game Predictions vs Results')
        ax4.legend()
        ax4.set_xlim(-0.1, 1.1)
        
        plt.tight_layout()
        plt.savefig('week2_model_performance.png', dpi=300, bbox_inches='tight')
        print("Saved visualization to week2_model_performance.png")
        
        return fig
    
    def generate_report(self, performance_summary, completed_games):
        """Generate a detailed markdown report"""
        if performance_summary is None or completed_games is None:
            print("No performance data to report")
            return
            
        report = f"""# Week 2 2025 Model Performance Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

The model made predictions for {performance_summary['total_games']} completed games in Week 2 2025.

### Overall Performance
- **Spread Coverage Accuracy**: {performance_summary['spread_accuracy']:.1%} ({performance_summary['correct_spread_predictions']}/{performance_summary['total_games']})
- **Outright Win Accuracy**: {performance_summary['outright_accuracy']:.1%} ({performance_summary['correct_outright_predictions']}/{performance_summary['total_games']})

### Performance by Confidence Level

| Confidence | Games | Accuracy | Correct |
|------------|-------|----------|---------|
| HIGH | {performance_summary['high_confidence_games']} | {performance_summary['high_confidence_accuracy']:.1%} | {performance_summary['high_confidence_games'] * (performance_summary['high_confidence_accuracy'] or 0):.0f} |
| MEDIUM | {performance_summary['medium_confidence_games']} | {performance_summary['medium_confidence_accuracy']:.1%} | {performance_summary['medium_confidence_games'] * (performance_summary['medium_confidence_accuracy'] or 0):.0f} |
| LOW | {performance_summary['low_confidence_games']} | {performance_summary['low_confidence_accuracy']:.1%} | {performance_summary['low_confidence_games'] * (performance_summary['low_confidence_accuracy'] or 0):.0f} |

## Detailed Game Results

| Game | Underdog | Favorite | Spread | Predicted Prob | Predicted | Actual Cover | Correct | Confidence |
|------|----------|----------|--------|----------------|-----------|--------------|---------|------------|
"""
        
        for _, game in completed_games.iterrows():
            predicted_cover = "Cover" if game['cover_probability'] > 0.5 else "No Cover"
            actual_cover = "Cover" if game['actual_cover'] else "No Cover"
            correct = "✓" if (game['cover_probability'] > 0.5) == game['actual_cover'] else "✗"
            
            report += f"| {game['game']} | {game['underdog']} | {game['favorite']} | {game['spread']} | {game['cover_probability']:.1%} | {predicted_cover} | {actual_cover} | {correct} | {game['confidence']} |\n"
        
        report += f"""
## Key Insights

### Model Strengths
- The model achieved {performance_summary['spread_accuracy']:.1%} accuracy on spread predictions
- High confidence predictions had {performance_summary['high_confidence_accuracy']:.1%} accuracy
- The model correctly predicted {performance_summary['correct_outright_predictions']} outright underdog wins

### Areas for Improvement
- Low confidence predictions had {performance_summary['low_confidence_accuracy']:.1%} accuracy
- The model missed {performance_summary['total_games'] - performance_summary['correct_spread_predictions']} spread predictions

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
- **Analysis Date**: {datetime.now().strftime('%Y-%m-%d')}
"""
        
        # Save report
        with open('week2_model_performance_report.md', 'w') as f:
            f.write(report)
        
        print("Saved detailed report to week2_model_performance_report.md")
        return report
    
    def export_results(self, completed_games):
        """Export detailed results to CSV"""
        if completed_games is None:
            print("No completed games to export")
            return
            
        # Create detailed results export
        export_df = completed_games.copy()
        export_df['predicted_cover'] = (export_df['cover_probability'] > 0.5)
        export_df['predicted_outright_win'] = (export_df['cover_probability'] > 0.5)
        export_df['spread_correct'] = export_df['predicted_cover'] == export_df['actual_cover']
        export_df['outright_correct'] = export_df['predicted_outright_win'] == export_df['actual_underdog_win']
        
        # Select relevant columns for export (only include columns that exist)
        available_columns = [
            'game', 'underdog', 'favorite', 'spread', 'cover_probability', 'confidence',
            'predicted_cover', 'actual_cover', 'spread_correct',
            'predicted_outright_win', 'actual_underdog_win', 'outright_correct',
            'actual_home_score', 'actual_away_score', 'notes'
        ]
        
        # Only include columns that actually exist in the dataframe
        export_columns = [col for col in available_columns if col in export_df.columns]
        
        export_df = export_df[export_columns]
        export_df.to_csv('week2_detailed_results.csv', index=False)
        print("Saved detailed results to week2_detailed_results.csv")
        
        return export_df

def main():
    """Main function to run the Week 2 model tracker"""
    print("=== Week 2 2025 Model Performance Tracker ===")
    
    tracker = Week2ModelTracker()
    
    # Load predictions
    if not tracker.load_predictions():
        print("Could not load predictions. Exiting.")
        return
    
    # Check if results exist, if not create template
    if not tracker.load_results():
        print("Creating results template...")
        tracker.create_results_template()
        print("\nPlease fill in the actual game results in week2_results_template.csv")
        print("Then rename it to week2_results.csv and run this script again.")
        return
    
    # Analyze performance
    print("\n=== Analyzing Model Performance ===")
    performance_summary, completed_games = tracker.analyze_performance()
    
    if performance_summary is None:
        print("No completed games to analyze")
        return
    
    # Print summary
    print(f"\nOverall Spread Accuracy: {performance_summary['spread_accuracy']:.1%}")
    print(f"Overall Outright Accuracy: {performance_summary['outright_accuracy']:.1%}")
    print(f"High Confidence Accuracy: {performance_summary['high_confidence_accuracy']:.1%}")
    
    # Create visualizations
    print("\n=== Creating Visualizations ===")
    tracker.create_visualizations(completed_games)
    
    # Generate report
    print("\n=== Generating Report ===")
    tracker.generate_report(performance_summary, completed_games)
    
    # Export results
    print("\n=== Exporting Results ===")
    tracker.export_results(completed_games)
    
    print("\n=== Analysis Complete ===")
    print("Files created:")
    print("- week2_model_performance.png (visualizations)")
    print("- week2_model_performance_report.md (detailed report)")
    print("- week2_detailed_results.csv (exported data)")

if __name__ == "__main__":
    main()
