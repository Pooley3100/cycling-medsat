"""

Applying regression models to find which cycling scores best correspond to a certain health metric.

currently using MedSat/london_msoa_medsat_scores.csv

and Score Scripts/msoa_scores_zscaled.csv

"""

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import os
import statsmodels.api as sm

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Dependant variable(s)
df_y = pd.read_csv(
    "../MedSat/london_msoa_medsat_scores.csv",
    header=0,
    names=['msoa', 'diabetes', 'opioids', 'OME', 'total', 'asthma', 'hypertension', 'depression', 'anxiety']
)

# --- predictor variables

df_x = pd.read_csv(
    "../Score Scripts/msoa_scores.csv",
    header=0,
    names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path']
)

df = (df_y.merge(df_x, on="msoa", how="inner").dropna())

print(df)

#Current
features = {
    'Mean' : ["ScoreCQIMean"],
    'index_space_syntax_length' : ['index_space_syntax_length'],
    'commute_rate' : ['commute_rate'], #Likely the best <--
    'Core Three' : ['ScoreCQIMean','commute_rate','crash_rate'],
    'Core Three Space Syntax' : ['index_space_syntax', 'commute_rate','crash_rate'],
    'Core Three Space Syntax Length' : ['index_space_syntax_length', 'commute_rate','crash_rate']
}

y     = df["total"]

#Split into subsets for test and train
kf = KFold(n_splits=5, shuffle=True, random_state=6)
scores = {}

for name, cols in features.items():
    X = df[cols]
    regr = LinearRegression()
    cv_rmse = -cross_val_score(
        regr, X, y,
        cv=kf,
        scoring="neg_root_mean_squared_error"
        # + fit_params={"sample_weight": w}  << add if you have a weight column
    )
    scores[name] = (cv_rmse.mean(), cv_rmse.std())

print("Model   |  RMSE  |  ±1 SD")
for k,v in scores.items():
    print(f"{k:<7} | {v[0]:6.3f} | {v[1]:5.3f}")