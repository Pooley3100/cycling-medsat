import csv
import os
import matplotlib.pyplot as plt

# Input file path
input_file = "msoa_distances_from_london.csv"

distances = []
scores = []

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open(input_file, "r") as infile:
    reader = csv.DictReader(infile)
    
    for row in reader:
        try:
            distance = float(row["Distance_from_London_km"])
            score = float(row["Score"])
            distances.append(distance)
            scores.append(score)
        except ValueError as e:
            print(f"Skipping row due to error: {row} - {e}")

# Plot the data
plt.figure(figsize=(12, 6))
plt.scatter(distances, scores, color="blue", alpha=0.6)


plt.title("Distance from London vs Score")
plt.xlabel("Distance from London (km)")
plt.ylabel("Score")

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()
plt.show()