"""

Update each of the MSOA's in output_jsons_msoa to calculate average score for each msoa instead of above a threshold. Add to msoa_scores.csv a comlumn with ScoreCQIMean

"""

import json
import os
import pandas as pd
import sys
Region = sys.argv[1]

# Load the GeoJSON file
file_path = f'Datasets/{Region}_cqi_jsons_msoa/'
msoa_dict_score = {}
for filename in os.listdir(file_path):
        msoa = ''
        total_ways = 0
        total_score = 0
        if filename.endswith('.json'):  # Adjust the extension as needed
            with open(os.path.join(file_path, filename), 'r') as geojson_file:
                data = json.load(geojson_file)
                
                msoa = data['features'][0]['properties']['msoa']
                for feature in data['features']:
                     total_score += feature['properties']['index']
                     total_ways += 1
        msoa_dict_score[msoa] = total_score / total_ways

# # Set the directory to the current script's location
# current_directory = os.path.dirname(os.path.abspath(__file__))
# os.chdir(current_directory)

#Add to msoa_scores.csv file
msoa_scores_path = f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv"
msoa_scores_csv = pd.read_csv(f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv", header=0, names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path'])

msoa_scores_csv["ScoreCQIMean"] = msoa_scores_csv["msoa"].map(msoa_dict_score).fillna(0).astype(float)
msoa_scores_csv.to_csv(msoa_scores_path, index=False)
print("Average scores added!")





