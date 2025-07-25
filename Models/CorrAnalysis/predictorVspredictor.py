'''

A heatmap matrix for cycling predictors against themselves (predictor vs predictor)

'''

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

Region = 'London'

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Dependant variable(s)
health_metrics = ['msoa', 'diabetes', 'opioids', 'OME', 'total', 'asthma', 'hypertension', 'depression', 'anxiety']
df_y = pd.read_csv(
    f"../../MedSat/{Region}/msoa_medsat_scores.csv",
    header=0,
    names=health_metrics
)

# --- predictor variables
cycle_metrics = ['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path']
df_x = pd.read_csv(
    f"../../Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv",
    header=0,
    names=cycle_metrics
)

df = (df_y.merge(df_x, on="msoa", how="inner").dropna())


all_predictors = cycle_metrics[1:]

x_only = df[all_predictors]    
cor_matrix = x_only.corr(method="pearson")


plt.figure(figsize=(14,6))
# Also spectral colour but coolwarm looks more like chloropleth map
sns.heatmap(cor_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.4)
plt.title(f'predictor-vs-predictor correlation matrix in {Region}')
plt.xlabel('Cycling Metrics')
plt.ylabel('Cycling Metrics')
plt.tight_layout()
plt.show()