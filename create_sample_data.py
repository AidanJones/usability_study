"""
Script to create sample usability study data in Excel format.
This generates data matching the structure shown in the user's table.
"""
import pandas as pd

def create_sample_data():
    """Create sample usability study data based on the provided table."""

    # Data from the table provided
    data = {
        'User': [
            'User 1', 'User 2', 'User 3', 'User 4', 'User 5',
            'User 6', 'User 7', 'User 8', 'User 9', 'User 10',
            'Observer', 'Observer', 'Observer', 'Observer', 'Observer',
            'Observer', 'Observer', 'Observer', 'Observer', 'Observer'
        ],
        'Question': [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10,  # Users
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10   # Observers
        ],
        'Score': [
            10, 4, 1, 4, 3, 6, 6, 4, 3, 2,  # User scores
            4, 5, 3, 1, 6, 7, 8, 8, 9, 0    # Observer scores
        ]
    }

    df = pd.DataFrame(data)

    # Save to Excel file
    output_file = 'usability_study_data.xls'
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Sample data created successfully: {output_file}")
    print(f"\nData preview:\n{df}")

    return df

if __name__ == "__main__":
    create_sample_data()
