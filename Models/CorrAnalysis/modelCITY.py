'''

A graph between cities showing the pearson correlation coefficients between each cycling related variable and health related variable across city

'''

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv('../DescComp/desc_metrics_summary.csv')


health_metrics = [
    "diabetes_avg", "diabetes_range", "opioids_avg", "opioids_range", 
    "OME_avg", "OME_range", "total_avg", "total_range", 
    "asthma_avg", "asthma_range", "hypertension_avg", "hypertension_range", 
    "depression_avg", "depression_range", "anxiety_avg", "anxiety_range", 
]



cycling_metrics = ["ScoreCQI_avg", "ScoreCQI_range", "crash_rate_avg", "crash_rate_range", 
    "commute_rate_avg", "commute_rate_range", "OverallCycleScore_avg", 
    "OverallCycleScore_range", "ScoreCQIMean_avg", "ScoreCQIMean_range", 
    "index_length_avg", "index_length_range", "index_space_syntax_avg", 
    "index_space_syntax_range", "index_space_syntax_length_avg", 
    "index_space_syntax_length_range", "commute_path_avg", "commute_path_range"
]

#Pick from above
health_metric = 'hypertension_avg'
cycling_metric = 'commute_rate_avg'

plt.figure(figsize=(10, 6))
plt.scatter(df[cycling_metric], df[health_metric], color='teal')


for i, row in df.iterrows():
    plt.text(row[cycling_metric]+0.05, row[health_metric], row['city'], fontsize=10)

plt.title(f'{health_metric} vs {cycling_metric}')
plt.xlabel(cycling_metric)
plt.ylabel(health_metric)
plt.grid(True)
plt.tight_layout()
plt.show()