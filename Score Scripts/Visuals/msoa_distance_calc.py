import csv
from math import radians, cos, sin, asin, sqrt
import os

# Define the center of London (latitude and longitude), charing cross
LONDON_LAT = 51.5074
LONDON_LON = -0.1278

#Haversine Function (NOT MINE) From: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


os.chdir(os.path.dirname(os.path.abspath(__file__)))
input_file = "msoa_loc_score.csv"
output_file = "msoa_distances_from_london.csv"

# Read the input file and calculate distances
with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["Distance_from_London_km"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in reader:
        try:
            lat = float(row["Latitude"])
            lon = float(row["Longitude"])
            
            # Calculate the distance from London Center
            distance = haversine(lon, lat, LONDON_LON, LONDON_LAT)
            row["Distance_from_London_km"] = round(distance, 2)
            
            writer.writerow(row)
        except ValueError as e:
            print(f"Error processing row {row}: {e}")

print(f"Distances calculated and saved to {output_file}")