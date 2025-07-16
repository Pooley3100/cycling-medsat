'''

Make regression model with confounding factors to see if they are key drive

'''
'''

Plot of some cycle scores against mediant income

'''

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

features = {
    'Mean_Raw' : ['ScoreCQIMean', 'crash_rate', 'commute_rate'],
    'Mean_Length' : ['index_length', 'crash_rate', 'commute_rate'],
    'space_syntax' : ['index_space_syntax', 'crash_rate', 'commute_rate'],
    'index_space_syntax_length' : ['index_space_syntax_length','crash_rate', 'commute_rate']
}

scaler = StandardScaler()


def regression_model():
    X_in  = scaler.fit_transform(df[features['index_space_syntax_length']])
    X_in  = sm.add_constant(X_in)                                  
    y      = df['hypertension']
    #Ordinary least squares
    model  = sm.OLS(y, X_in).fit()
    print(model.summary())


# regression_model()



#Building the coefficient matrix for every health outcome
predict_metrics = cycle_metrics[1:] + ['income']
coef_matrix = pd.DataFrame(index=health_metrics[1:], columns=predict_metrics)


for h in health_metrics[1:]:
    y = df[h]
    y_norm = scaler.fit_transform(df[[h]])
    #Standardise each independent varaible feature
    x_norm = scaler.fit_transform(df[predict_metrics]) 
    #Need to convert back to dataframe or else assingments get lost
    x_norm = pd.DataFrame(x_norm, columns=predict_metrics)

    #intercept to independatn variables (part 1 of fitting regression)
    x_norm = sm.add_constant(x_norm)
    #Part 2 of fitting is orignary least squares
    res = sm.OLS(y_norm, x_norm).fit()

    coef_matrix.loc[h] = res.params[predict_metrics]

print(coef_matrix)


plt.figure(figsize=(14,6))
# Also spectral colour but coolwarm looks more like chloropleth map
sns.heatmap(coef_matrix.astype(float), annot=True, fmt=".2f", center=0, cmap='coolwarm', linewidths=0.4)
plt.title(f'Coefficient Matrix comparing health outcomees to cycling scores in {Region}')
plt.xlabel('Cycling Indicators')
plt.ylabel('Health Outcomes')
plt.tight_layout()
plt.show()