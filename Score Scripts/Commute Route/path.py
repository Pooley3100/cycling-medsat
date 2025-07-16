"""

Final One, Use 2021 Census Origin Destination workplace (Warning COVID!) to find most popular route of commute and average index_space_syntax score along route

Surpisingly not that slow to run
"""
import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import Point, shape, LineString
import sys
import os
from sklearn.preprocessing import MinMaxScaler

Region = sys.argv[1]

# # Set the working directory to two levels up for DEBUG
# os.chdir(os.path.join(os.path.dirname(__file__), '../../'))

#Create MSOA List
msoa = pd.read_csv(f'Score Scripts/{Region}Datasets/{Region}MSOA.csv', header=0, names=['MSOA21CD', 'MSOA21NM'])

#Step 1, Take dataset and find for each MSOA (In London Currently) and look for most popular commute route for the MSOA
ori_dest = pd.read_csv('Score Scripts/Commute Route/ODWP01EW_MSOA.csv',
                       header=0,
                       names=['msoa_origin', 
                              'Middle layer Super Output Areas label', 
                              'msoa_dest', 
                              'MSOA of workplace label', 
                              'Place of work indicator (4 categories) code', 
                              'Place of work indicator (4 categories) label', 
                              'Count']
                       )

msoa_pop = {}
for msoa_cd in msoa['MSOA21CD']:
    subset_data = ori_dest[ori_dest['msoa_origin'] == msoa_cd]

    #Check msoa_dest code is not -8, 999999999 or msoa_dest = msoa_cd
    subset_data = subset_data[~subset_data['msoa_dest'].isin(['-8', '999999999', msoa_cd])]
    subset_data = subset_data.sort_values(by='Count', ascending=False)
    if not subset_data.empty:
        highest_route = subset_data.iloc[0]['msoa_dest']
        msoa_pop[msoa_cd] = highest_route


#Step 2, with current dict of MSOA and mos Popular Destination MSOA, find each MSOA passed in direct line path

# Use polygon geojson file for each msoa
polygon_path = 'Datasets/Middle_layer_Super_Output_Areas_December_2021_Boundaries_EW_BGC_V3.geojson'
polygons = {}

with open(polygon_path, 'r') as msoa_file:
    msoa_data = gpd.read_file(msoa_file)
    msoa_data = msoa_data.to_crs(epsg=4326)

def create_msoa_polygons():
    for index, feature in msoa_data.iterrows():
        polygon = feature['geometry']  # Use the geometry directly from the GeoDataFrame
        polygons[feature['MSOA21CD']] = polygon

create_msoa_polygons()

def find_polygons_in_path(start_msoa, end_msoa):
    # Create a line between the centroids of the start and end MSOA polygons
    start_polygon = polygons[start_msoa]
    end_polygon = polygons[end_msoa]
    
    start_centroid = start_polygon.centroid
    end_centroid = end_polygon.centroid
    
    line = LineString([start_centroid, end_centroid])
    
    # Find all polygons that intersect with the line
    intersecting_polygons = []
    for msoa_cd, polygon in polygons.items():
        if polygon.intersects(line):
            intersecting_polygons.append(msoa_cd)
    
    return intersecting_polygons


msoa_route = {}
# Iterate through the msoa_pop dictionary to find polygons for each route
for origin, destination in msoa_pop.items():
    route_polygons = find_polygons_in_path(origin, destination)
    print(f"Route from {origin} to {destination} passes through: {route_polygons}")
    msoa_route[origin] = (route_polygons, destination)


#Step 3, With dict of MSOA and dict containing list of MSOA's passed for most popular route, caluclate aver Mean CQI OR index_space_syntax along that route
results_file = pd.read_csv(f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv", header=0, names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path'])
#msoa_index_scores = dict(zip(results_file['msoa'], results_file['index_space_syntax_length']))

results_dict = results_file.set_index('msoa').T.to_dict()

scaler = MinMaxScaler()
columns_to_scale = ['crash_rate', 'commute_rate', 'index_space_syntax_length']
df = pd.DataFrame.from_dict(results_dict, orient="index")

df[[c + "_norm" for c in columns_to_scale]] = scaler.fit_transform(df[columns_to_scale])
#Get rid of Nans
df[[c + "_norm" for c in columns_to_scale]] = df[[c + "_norm" for c in columns_to_scale]].fillna(0.0)


#TODO Arbitrary wights?
alpha = 0.3
beta = 0.3
gamma = 0.4
msoa_route_score = {}
for msoa, (route_polygons, destination) in msoa_route.items():
    total_score = 0
    for msoa in route_polygons:
        if(msoa in results_dict):
            total_score += alpha * df.loc[msoa, 'crash_rate_norm'] + beta * df.loc[msoa, 'commute_rate_norm'] + gamma * df.loc[msoa, 'index_space_syntax_length_norm']
            # total_score += results_dict[msoa]['index_space_syntax_length']
    # total_score = sum(msoa_index_scores.get(msoa, 0) for msoa in route_polygons)
    #That is the commute_route score.
    msoa_route_score[msoa] = total_score / len(route_polygons) if route_polygons else 0

print(msoa_route_score)
results_file["commute_path"] = results_file["msoa"].map(msoa_route_score).fillna(0).astype(float)
results_file.to_csv(f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv", index=False)
print("Coomute rates score created!")


