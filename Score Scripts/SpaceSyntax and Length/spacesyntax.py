"""

applied space syntax weighting to roads, those roads that are more important in network centrality get larger scores applied.


gets score for each wayå
6) CQI Weight By length
7) CQI Mean weighted by space syntax
8) CQI Mean weighted by space syntax and road length


WARNING A BIT LONG TO RUN
"""
import json
import os
import geopandas as gpd
import networkx as nx
import momepy
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import sys

Region = sys.argv[1]

file_dir = f'Datasets/{Region}_cqi_jsons_msoa/'

#Testing before applying to all msoa's
#file_path = '/Users/mattpoole/OwnCodeProjs/THESIS/CyclingQualityIndex/Datasets/output_jsons_msoa/test.json'
#out_file_path = '/Users/mattpoole/OwnCodeProjs/THESIS/CyclingQualityIndex/Datasets/output_jsons_msoa/E02000001.json'


def add_space_syntax(file_path):
    streets_file = gpd.read_file(file_path)

    #Momepy will drop these attributes for some reason without renaming them, change to streets so don't edit rest
    streets = streets_file.rename(columns={"index": "CQI_Score"})
    streets = streets.reset_index().rename(columns={"id": "seg_id"})

    streets = streets.to_crs(epsg=27700)
    streets["length"] = streets.geometry.length  

    G = momepy.gdf_to_nx(                         
            streets,                             
            approach="primal",
            length="length",                        
    )

    #Two weights to be created
    node_bet = nx.betweenness_centrality(
        G, weight="length", normalized=True          # shortest paths weighted by metres
    )
    node_har = nx.harmonic_centrality(
        G, distance="length"                       # harmonic uses same length metric
    )

    nx.set_node_attributes(G, node_bet, "node_bet")
    nx.set_node_attributes(G, node_har, "node_har")


    # Convert node values to edge values, look at u and v and find average value.
    for u, v, k, data in G.edges(keys=True, data=True):
        data["edge_bet_mean"] = (node_bet[u] + node_bet[v]) / 2
        data["edge_har_mean"] = (node_har[u] + node_har[v]) / 2

    edges_gdf = momepy.nx_to_gdf(G, points=False, lines=True)


    # Now to noramlise to compute new score, use min max 0-1
    sc = MinMaxScaler()

    # Don't need to normalise the CQI_Score.
    edges_gdf[["index_n"]]       = edges_gdf[["CQI_Score"]]/100
    # Big question here is ONE, whethere to normalise acorss the whole region, But then need betweenness of whole region.
    edges_gdf[["choice_n"]]      = sc.fit_transform(edges_gdf[["edge_bet_mean"]])
    edges_gdf[["integration_n"]] = sc.fit_transform(edges_gdf[["edge_har_mean"]])

    #Two scores calculated
    alpha, beta, gamma = 0.3, 0.3, 0.4 # TODO Weightings need TUNING 
    edges_gdf["index_space_syntax"] = (
        alpha * edges_gdf.choice_n
        + beta * edges_gdf.integration_n
        + gamma * edges_gdf.index_n
    )

    edges_gdf["index_space_syntax_length"] = edges_gdf['index_space_syntax'] * edges_gdf['length']
    edges_gdf["index_length"] = edges_gdf['CQI_Score'] * edges_gdf['length']
    edges_gdf = edges_gdf.rename(columns={"seg_id": "id"})

    #print(edges_gdf)
    #edges is columns to copy back to streets file

    cols_copy = ['index_space_syntax_length',
                        'index_space_syntax',
                        'index_length',
                        'length']
    
    #Maybe not best solution but very limited duplicates that ruin merge
    edges_gdf    = edges_gdf.drop_duplicates(subset='id', keep='last')
    streets_file = streets_file.drop_duplicates(subset='id', keep='first')

    sf   = streets_file.set_index('id')
    e    = edges_gdf.set_index('id')
    
    # Check if the column 'index_space_syntax' exists in streets_file
    if 'index_space_syntax' in streets_file.columns:
        sf.update(e[cols_copy])
        streets_file = sf.reset_index()
    else:
        edges_gdf = edges_gdf.rename(columns={"seg_id": "id"})
        edges     = edges_gdf[cols_copy + ['id']].copy()
        streets_file = streets_file.merge(edges, on='id', how='left')

    #Save the updated feature back - adding headers, maybe not necessary really
    streets_file = json.loads(streets_file.to_json())
    streets_file["name"] = "cycling_quality_index"
    streets_file["crs"] = {
        "type": "name",
        "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
    }

    with open(file_path, 'w') as geojson_file:
        json.dump(streets_file, geojson_file, indent=4)
        print(f'Updated file with new scores: {file_path}')


for filename in os.listdir(file_dir):
    if filename.endswith('.json'): 
        add_space_syntax(file_dir + filename)

