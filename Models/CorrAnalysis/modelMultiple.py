'''

A correlation matrix showing the pearson correlation coefficients between each cycling
related variable and health related variable across ALL cities
'''
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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


#One big super plot with subplots, clamp 0.6 works well
fig, axes = plt.subplots(3, 3, figsize=(26, 13))
axes = axes.flatten()
for id, (city, matrix) in enumerate(city_matrices.items()):
    sns.heatmap(matrix, ax=axes[id], annot=True, fmt=".2f",
            cmap="coolwarm", vmin=-0.6, vmax=0.6, cbar=False)
    axes[id].set_title(f"{city}")
    axes[id].set_xlabel("Cycling Metrics")
    if id in [1, 2, 4, 5]:  #Hide y-axis for some plots
        axes[id].set_ylabel("")
        axes[id].yaxis.set_visible(False)

for i in range(id + 1, len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.show()