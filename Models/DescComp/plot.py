"""

Plotting average resulsts for more qualitative initial comparisons.


Create a bar chart for each city, displaying 
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(__file__))

city_stats = pd.read_csv('desc_metrics_summary.csv')

# Sort cities for better visualization 
city_stats = city_stats.sort_values(by='commute_rate_avg', ascending=False)

fig, ax1 = plt.subplots(figsize=(14, 6))

# Options: diabetes_avg,diabetes_range,opioids_avg,opioids_range,OME_avg,OME_range,total_avg,total_range,asthma_avg,asthma_range,hypertension_avg,hypertension_range,depression_avg,depression_range,anxiety_avg,anxiety_range,ScoreCQI_avg,ScoreCQI_range,crash_rate_avg,crash_rate_range,commute_rate_avg,commute_rate_range,OverallCycleScore_avg,OverallCycleScore_range,ScoreCQIMean_avg,ScoreCQIMean_range,index_length_avg,index_length_range,index_space_syntax_avg,index_space_syntax_range,index_space_syntax_length_avg,index_space_syntax_length_range,commute_path_avg,commute_path_range

# Bar plot for {average cycling commute rate}
ax1.bar(city_stats['city'], city_stats['commute_rate_avg'], color='tab:blue', label='Cycling Commute Rate')
ax1.set_ylabel('Avg Cycling Commute Rate', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_xlabel('City')

# second y-axis for {the average diabetes prescription rate}
ax2 = ax1.twinx()
#ax2.plot(city_stats['city'], city_stats['diabetes_avg'], color='tab:red', marker='o', label='Diabetes Prescription Rate')
ax2.plot(city_stats['city'], city_stats['hypertension_avg'], color='tab:red', marker='o', label='Hypertension Prescription Rate')
ax2.set_ylabel('Avg Diabetes Prescription Rate', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title('Cycling Commute Rate vs Diabetes Prescription Rate by City')
fig.tight_layout()
plt.show()
