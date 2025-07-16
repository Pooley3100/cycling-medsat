"""

Applying single predictor regression models to find which cycling scores best correspond to a certain health metric.


"""

import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

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

#Pick diff ones from health_met and cyclet_met

X = df['index_space_syntax_length']
y = df['total']

# X = df[['index_space_syntax_length']]
# y = df['total']


# ordinary least squares
X = sm.add_constant(X)

model = sm.OLS(y, X).fit()

print(model.summary())

#Also a plot if desired:

sns.regplot(x='commute_rate', y='hypertension', data=df)
plt.title('Index Space Syntax Length vs total')
plt.xlabel('Index Space Syntax Length')
plt.ylabel('Total Prescription rate')
plt.grid(True)
plt.tight_layout()
plt.show()