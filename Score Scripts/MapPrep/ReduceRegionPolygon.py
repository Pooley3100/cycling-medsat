'''

Take the sys.argv[1] path to region msoa's and create polygon file of only those msoa's

'''

import os
import json
import sys
import csv
import geopandas as gpd
from shapely.geometry import shape

# File paths
msoa_file_path = os.path.join(os.path.dirname(__file__), f'../../Datasets/Middle_layer_Super_Output_Areas_December_2021_Boundaries_EW_BGC_V3.geojson')
csv_file_path = os.path.join(os.path.dirname(__file__), f'../{sys.argv[2]}Datasets/{sys.argv[1]}')
output_file_path = os.path.join(os.path.dirname(__file__), f'../../Datasets/Filtered_{sys.argv[2]}_Polygon.geojson')

# Load the MSOA GeoJSON file
with open(msoa_file_path, 'r') as msoa_file:
    msoa_data = gpd.read_file(msoa_file)
    msoa_data = msoa_data.to_crs(epsg=4326)

# Load the list of MSOA codes from the CSV file
msoa_codes_to_keep = set()
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)#skip header
    for row in csv_reader:
        msoa_codes_to_keep.add(row[0])

# Filter the GeoJSON features
codes_to_keep = set(msoa_codes_to_keep)       
filtered_gdf = msoa_data.loc[
    msoa_data["MSOA21CD"].isin(codes_to_keep)
].copy()

# filtered_geojson = {
#     "type": "FeatureCollection",
#     "features": filtered_features
# }


# with open(output_file_path, 'w') as output_file:
#     # Convert filtered features to GeoDataFrame
#     filtered_gdf = gpd.GeoDataFrame.from_features(filtered_geojson)

#     # Save the filtered GeoDataFrame to a GeoJSON file
#     filtered_gdf.to_file(output_file_path, driver='GeoJSON')

filtered_gdf.to_file(
    output_file_path,
    driver="GeoJSON",
    index=False          # prevents “id”: 0,1,2… being written
)

print(f"Filtered GeoJSON saved to {output_file_path}")