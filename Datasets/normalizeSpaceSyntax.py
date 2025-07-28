"""

Add new normalised space syntax length score with StandardScaler for each Region

"""
import os
import geopandas as gpd
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
scaler = StandardScaler()


Region = os.sys.argv[1]

# os.chdir(os.path.dirname(__file__))
# current_directory = os.getcwd()

# cities = pd.read_csv('../Models/city_list.csv',header=0,names=['cities'])

city_way_paths = []
city_way_paths.append(f'Datasets/{Region}_cqi_jsons_msoa')

for city in city_way_paths:
    for filename in os.listdir(city+'/'):
        filepath = os.path.join(city, filename)
        if filename.endswith('.json'): 
            gdf = gpd.read_file(filepath)   
            values = gdf[['index_space_syntax_length']].values

            scaler = StandardScaler()
            normalised = scaler.fit_transform(values)
            gdf['index_space_syntax_length_norm'] = normalised
            gdf_json = gdf.to_file(filepath, driver='GeoJSON')
        
            print(f"Normalised way markers for file:'{filepath}'")


            
