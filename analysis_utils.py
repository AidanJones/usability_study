"""
Utility functions for usability study data analysis.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class UsabilityStudyAnalyzer:
    """Class to handle usability study data analysis."""

    def __init__(self, file_path):
        """
        Initialize the analyzer with data from an Excel file.

        Args:
            file_path: Path to the Excel file containing usability study data
        """
        self.file_path = file_path
        self.df = None
        self.user_data = None
        self.observer_data = None

    def load_data(self):
        """Load data from the Excel file."""
        try:
            self.df = pd.read_excel(self.file_path)
            print(f"Data loaded successfully from {self.file_path}")
            print(f"Shape: {self.df.shape}")
            print(f"\nColumns: {list(self.df.columns)}")

            # Separate user and observer data
            self.user_data = self.df[self.df['User'].str.startswith('User', na=False)]
            self.observer_data = self.df[self.df['User'] == 'Observer']

            print(f"\nUser responses: {len(self.user_data)}")
            print(f"Observer responses: {len(self.observer_data)}")

            return self.df
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def get_summary_statistics(self):
        """Calculate summary statistics for user and observer responses."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        summary = {
            'User Scores': {
                'Mean': self.user_data['Score'].mean(),
                'Median': self.user_data['Score'].median(),
                'Std Dev': self.user_data['Score'].std(),
                'Min': self.user_data['Score'].min(),
                'Max': self.user_data['Score'].max()
            },
            'Observer Scores': {
                'Mean': self.observer_data['Score'].mean(),
                'Median': self.observer_data['Score'].median(),
                'Std Dev': self.observer_data['Score'].std(),
                'Min': self.observer_data['Score'].min(),
                'Max': self.observer_data['Score'].max()
            }
        }

        return pd.DataFrame(summary).T

    def plot_score_distribution(self, figsize=(12, 5)):
        """
        Plot the distribution of scores for users and observers.

        Args:
            figsize: Tuple specifying figure size
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # User scores distribution
        axes[0].hist(self.user_data['Score'], bins=range(0, 12),
                     edgecolor='black', alpha=0.7, color='steelblue')
        axes[0].set_xlabel('Score')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('User Score Distribution')
        axes[0].grid(axis='y', alpha=0.3)

        # Observer scores distribution
        axes[1].hist(self.observer_data['Score'], bins=range(0, 12),
                     edgecolor='black', alpha=0.7, color='coral')
        axes[1].set_xlabel('Score')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Observer Score Distribution')
        axes[1].grid(axis='y', alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_question_comparison(self, figsize=(14, 6)):
        """
        Compare user and observer scores by question.

        Args:
            figsize: Tuple specifying figure size
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # Prepare data for comparison
        comparison_data = pd.DataFrame({
            'Question': self.user_data['Question'].values,
            'User Score': self.user_data['Score'].values,
            'Observer Score': self.observer_data['Score'].values
        })

        # Line plot
        axes[0].plot(comparison_data['Question'], comparison_data['User Score'],
                     marker='o', label='User', linewidth=2, markersize=8)
        axes[0].plot(comparison_data['Question'], comparison_data['Observer Score'],
                     marker='s', label='Observer', linewidth=2, markersize=8)
        axes[0].set_xlabel('Question Number')
        axes[0].set_ylabel('Score')
        axes[0].set_title('User vs Observer Scores by Question')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        axes[0].set_xticks(range(1, 11))

        # Bar plot
        x = np.arange(len(comparison_data['Question']))
        width = 0.35

        axes[1].bar(x - width/2, comparison_data['User Score'],
                    width, label='User', alpha=0.8, color='steelblue')
        axes[1].bar(x + width/2, comparison_data['Observer Score'],
                    width, label='Observer', alpha=0.8, color='coral')
        axes[1].set_xlabel('Question Number')
        axes[1].set_ylabel('Score')
        axes[1].set_title('User vs Observer Scores Comparison')
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(comparison_data['Question'])
        axes[1].legend()
        axes[1].grid(axis='y', alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_score_differences(self, figsize=(12, 5)):
        """
        Plot the difference between user and observer scores.

        Args:
            figsize: Tuple specifying figure size
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Calculate differences
        differences = self.user_data['Score'].values - self.observer_data['Score'].values
        questions = self.user_data['Question'].values

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # Bar plot of differences
        colors = ['green' if d > 0 else 'red' for d in differences]
        axes[0].bar(questions, differences, color=colors, alpha=0.7, edgecolor='black')
        axes[0].axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        axes[0].set_xlabel('Question Number')
        axes[0].set_ylabel('Score Difference (User - Observer)')
        axes[0].set_title('Score Differences by Question')
        axes[0].grid(axis='y', alpha=0.3)
        axes[0].set_xticks(range(1, 11))

        # Box plot of all scores
        data_for_box = [self.user_data['Score'], self.observer_data['Score']]
        axes[1].boxplot(data_for_box, labels=['User', 'Observer'],
                        patch_artist=True,
                        boxprops=dict(facecolor='lightblue', alpha=0.7),
                        medianprops=dict(color='red', linewidth=2))
        axes[1].set_ylabel('Score')
        axes[1].set_title('Score Distribution Comparison')
        axes[1].grid(axis='y', alpha=0.3)

        plt.tight_layout()
        return fig

    def calculate_agreement_metrics(self):
        """Calculate agreement metrics between user and observer."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        user_scores = self.user_data['Score'].values
        observer_scores = self.observer_data['Score'].values

        # Calculate various metrics
        differences = user_scores - observer_scores
        absolute_differences = np.abs(differences)

        metrics = {
            'Mean Difference': np.mean(differences),
            'Mean Absolute Difference': np.mean(absolute_differences),
            'RMSE': np.sqrt(np.mean(differences**2)),
            'Correlation': np.corrcoef(user_scores, observer_scores)[0, 1],
            'Agreement within 1 point': np.sum(absolute_differences <= 1) / len(differences) * 100,
            'Agreement within 2 points': np.sum(absolute_differences <= 2) / len(differences) * 100,
        }

        return pd.Series(metrics)

    def generate_full_report(self):
        """Generate a comprehensive analysis report."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        print("=" * 60)
        print("USABILITY STUDY ANALYSIS REPORT")
        print("=" * 60)

        print("\n1. SUMMARY STATISTICS")
        print("-" * 60)
        print(self.get_summary_statistics())

        print("\n2. AGREEMENT METRICS")
        print("-" * 60)
        print(self.calculate_agreement_metrics())

        print("\n3. DETAILED DATA")
        print("-" * 60)
        comparison = pd.DataFrame({
            'Question': self.user_data['Question'].values,
            'User Score': self.user_data['Score'].values,
            'Observer Score': self.observer_data['Score'].values,
            'Difference': self.user_data['Score'].values - self.observer_data['Score'].values
        })
        print(comparison)

        print("\n" + "=" * 60)
