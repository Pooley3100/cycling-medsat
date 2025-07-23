import pandas as pd
import matplotlib.pyplot as plt
import os


# Change <======

x_label = 'commute_rate_avg'
y_label = 'hypertension_avg'

#=========

os.chdir(os.path.dirname(__file__))

city_stats = pd.read_csv('desc_metrics_summary.csv')

#More just a way to select
Options = "diabetes_avg,diabetes_range,opioids_avg,opioids_range,OME_avg,OME_range,total_avg,total_range,asthma_avg," \
"asthma_range,hypertension_avg,hypertension_range,depression_avg,depression_range,anxiety_avg,anxiety_range," \
"ScoreCQI_avg,ScoreCQI_range,crash_rate_avg,crash_rate_range,commute_rate_avg,commute_rate_range," \
"OverallCycleScore_avg,OverallCycleScore_range,ScoreCQIMean_avg,ScoreCQIMean_range,index_length_avg," \
"index_length_range,index_space_syntax_avg,index_space_syntax_range,index_space_syntax_length_avg," \
"index_space_syntax_length_range,commute_path_avg,commute_path_range"
Options = Options.split(',')

labels = city_stats['city']

x = city_stats[x_label]
y = city_stats[y_label]

plt.figure(figsize=(8, 8))
plt.scatter(x, y)

# lable point with city name
for i, label in enumerate(labels):
    plt.annotate(label, (x.iloc[i], y.iloc[i]), fontsize=14)

plt.title(f'{y_label} against {x_label} by City')
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.grid(True)
plt.show()
