'''

Make regression model with confounding factors to see if they are key drive

'''

from matplotlib import pyplot as plt
import pandas as pd
import os
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

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
# --ad in income confound
df_x_conf = pd.read_csv(f'{Region}_msoa_income_scores.csv', header=0, names=['msoa','income'])

df = (df_y.merge(df_x, on="msoa", how="inner")
    .merge(df_x_conf, on="msoa", how="inner")
    .dropna())

predictors = ['commute_rate', 'index_length', 'index_space_syntax_length', 'commute_path','income']

scaler = StandardScaler()

def regression_model():
    X_in  = scaler.fit_transform(df[predictors])
    X_in  = sm.add_constant(X_in)                                  
    y      = df['hypertension']
    model  = sm.OLS(y, X_in).fit()
    print(model.summary())


regression_model()
