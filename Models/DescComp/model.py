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

for city in cities['cities']:
    health_metrics = ['msoa', 'diabetes', 'opioids', 'OME', 'total', 'asthma', 'hypertension', 'depression', 'anxiety']
    df_y = pd.read_csv(
        f'../../MedSat/{city}/msoa_medsat_scores.csv',
        header=0,
        names=health_metrics
    )
    # --- predictor variables
    cycle_scores = ['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path']
    df_x = pd.read_csv(
        f"../../Score Scripts/{city}Datasets/{city}_msoa_scores.csv",
        header=0,
        names=cycle_scores
    )

    #Average and range of each score by city
    for health_met in health_metrics[1:]:
        print(f'City {city} has a {health_met} mean of {df_y[health_met].mean()} and a range of {df_y[health_met].max() - df_y[health_met].min()}')

    for cycle_score in cycle_scores[1:]:
        print(f'City {city} has a {cycle_score} mean of {df_x[cycle_score].mean()} and a range of {df_x[cycle_score].max() - df_x[cycle_score].min()}')
