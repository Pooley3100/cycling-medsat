"""
Sort through each way feature produced by OSM-Cycling-Quality-Index

Then find which msoa21 each way is within and add to feature

Produce another file 'msoa-cqi' which is the percent over X score within that msoa

WARNING: This will likely take at least two hours to run

"""
from shapely.geometry import Point, shape
import json
import os
import sys
import pandas as pd
import geopandas as gpd

Region = sys.argv[1]
# Region = 'Birmingham'

msoa_dict = {}

# Gets postcode of a way in the feature
def get_msoa(feature, name):
    # Calculate the midpoint if the feature is a LineString
    coordinates = feature['geometry']['coordinates']
    if feature['geometry']['type'] == 'LineString' and len(coordinates) > 1:
        # Calculate the average of all longitude and latitude values, is this the best way???
        avg_lon = sum(coord[0] for coord in coordinates) / len(coordinates)
        avg_lat = sum(coord[1] for coord in coordinates) / len(coordinates)
        # Flip so that it works
        midpoint = [avg_lon, avg_lat]
        print(f"Feature ID: {name}")
        print(f"Midpoint: {midpoint}")
        msoa = get_msoa_from_coordinate(midpoint)
        print(f"For {name} msoa = {msoa}")
        if msoa in msoa_dict:
            msoa_dict[msoa].append(feature)
        else:
            msoa_dict[msoa] = [feature]
    else:
        print(f"Feature ID: {name} is not a valid LineString or has insufficient coordinates.")
        print(f"Coordinates: {coordinates}")

    return msoa if msoa else None

def create_msoa_polygons():
    # count = 0
    for index, feature in msoa_data.iterrows():
        polygon = feature['geometry']  # Use the geometry directly from the GeoDataFrame
        polygons.append((polygon, feature['MSOA21CD']))

def get_msoa_from_coordinate(coordinate):
    # Function to find which MSOA a coordinate belongs to
    point = Point(coordinate)  # Create a Shapely Point object
    #point.crs = 'EPSG:4326'  # Set the CRS if necessary, typically WGS84
    for polygonTuple in polygons:
        polygon = polygonTuple[0]
        if polygon.contains(point):  # Check if the point is within the polygon
            return polygonTuple[1] # Return the MSOA name (or use another property like 'msoa21cd')
    return None  # Return None if no MSOA contains the point

# Load the GeoJSON file
file_path = os.path.join(os.path.dirname(__file__), f'../{Region}Datasets/cycling_quality_index.geojson')
with open(file_path, 'r') as file:
    data = json.load(file)

# Load the MSOA GeoJSON , first option would be a lot faster if reduce shape file is obtained that works with epsg 4326
# msoa_file_path = os.path.join(os.path.dirname(__file__), f'../../Datasets/Filtered_{Region}_Polygon.geojson')
msoa_file_path = os.path.join(os.path.dirname(__file__), f'../../Datasets/Middle_layer_Super_Output_Areas_December_2021_Boundaries_EW_BGC_V3.geojson')
msoa_data = None
polygons = []

with open(msoa_file_path, 'r') as msoa_file:
    msoa_data = gpd.read_file(msoa_file)
    msoa_data = msoa_data.to_crs(epsg=4326)

create_msoa_polygons()

for feature in data['features']:
    name = feature['properties']['name']
    
    msoa = get_msoa(feature, name)
    
    if msoa:
        feature['properties']['msoa'] = msoa
    #print(feature)


msoa_scores = {}
#Now calculate a score for each msoa (threshold ones)
for msoa in msoa_dict.items():
    total_good = 0
    features = msoa[1]
    total_ways = len(features)
    for way in features:
        if way['properties']['index'] >= 55:
            total_good +=1
    score = (total_good / total_ways) * 100
    print(f'MSOA {msoa[0]} has a score of {score}')
    msoa_scores[msoa[0]] = score


# Add MSOA score to each feature's properties
for feature in data['features']:
    msoa = feature['properties'].get('msoa')  # Get the MSOA for the feature
    if msoa and msoa in msoa_scores:
        feature['properties']['msoa_threshold_score'] = msoa_scores[msoa]  
    else:
        feature['properties']['msoa_threshold_score'] = None  

# Write the updated GeoJSON back to a file
output_geojson_path = os.path.join(os.path.dirname(__file__), f'../{Region}Datasets/cycling_quality_index_with_msoa.geojson')
with open(output_geojson_path, 'w') as geojson_file:
    json.dump(data, geojson_file, indent=2)

print(f'Updated GeoJSON with MSOA scores has been written to {output_geojson_path}')