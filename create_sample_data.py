"""
Script to create sample usability study data in Excel format.
This generates data matching the structure shown in the user's table.
"""
import pandas as pd

def create_sample_data():
    """Create sample usability study data based on the provided table."""

    # Data from the user's updated table with multiple users and studies
    data = {
        'User': [
            # Study 1
            'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1',
            'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2',
            'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer',
            # Study 2
            'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1', 'User 1',
            'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2', 'User 2',
            'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer', 'Observer'
        ],
        'Question': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 6,  # 10 questions for each of 6 groups (2 users + 1 observer) × 2 studies
        'Score': [
            # Study 1 - User 1
            10, 4, 3, 4, 3, 6, 6, 4, 3, 2,
            # Study 1 - User 2
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            # Study 1 - Observer
            4, 5, 3, 1, 6, 7, 8, 9, 0, 5,
            # Study 2 - User 1
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            # Study 2 - User 2
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            # Study 2 - Observer
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ],
        'Study': [1] * 30 + [2] * 30  # 30 rows for study 1, 30 rows for study 2
    }

    df = pd.DataFrame(data)

    # Save to Excel file
    output_file = 'usability_study_data.xls'
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Sample data created successfully: {output_file}")
    print(f"\nData shape: {df.shape}")
    print(f"Studies: {df['Study'].unique()}")
    print(f"Users: {df['User'].unique()}")
    print(f"\nData preview:\n{df.head(20)}")

    return df

if __name__ == "__main__":
    create_sample_data()
