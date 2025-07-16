'''

A correlation matrix showing the pearson correlation coefficients between each cycling related variable and health related variable across city and MSOA's.

heatmap matrix is useful here as well.
'''

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

Region = 'Liverpool'

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


df_cor = df[health_metrics[1:] + cycle_metrics[1:]]
cor_matrix = df_cor.corr().loc[health_metrics[1:],cycle_metrics[1:]]

plt.figure(figsize=(14,6))
# Also spectral colour but coolwarm looks more like chloropleth map
sns.heatmap(cor_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.4)
plt.title(f'Correlation Matrix: Health Outcomes vs Cycling Metrics in {Region}')
plt.xlabel('Cycling Indicators')
plt.ylabel('Health Outcomes')
plt.tight_layout()
plt.show()