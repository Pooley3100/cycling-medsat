"""

First take the file ../Datasets/LSOAtoMSOAlookup.csv Col 2 to Col5 and in the file ../Datasets/dft-road-casualty-statistics-casualty-2021.csv, whereever col 16 = 1 (casualty type = cycling) using lsoa to msoa lookup

with a dictionary of each msoa as key add 1 to count for each casualty.

then within the file msoa_scores.csv add to it a column 3 (column 1 = msoa, column 2 = cycling scores) with the name crash rate which shows each msoa's number of crashes for the year 2021

"""

import pandas as pd
import sys

Region = sys.argv[1]

lookup_path = "Datasets/LSOAtoMSOAlookup.csv"
cas_path = "Datasets/dft-road-casualty-statistics-casualty-2021.csv"
london_msoa_path = f"Score Scripts/{Region}Datasets/{Region}MSOA.csv"

lookup_cols = ["OA21CD", "LSOA21CD", "LSOA21NM", "LSOA21NMW", "MSOA21CD", "MSOA21NM", "MSOA21NMW", "LAD22CD", "LAD22NM", "LAD22NMW", "ObjectId"]
lookup = pd.read_csv(lookup_path, usecols=range(1, 5), header=0, names=lookup_cols)


lsoa_to_msoa = lookup.set_index("LSOA21CD")["MSOA21CD"]

# print(lsoa_to_msoa["E01035188"])


cas = pd.read_csv(cas_path, low_memory=False)
cycling = cas[cas["casualty_type"] == 1]  # Filter for cycling casualties
cycling_counts = cycling["lsoa_of_casualty"].value_counts()  # Count casualties by LSOA

ldn_msoa = pd.read_csv(london_msoa_path)
ldn_msoa_dict = dict.fromkeys(ldn_msoa["MSOA21CD"])

# Map LSOA counts to MSOA and only add if in london msoa file.
# print(cycling_counts)
for lsoa in cycling_counts.index:
    msoa = lsoa_to_msoa.get(lsoa)
    if msoa is not None and msoa.iloc[0] in ldn_msoa_dict:
        # print(msoa.iloc[0])
        ldn_msoa_dict[msoa.iloc[0]] = (ldn_msoa_dict.get(msoa.iloc[0], 0) or 0) + cycling_counts[lsoa]
    # else:
    #     print(f"no msoa for {lsoa}")


msoa_scores_path = f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv"
msoa_scores_csv = pd.read_csv(f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv", header=0, names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path'])

for row in ldn_msoa_dict.items():
    print(f"MSOA: {row[0]}, Count: {row[1]}")

msoa_scores_csv["crash_rate"] = msoa_scores_csv["msoa"].map(ldn_msoa_dict).fillna(0).astype(int)

#1153 lines before 
msoa_scores_csv.to_csv(msoa_scores_path, index=False)
print("Crash rates score created!")


