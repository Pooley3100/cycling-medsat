'''

Plotting against various health metrics within the MSOA's for selectic cities

'''
import os
import pandas as pd
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

df_x = pd.read_csv(
    f"../../Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv",
    header=0,
    names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path']
)

df = (df_y.merge(df_x, on="msoa", how="inner").dropna())


#Current dependant to compare
dependant_in = 'commute_rate'

plt.figure(figsize=(15, 10))

for i, metric in enumerate(health_metrics[1:]):
    plt.subplot(3, 3, i + 1)
    plt.scatter(df[dependant_in], df[metric], alpha=0.5)
    plt.title(f'{metric.capitalize()} vs {dependant_in}')
    plt.xlabel(dependant_in)
    plt.ylabel(metric.capitalize())
    plt.grid(True)

plt.tight_layout()
plt.show()

