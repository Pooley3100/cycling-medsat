"""

Takes new scores for each way and update to overall MSOA level and updates file

"""
import os
import json
import sys
import pandas as pd

Region = sys.argv[1]

file_dir = f'Datasets/{Region}_cqi_jsons_msoa/'
msoa_score_dict = {}

#Length weighted is= sum(quality*length) / sum(length) for each msoa

for filename in os.listdir(file_dir):
    if filename.endswith('.json'): 
        with open(os.path.join(file_dir, filename), 'r') as json_file:
            ways = 0
            index_length = 0
            index_space_syntax = 0
            index_space_syntax_length = 0
            length = 0
            data = json.load(json_file)
            msoa = data['features'][0]['properties']['msoa']
            for feature in data['features']:
                ways += 1
                length += feature['properties']['length']
                index_length += feature['properties']['index_length']
                index_space_syntax += feature['properties']['index_space_syntax']
                index_space_syntax_length += feature['properties']['index_space_syntax_length']
            if ways > 0:
                length_weighted = index_length / length
                avg_space_syntax = index_space_syntax / ways
                avg_space_syntax_length = index_space_syntax_length / length
                msoa_score_dict[msoa] = (length_weighted, avg_space_syntax, avg_space_syntax_length)

                


#Add to msoa_scores.csv file
msoa_scores_path = f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv"
msoa_scores_csv = pd.read_csv(f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv", header=0, names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path'])

msoa_scores_csv["index_length"] = msoa_scores_csv["msoa"].map(lambda x: msoa_score_dict.get(x, (0, 0, 0))[0]).fillna(0).astype(float)
msoa_scores_csv["index_space_syntax"] = msoa_scores_csv["msoa"].map(lambda x: msoa_score_dict.get(x, (0, 0, 0))[1]).fillna(0).astype(float)
msoa_scores_csv["index_space_syntax_length"] = msoa_scores_csv["msoa"].map(lambda x: msoa_score_dict.get(x, (0, 0, 0))[2]).fillna(0).astype(float)

msoa_scores_csv.to_csv(msoa_scores_path, index=False)
print("Space Syntax (And Index Length) Scores added!")