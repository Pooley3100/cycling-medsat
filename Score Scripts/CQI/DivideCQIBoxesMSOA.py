"""

Divide the whole of london CQI scores into MSOA level scores to make more efficient processing.

"""

import json
import os
import sys

Region = sys.argv[1]

# Load the GeoJSON file
file_path = f'/Users/mattpoole/OwnCodeProjs/THESIS/CyclingQualityIndex/Score Scripts/{Region}Datasets/cycling_quality_index_with_msoa.geojson'

with open(file_path, 'r') as file:
    cycling_quality_index = json.load(file)

    # Create a dictionary to store features by MSOA21CD
    features_dict = {}

    for feature in cycling_quality_index['features']:
        #print(feature)
        try:
            msoa_code = feature['properties']['msoa']
            #print(msoa_code)
            if msoa_code not in features_dict:
                features_dict[msoa_code] = []
            features_dict[msoa_code].append(feature)
        except KeyError:
            print(f"No 'msoa' key found in feature properties for {feature['properties']['id']}.")


output_dir = f'/Users/mattpoole/OwnCodeProjs/THESIS/CyclingQualityIndex/Datasets/{Region}_cqi_jsons_msoa'
os.makedirs(output_dir, exist_ok=True)

for msoa_code, features in features_dict.items():
    output_file_path = os.path.join(output_dir, f'{msoa_code}.json')
    with open(output_file_path, 'w') as output_file:
        json.dump({'features': features}, output_file, indent=4)

        
#print(features_dict)