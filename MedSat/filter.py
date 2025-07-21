'''

Sort through medsat data get prescription and census levels for MSOA's. create file london_msoa_medsat_scores.csv

currently just using 2019_spatial_raw_master.csv, can combine with TODO 2020 later?


current vairable are presciription calcs in this order: o_diabetes_quantity_per_capita,o_opioids_quantity_per_capita,o_OME_per_capita,o_total_quantity_per_capita,o_asthma_quantity_per_capita,o_hypertension_quantity_per_capita,o_depression_quantity_per_capita,o_anxiety_quantity_per_capita
'''


import math
import pandas as pd
import os
from statistics import mean
import sys

Region = sys.argv[1]

#Create LSOA to MSOA lookup
msoa_london_path = f"Score Scripts/{Region}Datasets/{Region}MSOA.csv"
lookup_path = "Datasets/LSOAtoMSOAlookup.csv"
medsat_path = "MedSat/point_data/2019_spatial_raw_master.csv"

lookup_cols = ["OA21CD", "LSOA21CD", "LSOA21NM", "LSOA21NMW", "MSOA21CD", "MSOA21NM", "MSOA21NMW", "LAD22CD", "LAD22NM", "LAD22NMW", "ObjectId"]
lookup = pd.read_csv(lookup_path, usecols=range(1, 5), header=0, names=lookup_cols)

lsoa_to_msoa = lookup.set_index("LSOA21CD")["MSOA21CD"]

# #Test, Shouuld give islington 23 MSOACD
# print(lsoa_to_msoa["E01002704"].iloc[0])

msoa_london = pd.read_csv(msoa_london_path)
msoa_london_tuple_lookup = tuple(msoa_london['MSOA21CD'])

medsat = pd.read_csv(medsat_path)
msoa_scores_dict = {}
for index, row in medsat.iterrows():
    lsoa = lsoa_to_msoa[row['geography code']]
    
    if isinstance(lsoa, str):
        msoa = lsoa
    else:
        msoa = lsoa.iloc[0]
    #Skip for non London MSOA's
    if msoa not in msoa_london_tuple_lookup:
        continue
    if msoa not in msoa_scores_dict:
        msoa_scores_dict[msoa] = [{"diabetes": row['o_diabetes_quantity_per_capita'],
                                  "opioids": row['o_diabetes_quantity_per_capita'],
                                  "OME": row['o_OME_per_capita'],
                                  "total": row['o_total_quantity_per_capita'],
                                  "asthma": row['o_asthma_quantity_per_capita'],
                                  "hypertension": row['o_hypertension_quantity_per_capita'],
                                  "depression": row['o_depression_quantity_per_capita'],
                                  "anxiety": row['o_anxiety_quantity_per_capita']}]
    else:
        msoa_scores_dict[msoa].append({"diabetes": row['o_diabetes_quantity_per_capita'],
                                  "opioids": row['o_diabetes_quantity_per_capita'],
                                  "OME": row['o_OME_per_capita'],
                                  "total": row['o_total_quantity_per_capita'],
                                  "asthma": row['o_asthma_quantity_per_capita'],
                                  "hypertension": row['o_hypertension_quantity_per_capita'],
                                  "depression": row['o_depression_quantity_per_capita'],
                                  "anxiety": row['o_anxiety_quantity_per_capita']})
        

#Calcualte average for each msoa
msoa_avg_scores = {}

for msoa, records in msoa_scores_dict.items():
    if not records:
        continue

    keys = records[0].keys()
    avg_dict = {}

    for key in keys:
        # nan values filered out
        values = [
            d[key] for d in records
            if key in d and d[key] is not None and not math.isnan(d[key])
        ]
        avg_dict[key] = mean(values) if values else float('nan')
    msoa_avg_scores[msoa] = avg_dict

output_path = f"MedSat/{Region}/msoa_medsat_scores.csv"
df = pd.DataFrame.from_dict(msoa_avg_scores, orient='index')
df.index.name = 'msoa'
df.reset_index(inplace=True)

df.to_csv(output_path, index=False)

    
    






