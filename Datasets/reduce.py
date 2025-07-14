import os
import pandas as pd
import geopandas as gpd
'''

Creates {Region}_cqu_jsons_msoa_REDUCED folder with corresponding geojson files but with a lot of unnecessary data stripped

features kept in each property are just index_10

'''

# First find folders required, then check if {Region}_cqu_jsons_msoa_REDUCED already exists if not create folder

os.chdir(os.path.dirname(__file__))
current_directory = os.getcwd()



cities = pd.read_csv('../Models/city_list.csv',header=0,names=['cities'])

city_way_paths = []
for city in cities['cities']:
    city_way_paths.append(f'{city}_cqi_jsons_msoa')


def create_reduced_folder(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)

    for fname in os.listdir(src_dir):
        if not fname.endswith('.json'):   
            continue

        src_path = os.path.join(src_dir, fname)
        dst_path = os.path.join(dst_dir, fname)

        gdf = gpd.read_file(src_path)        
        reduced = gdf[['geometry', 'index_10']]  # keep only the two columns

        # write a proper GeoJSON FeatureCollection out
        reduced.to_file(dst_path, driver='GeoJSON')



for folder in os.listdir(current_directory):
    if os.path.isdir(folder) and folder in city_way_paths:
        print(f"Processing folder: {folder}")
        new_path = folder + '_REDUCED'
        if not os.path.exists(new_path):
            print(f"Creating reduce folder for {folder}")
            create_reduced_folder(folder, new_path)
        else:
            print(f'{new_path} already exists')