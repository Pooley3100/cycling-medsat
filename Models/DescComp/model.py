'''

Here running more descriptive analysis of the data obtained by MSOA and by City

These are

1) Mean and range of cycling metrics and health outcomes by city
2) City wide average vs Heatlh
3) Within City Variations


out = desc_metrics.csv

'''
import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

cities = pd.read_csv('../city_list.csv',header=0,names=['cities'])

city_dict_results = cities.set_index('cities').T.to_dict()

health_metrics = ['msoa', 'diabetes', 'opioids', 'OME', 'total', 'asthma', 'hypertension', 'depression', 'anxiety']
cycle_scores = ['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path']
res_cols = ['city']
for health_met in health_metrics[1:]:
    res_cols.append(health_met+'_avg')
    res_cols.append(health_met+'_range')
for cycle_score in cycle_scores[1:]:
    res_cols.append(cycle_score+'_avg')
    res_cols.append(cycle_score+'_range')

summary_df = pd.DataFrame(columns=res_cols)

for city in cities['cities']:
    df_y = pd.read_csv(
        f'../../MedSat/{city}/msoa_medsat_scores.csv',
        header=0,
        names=health_metrics
    )
    # --- predictor variables
   
    df_x = pd.read_csv(
        f"../../Score Scripts/{city}Datasets/{city}_msoa_scores.csv",
        header=0,
        names=cycle_scores
    )

    #Average and range of each score by city

    row_data = {'city': city}

    for health_met in health_metrics[1:]:
        avg = df_y[health_met].mean()
        range_val = df_y[health_met].max() - df_y[health_met].min()
        print(f'City {city} has a {health_met} mean of {avg} and a range of {range_val}')
        row_data[health_met + '_avg'] = avg
        row_data[health_met + '_range'] = range_val

    for cycle_score in cycle_scores[1:]:
        avg = df_x[cycle_score].mean()
        range_val = df_x[cycle_score].max() - df_x[cycle_score].min()
        print(f'City {city} has a {cycle_score} mean of {avg} and a range of {range_val}')
        row_data[cycle_score + '_avg'] = avg
        row_data[cycle_score + '_range'] = range_val

    summary_df = pd.concat([summary_df, pd.DataFrame([row_data])], ignore_index=True)



summary_df.to_csv('desc_metrics_summary.csv', index=False)
