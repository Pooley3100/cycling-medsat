"""

Applying regression models to find which cycling scores best correspond to a certain health metric.

currently using MedSat/london_msoa_medsat_scores.csv

and Score Scripts/msoa_scores_zscaled.csv

"""

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler


os.chdir(os.path.dirname(os.path.abspath(__file__)))

cities = pd.read_csv('../city_list.csv',header=0,names=['cities'])

scaler = StandardScaler()


city_matrices = {}
#Building the coefficient matrix for every health outcome for subplts
def build_matrix(df):
    coef_matrix = pd.DataFrame(index=health_metrics[1:], columns=cycle_metrics[1:])

    for h in health_metrics[1:]:
        y = df[h]
        y_norm = scaler.fit_transform(df[[h]])
        x_norm = scaler.fit_transform(df[cycle_metrics[1:]]) 
        x_norm = pd.DataFrame(x_norm, columns=cycle_metrics[1:])

        #intercept to independatn variables (part 1 of fitting regression)
        x_norm = sm.add_constant(x_norm)
        #Part 2 of fitting is orignary least squares
        res = sm.OLS(y_norm, x_norm).fit()

        coef_matrix.loc[h] = res.params[cycle_metrics[1:]]

    city_matrices[city] = coef_matrix.astype(float)


for city in cities['cities']:
    # --- Dependant variable(s)
    health_metrics = ['msoa', 'diabetes', 'opioids', 'OME', 'total', 'asthma', 'hypertension', 'depression', 'anxiety']
    df_y = pd.read_csv(
        f"../../MedSat/{city}/msoa_medsat_scores.csv",
        header=0,
        names=health_metrics
    )

    # --- predictor variables
    cycle_metrics = ['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path']
    df_x = pd.read_csv(
        f"../../Score Scripts/{city}Datasets/{city}_msoa_scores.csv",
        header=0,
        names=cycle_metrics
    )

    df = (df_y.merge(df_x, on="msoa", how="inner").dropna())
    
    # regression_model(df)
    build_matrix(df)
 

# One big super plot with subplots
fig, axes = plt.subplots(3, 3, figsize=(26, 13))

for idx, (ax, (city, matrix)) in enumerate(zip(axes.flat, city_matrices.items())):
    sns.heatmap(matrix, ax=ax, annot=True, fmt=".2f", cmap="coolwarm", center=0)
    ax.set_title(f"{city}")
    ax.set_xlabel("Cycling Metrics")
    ax.set_ylabel("Prescription Rates")
    if idx in [1, 2, 4, 5]:
        ax.set_ylabel("")
        ax.yaxis.set_visible(False)

for ax in axes.flat[len(city_matrices):]:
    fig.delaxes(ax)

plt.tight_layout()
plt.show()
