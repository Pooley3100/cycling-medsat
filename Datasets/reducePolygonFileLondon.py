import os
import pandas as pd
import geopandas as gpd
'''

Reduce london polygon file for GitHub

features kept in each property are just index_10

'''

# First find folders required, then check if {Region}_cqu_jsons_msoa_REDUCED already exists if not create folder

os.chdir(os.path.dirname(__file__))
current_directory = os.getcwd()

import geopandas as gpd
import os

input_file = "Filtered_London_Polygon.geojson"
output_file_1 = "Filtered_London_Polygon_ONE.geojson"
output_file_2 = "Filtered_London_Polygon_TWO.geojson"

gdf = gpd.read_file(input_file)

split_index = len(gdf) // 2
gdf_part1 = gdf.iloc[:split_index]
gdf_part2 = gdf.iloc[split_index:]

gdf_part1.to_file(output_file_1, driver="GeoJSON")
gdf_part2.to_file(output_file_2, driver="GeoJSON")

print(f"File 1 saved: {output_file_1}")
print(f"File 2 saved: {output_file_2}")

