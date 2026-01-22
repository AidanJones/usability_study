# Usability Study Data Analysis

A Python-based data analysis toolkit for usability studies, comparing user and observer responses across multiple questions. This project uses `uv` for Python environment management.

## Features

- Load and analyze usability study data from Excel files
- Compare user vs observer responses
- Statistical analysis and agreement metrics
- Multiple visualization types:
  - Score distribution histograms
  - Question-by-question comparisons
  - Difference analysis
  - Correlation plots
  - Box plots
- Comprehensive reporting

## Quick Start

```bash
# 1. Sync dependencies
uv sync

# 2. Create sample data (optional - skip if you have your own data file)
uv run python create_sample_data.py

# 3. Start Jupyter Notebook
uv run jupyter notebook

# 4. Open usability_analysis.ipynb and run all cells
```

## Project Structure

```
.
├── pyproject.toml              # Project dependencies managed by uv
├── analysis_utils.py           # Core analysis utilities and classes
├── create_sample_data.py       # Script to generate sample data
├── usability_analysis.ipynb    # Main Jupyter notebook for analysis
├── usability_study_data.xls    # Your data file (generated or provided)
└── README.md                   # This file
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

### Option 2: Use the Analysis Module Directly

You can also use the analysis utilities in your own Python scripts:

```python
from analysis_utils import UsabilityStudyAnalyzer

# Initialize analyzer
analyzer = UsabilityStudyAnalyzer('usability_study_data.xls')

# Load data
analyzer.load_data()

# Get summary statistics
print(analyzer.get_summary_statistics())

# Generate visualizations
analyzer.plot_score_distribution()
analyzer.plot_question_comparison()
analyzer.plot_score_differences()

# Calculate agreement metrics
print(analyzer.calculate_agreement_metrics())

# Generate full report
analyzer.generate_full_report()
```

## Data Format

Your Excel file should have the following structure:

| User      | Question | Score |
|-----------|----------|-------|
| User 1    | 1        | 10    |
| User 2    | 2        | 4     |
| ...       | ...      | ...   |
| Observer  | 1        | 4     |
| Observer  | 2        | 5     |
| ...       | ...      | ...   |

- **User**: Identifier (e.g., "User 1", "User 2", ..., "Observer")
- **Question**: Question number (1-10)
- **Score**: Rating score (typically 1-10)

## Analysis Outputs

The notebook provides:

1. **Summary Statistics**: Mean, median, std dev, min, max for both groups
2. **Score Distributions**: Histograms showing rating patterns
3. **Question Comparisons**: Line and bar charts comparing responses
4. **Difference Analysis**: How much users and observers differ per question
5. **Agreement Metrics**:
   - Mean difference
   - Mean absolute difference
   - RMSE
   - Correlation coefficient
   - Agreement percentages (within 1-2 points)
6. **Correlation Plot**: Scatter plot with trend line
7. **Detailed Report**: Comprehensive text-based analysis

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
