"""

Applying single predictor regression models to find which cycling scores best correspond to a certain health metric.


"""

import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Change this <-----
Region = 'London'
x_label= 'commute_rate'
y_label= 'diabetes'
#Threshold Score (ScoreCQI), Crash Rate, Commute Rate, CQI Mean (index_length), CQI Space Syntax (index_space_syntax_length) and Commute Path.

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

X = df[x_label]
# scaler = MinMaxScaler()
# X = scaler.fit_transform(df[[x_label]])
y = df[y_label]

# ordinary least squares
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

print(model.summary())

#Also a plot

sns.regplot(x=x_label, y=y_label, data=df)
plt.title(f'{x_label} vs {y_label} in {Region}')
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.grid(True)
plt.tight_layout()
plt.show()