"""

Plotting average resulsts for more qualitative initial comparisons.


Create a bar chart for each city, displaying 
"""
import pandas as pd
import matplotlib.pyplot as plt
import os


# Change this========
y1 = 'commute_rate_avg' #Cycle
y2 = 'diabetes_avg' # Health

#=======

os.chdir(os.path.dirname(__file__))

city_stats = pd.read_csv('desc_metrics_summary.csv')

# Sort cities for better visualization 
city_stats = city_stats.sort_values(by=y1, ascending=False)

fig, ax1 = plt.subplots(figsize=(14, 6))

#More just a way to select
Options = "diabetes_avg,diabetes_range,opioids_avg,opioids_range,OME_avg,OME_range,total_avg,total_range,asthma_avg," \
"asthma_range,hypertension_avg,hypertension_range,depression_avg,depression_range,anxiety_avg,anxiety_range," \
"ScoreCQI_avg,ScoreCQI_range,crash_rate_avg,crash_rate_range,commute_rate_avg,commute_rate_range," \
"OverallCycleScore_avg,OverallCycleScore_range,ScoreCQIMean_avg,ScoreCQIMean_range,index_length_avg," \
"index_length_range,index_space_syntax_avg,index_space_syntax_range,index_space_syntax_length_avg," \
"index_space_syntax_length_range,commute_path_avg,commute_path_range"
Options = Options.split(',')

#Dual axis bar plot
ax1.bar(city_stats['city'], city_stats[y1], color='lightblue', label=y1)
ax1.set_ylabel(y1, color='blue')
ax1.set_xlabel('City')
ax1.set_ylim(bottom=city_stats[y1].min() * 0.8)#y lim 80%

# second y-axis for {the average diabetes prescription rate}
ax2 = ax1.twinx()
ax2.plot(city_stats['city'], city_stats[y2], color='red', marker='o', label=y2)
ax2.set_ylabel(y2, color='red')

plt.title(f'{y1} vs {y2}by City')
fig.tight_layout()
plt.show()
