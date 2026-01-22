"""
Example script demonstrating multi-study, multi-user analysis.
This script shows how to use the updated UsabilityStudyAnalyzer
to analyze data with multiple users across multiple experiments/studies.
"""

from analysis_utils import UsabilityStudyAnalyzer
import matplotlib.pyplot as plt

def main():
    # Create or load data
    print("Step 1: Creating sample data...")
    from create_sample_data import create_sample_data
    create_sample_data()

    # Initialize analyzer
    print("\nStep 2: Loading data...")
    analyzer = UsabilityStudyAnalyzer('usability_study_data.xls')
    analyzer.load_data()

    # Generate comprehensive report
    print("\n" + "="*80)
    print("COMPREHENSIVE ANALYSIS")
    print("="*80)
    analyzer.generate_full_report()

    # Detailed analysis examples
    print("\n" + "="*80)
    print("EXAMPLE ANALYSES")
    print("="*80)

    # 1. Analyze User 1 across studies
    print("\n1. User 1 Across Studies:")
    print("-" * 40)
    user1_data = analyzer.analyze_user_across_studies('User 1')
    print(user1_data)

    # 2. Compare all users in Study 1
    print("\n2. All Users Comparison in Study 1:")
    print("-" * 40)
    study1_comparison = analyzer.compare_users_by_study(1)
    print(study1_comparison)

    # 3. User consistency metrics
    print("\n3. User Consistency Across Studies:")
    print("-" * 40)
    consistency = analyzer.calculate_user_consistency()
    if consistency is not None:
        print(consistency)

    # 4. User vs Observer detailed comparison
    print("\n4. User vs Observer Detailed Comparison:")
    print("-" * 40)
    user_obs_comp = analyzer.compare_user_vs_observer()
    if user_obs_comp is not None:
        print(user_obs_comp)

    # Generate visualizations
    print("\n" + "="*80)
    print("GENERATING VISUALIZATIONS")
    print("="*80)

    # Plot 1: Overall studies overview
    print("\n1. Creating overview of all studies...")
    fig1 = analyzer.plot_all_studies_overview()
    plt.savefig('all_studies_overview.png', dpi=150, bbox_inches='tight')
    print("   Saved: all_studies_overview.png")
    plt.close()

    # Plot 2: User 1 across studies
    print("\n2. Creating User 1 across studies plot...")
    fig2 = analyzer.plot_user_across_studies('User 1')
    if fig2 is not None:
        plt.savefig('user1_across_studies.png', dpi=150, bbox_inches='tight')
        print("   Saved: user1_across_studies.png")
        plt.close()

    # Plot 3: User 2 across studies
    print("\n3. Creating User 2 across studies plot...")
    fig3 = analyzer.plot_user_across_studies('User 2')
    if fig3 is not None:
        plt.savefig('user2_across_studies.png', dpi=150, bbox_inches='tight')
        print("   Saved: user2_across_studies.png")
        plt.close()

    # Plot 4: Study 1 comparison
    print("\n4. Creating Study 1 comparison plot...")
    fig4 = analyzer.plot_users_comparison_by_study(1)
    plt.savefig('study1_comparison.png', dpi=150, bbox_inches='tight')
    print("   Saved: study1_comparison.png")
    plt.close()

    # Plot 5: Study 2 comparison
    print("\n5. Creating Study 2 comparison plot...")
    fig5 = analyzer.plot_users_comparison_by_study(2)
    plt.savefig('study2_comparison.png', dpi=150, bbox_inches='tight')
    print("   Saved: study2_comparison.png")
    plt.close()

    # Plot 6: Score distributions by study
    print("\n6. Creating score distribution plots...")
    fig6 = analyzer.plot_score_distribution(by_study=True)
    plt.savefig('score_distributions_by_study.png', dpi=150, bbox_inches='tight')
    print("   Saved: score_distributions_by_study.png")
    plt.close()

    # Plot 7: Question comparison for Study 1
    print("\n7. Creating question comparison for Study 1...")
    fig7 = analyzer.plot_question_comparison(study=1)
    plt.savefig('study1_question_comparison.png', dpi=150, bbox_inches='tight')
    print("   Saved: study1_question_comparison.png")
    plt.close()

    # Plot 8: Score differences by study
    print("\n8. Creating score differences plot for Study 1...")
    fig8 = analyzer.plot_score_differences(study=1)
    plt.savefig('study1_score_differences.png', dpi=150, bbox_inches='tight')
    print("   Saved: study1_score_differences.png")
    plt.close()

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated files:")
    print("  - usability_study_data.xls (data file)")
    print("  - all_studies_overview.png")
    print("  - user1_across_studies.png")
    print("  - user2_across_studies.png")
    print("  - study1_comparison.png")
    print("  - study2_comparison.png")
    print("  - score_distributions_by_study.png")
    print("  - study1_question_comparison.png")
    print("  - study1_score_differences.png")

if __name__ == "__main__":
    main()
