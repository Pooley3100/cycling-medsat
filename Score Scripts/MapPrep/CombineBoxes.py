
import json
import os
import sys

# geojson_files = [
#     'london_box1.geojson',
#     'london_box2.geojson',
#     'london_box3.geojson',
#     'london_box4.geojson',
#     'london_box5.geojson',
#     'london_box6.geojson',
#     'london_box7.geojson',
#     'london_box8.geojson'
# ]
geojson_directory = os.path.join(os.path.dirname(__file__), f'../../Datasets/{sys.argv[1]}/')
geojson_files = [f for f in os.listdir(geojson_directory) if f.endswith('.geojson')]

# File to use in OSM-Cycling-Quality-Index
output_file = 'way_import.geojson'

seen_ids = set()
all_features = []

for file_name in geojson_files:
    file_path = os.path.join(os.path.dirname(__file__), f'../../Datasets/{sys.argv[1]}/' + file_name)
    with open(file_path, 'r') as geojson_file:
        data = json.load(geojson_file)
        for feature in data['features']:
            feature_id = feature.get('id')  # FIXED
            if feature_id and feature_id not in seen_ids:
                seen_ids.add(feature_id)
                all_features.append(feature)

combined_geojson = {
    "type": "FeatureCollection",
    "features": all_features
}

with open(output_file, 'w') as output_geojson_file:
    json.dump(combined_geojson, output_geojson_file, indent=2)

print(f"Combined GeoJSON saved to {output_file}")

