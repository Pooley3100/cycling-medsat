"""

Each json file needs streets_file["name"] = "cycling_quality_index"
    streets_file["crs"] = {
        "type": "name",
        "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
    }
attached

"""
import os
import json
import sys

Region = sys.argv[1]

file_dir = f'Datasets/{Region}_cqi_jsons_msoa/'

header = {
    "type": "FeatureCollection",
    "name": "cycling_quality_index",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    }
}

for filename in os.listdir(file_dir):
    if filename.endswith('.json'): 
        with open(file_dir + filename, "r") as infile:
            data = json.load(infile)

        if "features" not in data:
            raise KeyError("The input JSON file does not contain a 'features' key.")
        
        updated_data = header
        updated_data["features"] = data["features"]

        with open(file_dir + filename, "w") as outfile:
            json.dump(updated_data, outfile, indent=4)

print("headers added")