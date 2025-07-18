'''

A correlation matrix showing the pearson correlation coefficients between each cycling related variable and health related variable across city and MSOA's.

heatmap matrix is useful here as well.
'''

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Region = 'London'

os.chdir(os.path.dirname(os.path.abspath(__file__)))
cities = pd.read_csv('../city_list.csv',header=0,names=['cities'])

cities_cor_matrix = {}
def cor_matrix(Region):
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
    return df_cor.corr().loc[health_metrics[1:],cycle_metrics[1:]]


city_matrices = {}
for city in cities['cities']:
    matrix = cor_matrix(city)
    if matrix is not None:
        city_matrices[city] = matrix


# One big super plot with subplots
fig, axes = plt.subplots(3, 3, figsize=(26, 13))
axes = axes.flatten()
for idx, (city, matrix) in enumerate(city_matrices.items()):
    sns.heatmap(matrix, ax=axes[idx], annot=True, fmt=".2f",
            cmap="coolwarm", vmin=-0.6, vmax=0.6)
    axes[idx].set_title(f"{city}")
    axes[idx].set_xlabel("Cycling Metrics")
    axes[idx].set_ylabel("Health Outcomes")

for j in range(idx + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()