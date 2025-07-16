'''

Plot of some cycle scores against mediant income

'''
import matplotlib.pyplot as plt

import pandas as pd
import os



os.chdir(os.path.dirname(os.path.abspath(__file__)))

Region = 'Sheffield'
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
# --ad in income confound
df_x_conf = pd.read_csv(f'{Region}_msoa_income_scores.csv', header=0, names=['msoa','income'])

df = (df_y.merge(df_x, on="msoa", how="inner")
    .merge(df_x_conf, on="msoa", how="inner")
    .dropna())


y = 'commute_path'
x = 'income'
    

plt.figure(figsize=(12, 6))
plt.scatter(df[x], df[y], alpha=0.8)
plt.title(f'{y} Scores vs Income')
plt.xlabel('Income')
plt.ylabel(f'{y} Scores')
plt.grid(True)
plt.show()