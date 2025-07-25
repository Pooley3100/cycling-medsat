'''

Plot of some cycle scores against mediant income

'''
import matplotlib.pyplot as plt

import pandas as pd
import os
import statsmodels.api as sm
import seaborn as sns
from sklearn.preprocessing import StandardScaler



os.chdir(os.path.dirname(os.path.abspath(__file__)))

Region = 'London'
y = 'commute_rate'
x = 'income'

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



scaler = StandardScaler()
X_Scaled = scaler.fit_transform(df[[x]])

X = sm.add_constant(X_Scaled)
model = sm.OLS(df[y], X).fit()
print(model.summary())

#Also a plot
sns.regplot(x=x, y=y, data=df)
plt.title(f'{x} vs {y} in {Region}')
plt.xlabel(x)
plt.ylabel(y)
plt.grid(True)
plt.tight_layout()
plt.show()
