import csv
import os
import matplotlib.pyplot as plt

# Input file path
input_file = "msoa_distances_from_london.csv"

# Lists to store data
distances = []
scores = []

# Set the working directory to the current script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Read the CSV file
with open(input_file, "r") as infile:
    reader = csv.DictReader(infile)
    
    for row in reader:
        try:
            # Extract Distance and Score
            distance = float(row["Distance_from_London_km"])
            score = float(row["Score"])
            
            # Append to lists
            distances.append(distance)
            scores.append(score)
        except ValueError as e:
            print(f"Skipping row due to error: {row} - {e}")

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(distances, scores, color="blue", alpha=0.7, edgecolor="k")

# Add labels and title
plt.title("Distance from London vs Score", fontsize=16)
plt.xlabel("Distance from London (km)", fontsize=14)
plt.ylabel("Score", fontsize=14)

# Add grid
plt.grid(True, linestyle="--", alpha=0.6)

# Show the plot
plt.tight_layout()
plt.show()