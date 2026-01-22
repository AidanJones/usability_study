# Usability Study Data Analysis

A comprehensive Python-based data analysis toolkit for usability studies with support for **multiple users**, **multiple studies/experiments**, and observer comparisons. This project uses `uv` for Python environment management.

## Features

- **Multi-Study Analysis**: Compare data across different experiments/studies
- **Multi-User Support**: Analyze multiple users simultaneously
- **User vs Observer Comparison**: Detailed comparison metrics between users and observers
- **User Consistency Tracking**: Track how individual users change across studies
- Load and analyze usability study data from Excel files
- Statistical analysis and agreement metrics
- Comprehensive visualization suite:
  - Score distribution histograms (by study)
  - Question-by-question comparisons
  - User consistency across studies (line plots + heatmaps)
  - Study-specific user comparisons
  - Difference analysis
  - Correlation plots
  - Box plots
- Comprehensive reporting for multi-study data

## Quick Start

```bash
# 1. Sync dependencies
uv sync

# 2. Create sample data (optional - skip if you have your own data file)
uv run python create_sample_data.py

# 3. Run the complete multi-study analysis example
uv run python example_multi_study_analysis.py

# 4. Or start Jupyter Notebook for interactive analysis
uv run jupyter notebook
# Then open usability_analysis.ipynb and run all cells
```

### Quick Example - Multi-Study Analysis

```python
from analysis_utils import UsabilityStudyAnalyzer

# Initialize and load data
analyzer = UsabilityStudyAnalyzer('usability_study_data.xls')
analyzer.load_data()

# Generate comprehensive report
analyzer.generate_full_report()

# Analyze User 1 across all studies
user1_data = analyzer.analyze_user_across_studies('User 1')
analyzer.plot_user_across_studies('User 1')

# Compare all users in Study 1
analyzer.plot_users_comparison_by_study(1)

# Calculate user consistency across studies
consistency = analyzer.calculate_user_consistency()

# User vs Observer comparison
comparison = analyzer.compare_user_vs_observer()
```

## Project Structure

```
.
├── pyproject.toml                    # Project dependencies managed by uv
├── requirements.txt                  # Python dependencies (for pip users)
├── analysis_utils.py                 # Core analysis utilities and classes
├── create_sample_data.py             # Script to generate sample multi-study data
├── example_multi_study_analysis.py   # Complete multi-study analysis example
├── usability_analysis.ipynb          # Jupyter notebook for interactive analysis
├── usability_study_data.xls          # Your data file (generated or provided)
└── README.md                         # This file
```

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer

### Installing uv

If you don't have `uv` installed:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Setup

1. **Sync dependencies with uv:**

```bash
uv sync
```

This will create a virtual environment and install all required packages.

2. **Create sample data (optional):**

If you don't have your own data file yet, generate sample data:

```bash
uv run python create_sample_data.py
```

This creates `usability_study_data.xls` with example data.

## Usage

### Option 1: Run Jupyter Notebook (Recommended)

1. Start Jupyter Notebook:

```bash
uv run jupyter notebook
```

2. Open `usability_analysis.ipynb` in your browser

3. Run all cells to see the complete analysis

### Option 2: Run the Complete Multi-Study Example

Run the comprehensive example that demonstrates all features:

```bash
python example_multi_study_analysis.py
```

This will generate:
- Complete console report with all metrics
- 8+ visualization PNG files:
  - `all_studies_overview.png` - Overview of all studies
  - `user1_across_studies.png` - User 1's changes across studies
  - `user2_across_studies.png` - User 2's changes across studies
  - `study1_comparison.png` - All users in Study 1
  - `study2_comparison.png` - All users in Study 2
  - `score_distributions_by_study.png` - Score distributions
  - `study1_question_comparison.png` - Question-level comparison
  - `study1_score_differences.png` - User vs observer differences

### Option 3: Use the Analysis Module Directly

You can also use the analysis utilities in your own Python scripts:

```python
from analysis_utils import UsabilityStudyAnalyzer

# Initialize analyzer
analyzer = UsabilityStudyAnalyzer('usability_study_data.xls')

# Load data
analyzer.load_data()

# Get summary statistics by study and user
print(analyzer.get_summary_statistics(by_study=True, by_user=True))

# Analyze specific user across studies
user1_data = analyzer.analyze_user_across_studies('User 1')
print(user1_data)

# Generate visualizations
analyzer.plot_score_distribution(by_study=True)
analyzer.plot_user_across_studies('User 1')
analyzer.plot_users_comparison_by_study(1)
analyzer.plot_all_studies_overview()

# Calculate user consistency
consistency = analyzer.calculate_user_consistency()
print(consistency)

# User vs observer comparison
comparison = analyzer.compare_user_vs_observer()
print(comparison)

# Generate full multi-study report
analyzer.generate_full_report()
```

## Data Format

Your Excel file should have the following structure for **multi-study analysis**:

| User      | Question | Score | Study |
|-----------|----------|-------|-------|
| User 1    | 1        | 10    | 1     |
| User 1    | 2        | 4     | 1     |
| User 2    | 1        | 0     | 1     |
| Observer  | 1        | 4     | 1     |
| User 1    | 1        | 0     | 2     |
| User 2    | 1        | 0     | 2     |
| Observer  | 1        | 0     | 2     |
| ...       | ...      | ...   | ...   |

- **User**: Identifier (e.g., "User 1", "User 2", ..., "Observer")
- **Question**: Question number (1-10 or any range)
- **Score**: Rating score (typically 0-10)
- **Study**: Study/experiment identifier (1, 2, 3, etc.)

**Note**: The toolkit now supports multiple users across multiple studies. Each user can appear in multiple studies, allowing for longitudinal analysis and consistency tracking.

## Multi-Study Analysis Methods

The toolkit now includes powerful methods for analyzing multiple users across multiple studies:

### Core Analysis Methods

1. **`analyze_user_across_studies(user)`**: Get a specific user's data across all studies
2. **`compare_users_by_study(study)`**: Compare all users and observer for a specific study
3. **`calculate_user_consistency()`**: Calculate how consistent each user is across studies
4. **`compare_user_vs_observer(study=None)`**: Detailed user vs observer comparison metrics
5. **`get_summary_statistics(by_study=True, by_user=True)`**: Statistics broken down by study and/or user

### Visualization Methods

1. **`plot_all_studies_overview()`**: Comprehensive overview of all studies
2. **`plot_user_across_studies(user)`**: Line plot + heatmap showing user changes across studies
3. **`plot_users_comparison_by_study(study)`**: Compare all users in a specific study
4. **`plot_score_distribution(by_study=True)`**: Score distributions by study
5. **`plot_question_comparison(study=None, user=None)`**: Question-level comparisons
6. **`plot_score_differences(study=None)`**: User vs observer difference analysis

### Key Metrics

**User Consistency Metrics:**
- Mean Absolute Difference: Average change in scores across studies
- Std Dev of Differences: Variability in score changes
- Max Difference: Largest change between studies
- Consistency Score (%): Overall consistency (100% = perfect consistency)

**User vs Observer Comparison:**
- Mean Difference: Average difference (user - observer)
- Mean Absolute Difference: Average absolute difference
- RMSE: Root Mean Square Error
- Correlation: Pearson correlation coefficient
- Agreement ≤1: Percentage within 1 point
- Agreement ≤2: Percentage within 2 points

## Analysis Outputs

The analysis provides:

1. **Summary Statistics**: Mean, median, std dev, min, max by study and user
2. **Score Distributions**: Histograms showing rating patterns (by study)
3. **Question Comparisons**: Line and bar charts comparing responses
4. **User Consistency**: Track how users change across studies
5. **Multi-User Comparisons**: Compare different users within the same study
6. **Difference Analysis**: How much users and observers differ per question
7. **Agreement Metrics**: Detailed comparison metrics between users and observers
8. **Correlation Analysis**: Statistical relationships between user and observer scores
9. **Comprehensive Reports**: Text-based analysis with all metrics

## Customization

### Change Data File

In the notebook, modify the file path:

```python
analyzer = UsabilityStudyAnalyzer('your_data_file.xls')
```

### Adjust Visualizations

Modify `figsize` parameters in the analysis functions:

```python
analyzer.plot_score_distribution(figsize=(16, 6))
```

### Export Visualizations

Save figures to files:

```python
fig = analyzer.plot_question_comparison()
fig.savefig('comparison.png', dpi=300, bbox_inches='tight')
```

## Dependencies

All dependencies are managed through `pyproject.toml`:

- pandas: Data manipulation
- openpyxl: Excel file reading
- matplotlib: Plotting
- seaborn: Statistical visualizations
- jupyter: Notebook interface
- numpy: Numerical operations

## Troubleshooting

### Issue: "No module named 'analysis_utils'"

Make sure you're running the notebook from the project directory:

```bash
cd /path/to/usability_study
uv run jupyter notebook
```

### Issue: Excel file not found

Ensure your data file is in the same directory as the notebook, or provide the full path:

```python
analyzer = UsabilityStudyAnalyzer('/full/path/to/data.xls')
```

### Issue: Style warnings in plots

If you see matplotlib style warnings, the plots will still work. Update the notebook to use:

```python
plt.style.use('default')
```

## Contributing

Feel free to extend the analysis utilities with additional:
- Statistical tests (t-tests, ANOVA, etc.)
- Alternative visualizations
- Export functionality (PDF reports, etc.)
- Data validation and cleaning

## License

MIT License - See LICENSE file for details
