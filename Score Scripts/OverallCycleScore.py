import pandas as pd
import sys
from sklearn.preprocessing import MinMaxScaler

Region = sys.argv[1]

'''

Calculate overall cycling score using commute rate, CQI and crash rate with their respective weightings in the file msoa_scores.csv

with equation CycleScore for MSOA = 0.4? × Infrastructure Score
          + 0.30? × Participation Score
          + 0.30? × Safety Score

then add overall column to the file msoa_score.csv
 
'''

msoa_scores_path = f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv"
msoa_scores_csv = pd.read_csv(f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv", header=0, names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path'])


#Scale each one within its own range
scaler = MinMaxScaler()             
msoa_scores_csv["InfraScore"] = scaler.fit_transform(msoa_scores_csv[["index_space_syntax_length"]])
msoa_scores_csv["PartScore"]  = scaler.fit_transform(msoa_scores_csv[["commute_rate"]])

#Try inverting safety score, i.e. lower is better. i.e 1- norm_crash rate
msoa_scores_csv["InvertCrashScore"] = scaler.fit_transform(msoa_scores_csv[["crash_rate"]])

#print(msoa_scores_csv.loc[msoa_scores_csv['msoa'] == 'E02000834', 'InvertCrashScore'].values[0])
#print(msoa_scores_csv[msoa_scores_csv['InvertCrashScore'] == 0]['msoa'])
# Calculate the overall cycling score
msoa_scores_csv['OverallCycleScore'] = (0.40 * msoa_scores_csv['InfraScore'] +
                    0.30 * msoa_scores_csv['PartScore'] +
                    0.30 * msoa_scores_csv['InvertCrashScore'])


msoa_scores_csv.drop(columns=['InfraScore', 'PartScore', 'InvertCrashScore'], inplace=True)

# Save the updated DataFrame back to the CSV file
msoa_scores_csv.to_csv(msoa_scores_path, index=False)

