import csv
import math
import os

# Define the center of London (latitude and longitude)
LONDON_LAT = 51.5074
LONDON_LON = -0.1278

# Function to calculate the Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371  # Radius of Earth in kilometers
    return R * c


# Set the working directory to the current script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Input and output file paths
input_file = "msoa_loc_score.csv"
output_file = "msoa_distances_from_london.csv"

# Read the input file and calculate distances
with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["Distance_from_London_km"]  # Add a new column for distance
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write the header to the output file
    writer.writeheader()
    
    # Process each row
    for row in reader:
        try:
            # Extract latitude and longitude
            lat = float(row["Latitude"])
            lon = float(row["Longitude"])
            
            # Calculate the distance from London
            distance = haversine(lat, lon, LONDON_LAT, LONDON_LON)
            
            # Add the distance to the row
            row["Distance_from_London_km"] = round(distance, 2)  # Round to 2 decimal places
            
            # Write the updated row to the output file
            writer.writerow(row)
        except ValueError as e:
            print(f"Error processing row {row}: {e}")

print(f"Distances calculated and saved to {output_file}")