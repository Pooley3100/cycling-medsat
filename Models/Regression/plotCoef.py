''''

Coefficient plot of best multiple predictor regression model

'''

from matplotlib import pyplot as plt
import pandas as pd
import os
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
 

# Edit this <------
Region = 'Sheffield'

os.chdir(os.path.dirname(os.path.abspath(__file__)))

predictors = ['commute_rate', 'index_length', 'index_space_syntax_length', 'commute_path'] #Best one, drop threshold and crahs

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

x_scaler = StandardScaler()
y_scaler = StandardScaler()

X_scaled   = x_scaler.fit_transform(df[predictors])

# ==========
stds = pd.Series(x_scaler.scale_, index=predictors)

print("Raw standard deviations:")
print(stds)

# ======= Understanding what one std is

# will hold one row per health metric with predictor, coef, healthmetric and error
coef_rows  = []        

#Bit hard coded
def predict_names(predictor):
    if predictor == 'x1':
        return 'commute_rate'
    elif predictor == 'x2':
        return 'index_length'
    elif predictor == 'x3':
        return 'index_space_syntax_length'
    else:
        return 'commute_path'

for metric in health_metrics[1:]:             
    y_scaled    = y_scaler.fit_transform(df[[metric]]).ravel()
    if(metric == 'hypertension'):
        stds = pd.Series(y_scaler.scale_)
        print(f"y stds for hypertension = {stds}")

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
            'Err'         : 1.96 * errs[p] #1.96 gives 95% of proabable range of values
        })
        
coef_long = pd.DataFrame(coef_rows)

plt.figure(figsize=(14, 8))

# Create a dot plot with error bars
ax = sns.stripplot(
    data=coef_long,
    x='Coef',
    y='HealthMetric',
    hue='Predictor',
    dodge=True,
    order=health_metrics[1:],
    size=6
)

label_to_y = {label: i for i, label in enumerate(health_metrics[1:])}

def error_colour(predictor):
    if predictor == 'commute_rate':
        return 'blue'
    elif predictor == 'index_length':
        return 'orange'
    elif predictor == 'commute_path':
        return 'red'
    else:
        return 'green'
    
def get_dodge_offset(predictor):
    if predictor == 'commute_rate':
        return -0.3
    elif predictor == 'index_length':
        return -0.1
    elif predictor == 'commute_path':
        return +0.30
    else:
        return +0.1

#Overlay one horizontal error bar per estimate manually - maybe change to not hard coded later
for _, row in coef_long.iterrows():
    base_y = label_to_y[row["HealthMetric"]] 
    dodge = get_dodge_offset(row['Predictor'])
    y = base_y + dodge 
    ax.errorbar(
        x=row['Coef'],
        y=y,
        xerr=row['Err'],  
        fmt='none',
        ecolor=error_colour(row['Predictor']),
        capsize=3,
        linewidth=1,
        color=error_colour(row['Predictor'])
    )

ax.set_ylabel('Health metric')
ax.set_xlabel('Standardised coefficient')
ax.set_title('OLS coefficients with (95% confidence bars)')
plt.tight_layout()
plt.show()