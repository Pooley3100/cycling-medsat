'''

Take the file ../Datasets/MethodTravelToWork.csv and append percent by bike commute to msoa_scores.csv

'''

import pandas as pd
import os
import sys
Region = sys.argv[1]

commute_path = "Datasets/MethodTravelToWork.csv"
msoa_scores_path = f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv"
msoa_scores = pd.read_csv(f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv", header=0, names=['msoa', 'ScoreCQI', 'crash_rate', 'commute_rate', 'OverallCycleScore', 'ScoreCQIMean', 'index_length', 'index_space_syntax', 'index_space_syntax_length', 'commute_path'])

commute_file = pd.read_csv(commute_path)
commute_file.columns = ["Area", "Total", "Percent_Total", "Bicycle", "Percent_Bicycle"]

commute_file["MSOA"] = commute_file["Area"].str.split(":").str[1].str.strip()


#--->Find duplicated
duplicates = commute_file[commute_file.duplicated(subset="MSOA", keep=False)]

# Output the duplicate MSOA values and their rows
if not duplicates.empty:
    print("Duplicate MSOA values found:")
    print(duplicates[["MSOA", "Area", "Total", "Bicycle", "Percent_Bicycle"]])
else:
    print("No duplicate MSOA values found.")
#---->End of duplicate search

#--->Remove non Region MSOA
ldn_msoa = pd.read_csv(f'Score Scripts/{Region}Datasets/{Region}MSOA.csv')
ldn_msoa_set = set(ldn_msoa["MSOA21CD"])
commute_file = commute_file[commute_file["MSOA"].isin(ldn_msoa_set)]

#---->End of london search


msoa_to_bike_percent = commute_file.set_index("MSOA")["Percent_Bicycle"] 

msoa_scores["commute_rate"] = msoa_scores["msoa"].map(msoa_to_bike_percent).fillna(0).astype(float)

msoa_scores.to_csv(msoa_scores_path, index=False)
print("Commute rates added!")