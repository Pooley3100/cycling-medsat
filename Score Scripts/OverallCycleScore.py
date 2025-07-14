import pandas as pd
import sys

Region = sys.argv[1]

'''

Calculate overall cycling score using commute rate, CQI and crash rate with their respective weightings in the file msoa_scores.csv

with equation CycleScore for MSOA = 0.40? × Infrastructure Score
          + 0.30? × Participation Score
          + 0.30? × Safety Score

then add overall column to the file msoa_score.csv
 
'''

msoa_scores_path = f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv"
msoa_scores_csv = pd.read_csv(f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv", header=0, names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path'])

# Calculate the overall cycling score
msoa_scores_csv['OverallCycleScore'] = (0.40 * msoa_scores_csv['ScoreCQI'] +
                    0.25 * msoa_scores_csv['commute_rate'] +
                    0.35 * msoa_scores_csv['crash_rate'])

# Save the updated DataFrame back to the CSV file
msoa_scores_csv.to_csv(msoa_scores_path, index=False)

