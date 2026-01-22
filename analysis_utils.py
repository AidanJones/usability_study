"""
Utility functions for usability study data analysis.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class UsabilityStudyAnalyzer:
    """Class to handle usability study data analysis with multiple studies and users."""

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
        self.studies = None
        self.users = None

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

            # Get unique studies and users
            if 'Study' in self.df.columns:
                self.studies = sorted(self.df['Study'].unique())
                print(f"\nStudies found: {self.studies}")
            else:
                self.studies = [1]  # Default to single study if no Study column
                self.df['Study'] = 1

            self.users = sorted([u for u in self.df['User'].unique() if u.startswith('User')])

            print(f"Users found: {self.users}")
            print(f"\nUser responses: {len(self.user_data)}")
            print(f"Observer responses: {len(self.observer_data)}")

            return self.df
        except Exception as e:
            print(f"Error loading data: {e}")
            raise

    def get_summary_statistics(self, by_study=True, by_user=True):
        """
        Calculate summary statistics for user and observer responses.

        Args:
            by_study: If True, break down statistics by study
            by_user: If True, break down statistics by individual user
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        results = []

        if by_study and by_user:
            # Statistics by study and user
            for study in self.studies:
                study_data = self.df[self.df['Study'] == study]
                for user in self.users:
                    user_study_data = study_data[study_data['User'] == user]
                    if len(user_study_data) > 0:
                        results.append({
                            'Study': study,
                            'User': user,
                            'Mean': user_study_data['Score'].mean(),
                            'Median': user_study_data['Score'].median(),
                            'Std Dev': user_study_data['Score'].std(),
                            'Min': user_study_data['Score'].min(),
                            'Max': user_study_data['Score'].max(),
                            'Count': len(user_study_data)
                        })

                # Observer stats for this study
                observer_study_data = study_data[study_data['User'] == 'Observer']
                if len(observer_study_data) > 0:
                    results.append({
                        'Study': study,
                        'User': 'Observer',
                        'Mean': observer_study_data['Score'].mean(),
                        'Median': observer_study_data['Score'].median(),
                        'Std Dev': observer_study_data['Score'].std(),
                        'Min': observer_study_data['Score'].min(),
                        'Max': observer_study_data['Score'].max(),
                        'Count': len(observer_study_data)
                    })
        elif by_study:
            # Statistics by study only
            for study in self.studies:
                study_user_data = self.df[(self.df['Study'] == study) & (self.df['User'].str.startswith('User', na=False))]
                study_observer_data = self.df[(self.df['Study'] == study) & (self.df['User'] == 'Observer')]

                results.append({
                    'Study': study,
                    'Type': 'Users',
                    'Mean': study_user_data['Score'].mean(),
                    'Median': study_user_data['Score'].median(),
                    'Std Dev': study_user_data['Score'].std(),
                    'Count': len(study_user_data)
                })
                results.append({
                    'Study': study,
                    'Type': 'Observer',
                    'Mean': study_observer_data['Score'].mean(),
                    'Median': study_observer_data['Score'].median(),
                    'Std Dev': study_observer_data['Score'].std(),
                    'Count': len(study_observer_data)
                })
        else:
            # Overall statistics
            results.append({
                'Type': 'All Users',
                'Mean': self.user_data['Score'].mean(),
                'Median': self.user_data['Score'].median(),
                'Std Dev': self.user_data['Score'].std(),
                'Count': len(self.user_data)
            })
            results.append({
                'Type': 'Observer',
                'Mean': self.observer_data['Score'].mean(),
                'Median': self.observer_data['Score'].median(),
                'Std Dev': self.observer_data['Score'].std(),
                'Count': len(self.observer_data)
            })

        return pd.DataFrame(results)

    def analyze_user_across_studies(self, user):
        """
        Analyze how a specific user's responses change across studies.

        Args:
            user: The user identifier (e.g., 'User 1')

        Returns:
            DataFrame with comparison across studies
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        user_across_studies = []
        for study in self.studies:
            study_data = self.df[(self.df['Study'] == study) & (self.df['User'] == user)]
            if len(study_data) > 0:
                for _, row in study_data.iterrows():
                    user_across_studies.append({
                        'Study': study,
                        'Question': row['Question'],
                        'Score': row['Score']
                    })

        return pd.DataFrame(user_across_studies)

    def compare_users_by_study(self, study):
        """
        Compare all users and observer for a specific study.

        Args:
            study: The study number

        Returns:
            DataFrame with comparison across users for that study
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        study_data = self.df[self.df['Study'] == study]

        # Pivot to get users as columns
        comparison = study_data.pivot_table(
            index='Question',
            columns='User',
            values='Score',
            aggfunc='first'
        )

        return comparison

    def calculate_user_consistency(self):
        """
        Calculate consistency metrics for each user across studies.

        Returns:
            DataFrame with consistency metrics for each user
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        if len(self.studies) < 2:
            print("Only one study found. Consistency analysis requires multiple studies.")
            return None

        consistency_results = []

        for user in self.users:
            user_data = self.user_data[self.user_data['User'] == user]

            # Get scores by question for each study
            study_scores = {}
            for study in self.studies:
                study_data = user_data[user_data['Study'] == study]
                if len(study_data) > 0:
                    study_scores[study] = study_data.set_index('Question')['Score'].to_dict()

            # Calculate consistency metrics between consecutive studies
            if len(study_scores) >= 2:
                studies_list = sorted(study_scores.keys())
                differences = []

                for i in range(len(studies_list) - 1):
                    study1, study2 = studies_list[i], studies_list[i + 1]
                    scores1 = study_scores[study1]
                    scores2 = study_scores[study2]

                    # Find common questions
                    common_questions = set(scores1.keys()) & set(scores2.keys())

                    for q in common_questions:
                        diff = abs(scores1[q] - scores2[q])
                        differences.append(diff)

                if differences:
                    consistency_results.append({
                        'User': user,
                        'Mean Absolute Difference': np.mean(differences),
                        'Std Dev of Differences': np.std(differences),
                        'Max Difference': np.max(differences),
                        'Consistency Score (%)': (1 - np.mean(differences) / 10) * 100
                    })

        return pd.DataFrame(consistency_results) if consistency_results else None

    def compare_user_vs_observer(self, study=None):
        """
        Compare user scores vs observer scores.

        Args:
            study: If specified, compare only for that study. Otherwise, compare all studies.

        Returns:
            DataFrame with comparison metrics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        results = []

        studies_to_analyze = [study] if study is not None else self.studies

        for s in studies_to_analyze:
            study_data = self.df[self.df['Study'] == s]

            for user in self.users:
                user_data = study_data[study_data['User'] == user]
                observer_data = study_data[study_data['User'] == 'Observer']

                if len(user_data) > 0 and len(observer_data) > 0:
                    # Merge on Question
                    merged = pd.merge(
                        user_data[['Question', 'Score']],
                        observer_data[['Question', 'Score']],
                        on='Question',
                        suffixes=('_user', '_observer')
                    )

                    if len(merged) > 0:
                        differences = merged['Score_user'] - merged['Score_observer']
                        abs_differences = np.abs(differences)

                        results.append({
                            'Study': s,
                            'User': user,
                            'Mean Difference': differences.mean(),
                            'Mean Abs Difference': abs_differences.mean(),
                            'RMSE': np.sqrt((differences ** 2).mean()),
                            'Correlation': merged['Score_user'].corr(merged['Score_observer']),
                            'Agreement ≤1': (abs_differences <= 1).sum() / len(abs_differences) * 100,
                            'Agreement ≤2': (abs_differences <= 2).sum() / len(abs_differences) * 100
                        })

        return pd.DataFrame(results) if results else None

    def plot_score_distribution(self, by_study=True, figsize=(12, 5)):
        """
        Plot the distribution of scores for users and observers.

        Args:
            by_study: If True, separate distributions by study
            figsize: Tuple specifying figure size
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        if by_study and len(self.studies) > 1:
            # Create subplots for each study
            n_studies = len(self.studies)
            fig, axes = plt.subplots(2, n_studies, figsize=(figsize[0] * n_studies / 2, figsize[1] * 1.5))

            if n_studies == 1:
                axes = axes.reshape(-1, 1)

            for idx, study in enumerate(self.studies):
                study_user_data = self.df[(self.df['Study'] == study) & (self.df['User'].str.startswith('User', na=False))]
                study_observer_data = self.df[(self.df['Study'] == study) & (self.df['User'] == 'Observer')]

                # User scores
                axes[0, idx].hist(study_user_data['Score'], bins=range(0, 12),
                                 edgecolor='black', alpha=0.7, color='steelblue')
                axes[0, idx].set_xlabel('Score')
                axes[0, idx].set_ylabel('Frequency')
                axes[0, idx].set_title(f'Study {study} - User Scores')
                axes[0, idx].grid(axis='y', alpha=0.3)

                # Observer scores
                axes[1, idx].hist(study_observer_data['Score'], bins=range(0, 12),
                                 edgecolor='black', alpha=0.7, color='coral')
                axes[1, idx].set_xlabel('Score')
                axes[1, idx].set_ylabel('Frequency')
                axes[1, idx].set_title(f'Study {study} - Observer Scores')
                axes[1, idx].grid(axis='y', alpha=0.3)
        else:
            # Combined distribution across all studies
            fig, axes = plt.subplots(1, 2, figsize=figsize)

            axes[0].hist(self.user_data['Score'], bins=range(0, 12),
                        edgecolor='black', alpha=0.7, color='steelblue')
            axes[0].set_xlabel('Score')
            axes[0].set_ylabel('Frequency')
            axes[0].set_title('All Users - Score Distribution')
            axes[0].grid(axis='y', alpha=0.3)

            axes[1].hist(self.observer_data['Score'], bins=range(0, 12),
                        edgecolor='black', alpha=0.7, color='coral')
            axes[1].set_xlabel('Score')
            axes[1].set_ylabel('Frequency')
            axes[1].set_title('Observer - Score Distribution')
            axes[1].grid(axis='y', alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_question_comparison(self, study=None, user=None, figsize=(14, 6)):
        """
        Compare user and observer scores by question.

        Args:
            study: If specified, show only that study. If None, show all studies.
            user: If specified, show only that user. If None, show average of all users.
            figsize: Tuple specifying figure size
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # Filter data
        if study is not None:
            data = self.df[self.df['Study'] == study]
            title_suffix = f" (Study {study})"
        else:
            data = self.df
            title_suffix = " (All Studies)"

        if user is not None:
            user_data = data[data['User'] == user]
            user_label = user
        else:
            user_data = data[data['User'].str.startswith('User', na=False)]
            # Group by question and average
            user_data = user_data.groupby('Question')['Score'].mean().reset_index()
            user_data['User'] = 'Average User'
            user_label = 'Average User'

        observer_data = data[data['User'] == 'Observer']
        observer_data = observer_data.groupby('Question')['Score'].mean().reset_index()

        # Merge data
        if 'User' in user_data.columns:
            comparison_data = pd.merge(
                user_data[['Question', 'Score']],
                observer_data[['Question', 'Score']],
                on='Question',
                suffixes=('_user', '_observer')
            )
        else:
            comparison_data = pd.merge(
                user_data,
                observer_data[['Question', 'Score']],
                on='Question',
                suffixes=('_user', '_observer')
            )

        # Line plot
        axes[0].plot(comparison_data['Question'], comparison_data['Score_user'],
                     marker='o', label=user_label, linewidth=2, markersize=8)
        axes[0].plot(comparison_data['Question'], comparison_data['Score_observer'],
                     marker='s', label='Observer', linewidth=2, markersize=8)
        axes[0].set_xlabel('Question Number')
        axes[0].set_ylabel('Score')
        axes[0].set_title(f'User vs Observer Scores{title_suffix}')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Bar plot
        x = np.arange(len(comparison_data['Question']))
        width = 0.35

        axes[1].bar(x - width/2, comparison_data['Score_user'],
                    width, label=user_label, alpha=0.8, color='steelblue')
        axes[1].bar(x + width/2, comparison_data['Score_observer'],
                    width, label='Observer', alpha=0.8, color='coral')
        axes[1].set_xlabel('Question Number')
        axes[1].set_ylabel('Score')
        axes[1].set_title(f'Score Comparison{title_suffix}')
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(comparison_data['Question'])
        axes[1].legend()
        axes[1].grid(axis='y', alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_score_differences(self, study=None, figsize=(12, 5)):
        """
        Plot the difference between user and observer scores.

        Args:
            study: If specified, show only that study. If None, show all studies combined.
            figsize: Tuple specifying figure size
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # Filter by study if specified
        if study is not None:
            data = self.df[self.df['Study'] == study]
            title_suffix = f" (Study {study})"
        else:
            data = self.df
            title_suffix = " (All Studies)"

        # Get user and observer data
        user_data = data[data['User'].str.startswith('User', na=False)]
        observer_data = data[data['User'] == 'Observer']

        # Average by question
        user_avg = user_data.groupby('Question')['Score'].mean()
        observer_avg = observer_data.groupby('Question')['Score'].mean()

        # Calculate differences
        common_questions = sorted(set(user_avg.index) & set(observer_avg.index))
        differences = [user_avg[q] - observer_avg[q] for q in common_questions]

        # Bar plot of differences
        colors = ['green' if d > 0 else 'red' for d in differences]
        axes[0].bar(common_questions, differences, color=colors, alpha=0.7, edgecolor='black')
        axes[0].axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        axes[0].set_xlabel('Question Number')
        axes[0].set_ylabel('Avg Score Difference (User - Observer)')
        axes[0].set_title(f'Score Differences{title_suffix}')
        axes[0].grid(axis='y', alpha=0.3)

        # Box plot by user and observer
        box_data = []
        box_labels = []

        for user in sorted(self.users):
            user_scores = data[data['User'] == user]['Score']
            if len(user_scores) > 0:
                box_data.append(user_scores)
                box_labels.append(user)

        observer_scores = data[data['User'] == 'Observer']['Score']
        if len(observer_scores) > 0:
            box_data.append(observer_scores)
            box_labels.append('Observer')

        bp = axes[1].boxplot(box_data, labels=box_labels,
                            patch_artist=True,
                            medianprops=dict(color='red', linewidth=2))

        # Color user boxes differently from observer
        for i, patch in enumerate(bp['boxes']):
            if i < len(self.users):
                patch.set_facecolor('lightblue')
            else:
                patch.set_facecolor('lightcoral')
            patch.set_alpha(0.7)

        axes[1].set_ylabel('Score')
        axes[1].set_title(f'Score Distribution{title_suffix}')
        axes[1].grid(axis='y', alpha=0.3)
        axes[1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        return fig

    def plot_user_across_studies(self, user, figsize=(12, 6)):
        """
        Plot how a specific user's responses change across studies.

        Args:
            user: The user identifier
            figsize: Tuple specifying figure size
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        data = self.analyze_user_across_studies(user)

        if data is None or len(data) == 0:
            print(f"No data found for {user}")
            return None

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # Line plot
        for study in sorted(data['Study'].unique()):
            study_data = data[data['Study'] == study]
            axes[0].plot(study_data['Question'], study_data['Score'],
                        marker='o', label=f'Study {study}', linewidth=2, markersize=8)

        axes[0].set_xlabel('Question Number')
        axes[0].set_ylabel('Score')
        axes[0].set_title(f'{user} - Score Comparison Across Studies')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        axes[0].set_xticks(sorted(data['Question'].unique()))

        # Heatmap
        pivot_data = data.pivot(index='Question', columns='Study', values='Score')
        im = axes[1].imshow(pivot_data.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=10)
        axes[1].set_xlabel('Study')
        axes[1].set_ylabel('Question')
        axes[1].set_title(f'{user} - Score Heatmap')
        axes[1].set_yticks(range(len(pivot_data)))
        axes[1].set_yticklabels(pivot_data.index)
        axes[1].set_xticks(range(len(pivot_data.columns)))
        axes[1].set_xticklabels(pivot_data.columns)

        # Add colorbar
        cbar = plt.colorbar(im, ax=axes[1])
        cbar.set_label('Score')

        # Add values to heatmap
        for i in range(len(pivot_data)):
            for j in range(len(pivot_data.columns)):
                val = pivot_data.values[i, j]
                if not np.isnan(val):
                    axes[1].text(j, i, f'{val:.0f}', ha='center', va='center',
                               color='white' if val < 5 else 'black')

        plt.tight_layout()
        return fig

    def plot_users_comparison_by_study(self, study, figsize=(14, 6)):
        """
        Compare all users and observer for a specific study.

        Args:
            study: The study number
            figsize: Tuple specifying figure size
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        comparison = self.compare_users_by_study(study)

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # Line plot
        for col in comparison.columns:
            axes[0].plot(comparison.index, comparison[col],
                        marker='o', label=col, linewidth=2, markersize=8)

        axes[0].set_xlabel('Question Number')
        axes[0].set_ylabel('Score')
        axes[0].set_title(f'Study {study} - All Participants Comparison')
        axes[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0].grid(True, alpha=0.3)

        # Grouped bar plot
        x = np.arange(len(comparison.index))
        width = 0.8 / len(comparison.columns)

        for i, col in enumerate(comparison.columns):
            offset = (i - len(comparison.columns) / 2) * width + width / 2
            axes[1].bar(x + offset, comparison[col], width, label=col, alpha=0.8)

        axes[1].set_xlabel('Question Number')
        axes[1].set_ylabel('Score')
        axes[1].set_title(f'Study {study} - Grouped Comparison')
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(comparison.index)
        axes[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1].grid(axis='y', alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_all_studies_overview(self, figsize=(16, 10)):
        """
        Create a comprehensive overview of all studies.

        Args:
            figsize: Tuple specifying figure size
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        n_studies = len(self.studies)
        fig, axes = plt.subplots(2, n_studies, figsize=figsize)

        if n_studies == 1:
            axes = axes.reshape(-1, 1)

        for idx, study in enumerate(self.studies):
            study_data = self.df[self.df['Study'] == study]

            # Top row: Score distributions
            for user_type in ['User', 'Observer']:
                if user_type == 'User':
                    data = study_data[study_data['User'].str.startswith('User', na=False)]['Score']
                    color = 'steelblue'
                else:
                    data = study_data[study_data['User'] == 'Observer']['Score']
                    color = 'coral'

                axes[0, idx].hist(data, bins=range(0, 12), alpha=0.6,
                                 label=user_type, edgecolor='black', color=color)

            axes[0, idx].set_xlabel('Score')
            axes[0, idx].set_ylabel('Frequency')
            axes[0, idx].set_title(f'Study {study} - Score Distribution')
            axes[0, idx].legend()
            axes[0, idx].grid(axis='y', alpha=0.3)

            # Bottom row: User comparison
            comparison = self.compare_users_by_study(study)
            for col in comparison.columns:
                axes[1, idx].plot(comparison.index, comparison[col],
                                marker='o', label=col, linewidth=2)

            axes[1, idx].set_xlabel('Question Number')
            axes[1, idx].set_ylabel('Score')
            axes[1, idx].set_title(f'Study {study} - User Comparison')
            axes[1, idx].legend(fontsize=8)
            axes[1, idx].grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def calculate_agreement_metrics(self):
        """
        Calculate basic agreement metrics between all users and observers.
        For detailed analysis by study and user, use compare_user_vs_observer().
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # This is a simplified version for overall metrics
        # For detailed analysis, use compare_user_vs_observer()
        results = []

        for study in self.studies:
            for user in self.users:
                study_user_data = self.df[(self.df['Study'] == study) & (self.df['User'] == user)]
                study_observer_data = self.df[(self.df['Study'] == study) & (self.df['User'] == 'Observer')]

                if len(study_user_data) > 0 and len(study_observer_data) > 0:
                    # Merge on Question to align scores
                    merged = pd.merge(
                        study_user_data[['Question', 'Score']],
                        study_observer_data[['Question', 'Score']],
                        on='Question',
                        suffixes=('_user', '_observer')
                    )

                    if len(merged) > 0:
                        user_scores = merged['Score_user'].values
                        observer_scores = merged['Score_observer'].values

                        differences = user_scores - observer_scores
                        absolute_differences = np.abs(differences)

                        results.append({
                            'Study': study,
                            'User': user,
                            'Mean Difference': np.mean(differences),
                            'Mean Abs Diff': np.mean(absolute_differences),
                            'RMSE': np.sqrt(np.mean(differences**2)),
                            'Correlation': np.corrcoef(user_scores, observer_scores)[0, 1] if len(user_scores) > 1 else np.nan,
                            'Agreement ≤1': np.sum(absolute_differences <= 1) / len(differences) * 100,
                        })

        return pd.DataFrame(results) if results else None

    def generate_full_report(self):
        """Generate a comprehensive analysis report for multiple studies and users."""
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        print("=" * 80)
        print("USABILITY STUDY ANALYSIS REPORT - MULTI-STUDY & MULTI-USER")
        print("=" * 80)

        print(f"\nDataset Overview:")
        print(f"  - Total records: {len(self.df)}")
        print(f"  - Studies: {self.studies}")
        print(f"  - Users: {self.users}")
        print(f"  - Questions: {sorted(self.df['Question'].unique())}")

        print("\n" + "=" * 80)
        print("1. SUMMARY STATISTICS BY STUDY AND USER")
        print("-" * 80)
        print(self.get_summary_statistics(by_study=True, by_user=True))

        print("\n" + "=" * 80)
        print("2. USER CONSISTENCY ACROSS STUDIES")
        print("-" * 80)
        consistency = self.calculate_user_consistency()
        if consistency is not None:
            print(consistency)
        else:
            print("Not enough studies for consistency analysis.")

        print("\n" + "=" * 80)
        print("3. USER vs OBSERVER COMPARISON")
        print("-" * 80)
        user_observer_comp = self.compare_user_vs_observer()
        if user_observer_comp is not None:
            print(user_observer_comp)
        else:
            print("No data available for user-observer comparison.")

        print("\n" + "=" * 80)
        print("4. DETAILED COMPARISON BY STUDY")
        print("-" * 80)
        for study in self.studies:
            print(f"\nStudy {study}:")
            print("-" * 40)
            comparison = self.compare_users_by_study(study)
            print(comparison)

        print("\n" + "=" * 80)
        print("5. INDIVIDUAL USER ANALYSIS ACROSS STUDIES")
        print("-" * 80)
        for user in self.users:
            print(f"\n{user}:")
            print("-" * 40)
            user_analysis = self.analyze_user_across_studies(user)
            if len(user_analysis) > 0:
                pivot = user_analysis.pivot(index='Question', columns='Study', values='Score')
                print(pivot)

                # Calculate change between studies if multiple studies exist
                if len(self.studies) > 1:
                    studies_list = sorted(self.studies)
                    for i in range(len(studies_list) - 1):
                        s1, s2 = studies_list[i], studies_list[i + 1]
                        if s1 in pivot.columns and s2 in pivot.columns:
                            change = pivot[s2] - pivot[s1]
                            print(f"\nChange from Study {s1} to Study {s2}:")
                            print(change)
                            print(f"Mean change: {change.mean():.2f}")
                            print(f"Max increase: {change.max():.2f}")
                            print(f"Max decrease: {change.min():.2f}")
            else:
                print("No data available")

        print("\n" + "=" * 80)
