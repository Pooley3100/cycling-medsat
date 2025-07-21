''''

Coefficient plot of best multiple predictor regression model = ['index_space_syntax_length','commute_path', 'commute_rate']
}

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
 


# Edit this <------
Region = 'London'
x_label_features = 'index_space_syntax_length'

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Different predictor combinations
# cycle_in = cycle_metrics[1:] not ideal this one, as some scores build upon others, such as space syntax use CQI score and commute path uses crash and commute rate already
features = {
    'Mean_Raw' : ['ScoreCQIMean', 'crash_rate', 'commute_rate'],
    'Mean_Length' : ['index_length', 'crash_rate', 'commute_rate'],
    'space_syntax' : ['index_space_syntax', 'crash_rate', 'commute_rate'],
    'VIF-Test' : ['ScoreCQI', 'crash_rate', 'ScoreCQIMean'],
    'index_space_syntax_length' : ['index_space_syntax_length','commute_path', 'commute_rate']
}
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

# And the model --------------------------

scaler = StandardScaler()

X_scaled   = scaler.fit_transform(df[features[x_label_features]])     

coef_rows  = []          # will hold one row per health metric

def predict_names(predictor):
    if predictor == 'x1':
        return 'index_space_syntax_length'
    elif predictor == 'x2':
        return 'commute_path'
    else:
        return 'commute_rate'

for metric in health_metrics[1:]:             
    y_scaled    = scaler.fit_transform(df[[metric]]).ravel()
    X_in  = sm.add_constant(X_scaled)       
    res   = sm.OLS(y_scaled, X_in).fit()
    
    names  = res.model.exog_names        
    
    params = pd.Series(res.params, index=names).drop('const')
    errs   = pd.Series(res.bse, index=names).drop('const')
    
    for p, val in params.items():
        coef_rows.append({
            'HealthMetric': metric,
            'Predictor'   : predict_names(p),
            'Coef'        : val,
            'Err'         : errs[p]
        })
        
coef_long = pd.DataFrame(coef_rows)

plt.figure(figsize=(14, 8))

# Create a dot plot with error bars
ax = sns.pointplot(
    data=coef_long,
    x='Coef',
    y='HealthMetric',
    hue='Predictor',
    join=False,
)

ypos = dict(zip(
    [t.get_text() for t in ax.get_yticklabels()],
    ax.get_yticks()
)) 

def error_colour(predictor):
    if predictor == 'x1':
        return 'blue'
    elif predictor == 'x2':
        return 'orange'
    else:
        return 'green'
    
#Overlay one horizontal error bar per estimate manually
for _, row in coef_long.iterrows():
    ax.errorbar(
        x=row['Coef'],
        y=ypos[row['HealthMetric']],
        xerr=row['Err'],  
        fmt='none',
        ecolor=error_colour(row['Predictor']),
        capsize=3,
        linewidth=1
    )

ax.set_ylabel('Health metric')
ax.set_xlabel('Standardised coefficient')
ax.set_title('OLS coefficients with std Error bars')
plt.tight_layout()
plt.show()