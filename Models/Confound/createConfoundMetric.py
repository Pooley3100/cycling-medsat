"""

Look for any confounding socioeconmic factors, create an indicy to represent this

options for confounding variables:
c_percent asian,c_percent black,c_percent mixed,c_percent white,c_percent sikh,c_percent hindu,c_percent christian,c_percent jewish,c_percent buddhist,c_percent no religion,c_percent muslim,c_percent no central heating,c_percent wood heating,c_percent communal heating,c_percent TFW less than 2km,c_percent TFW 2km to 5km,c_percent TFW 60km and over,c_percent WFH,c_percent part-time,c_percent 15 hours or less worked,c_percent 49 or more hours worked,c_percent full-time,c_percent commute on foot,c_percent commute metro rail,c_percent commute bus,c_percent commute bicycle,c_percent commute train,c_percent commute car,c_percent same address,c_percent student moved to address,c_percent from within UK moved to address,c_percent outside UK moved to address,c_percent occupancy rating bedrooms +2,c_percent occupancy rating bedrooms 0,c_percent occupancy rating bedrooms +1,c_percent occupancy rating bedrooms -2,c_percent occupancy rating bedrooms -1,c_percent occupancy rating rooms +2,c_percent occupancy rating rooms 0,c_percent occupancy rating rooms +1,c_percent occupancy rating rooms -2,c_percent occupancy rating rooms -1,c_percent 1. Managers directors and senior officials,c_percent 2. Professional occupations,c_percent 3. Associate professional and technical occupations,c_percent 4. Administrative and secretarial occupations,c_percent 5. Skilled trades occupations,c_percent 6. Caring leisure and other service occupations,c_percent 7. Sales and customer service occupations,c_percent 8. Process plant and machine operatives,c_percent 9. Elementary occupations,c_percent born in the UK,c_percent 10 years or more,c_percent 2 years or more but less than 5 years,c_percent 5 years or more but less than 10 years,c_percent less than 2 years,c_pop_density,c_percent Aged 4 years and under,c_percent Aged 5 to 9 years,c_percent Aged 10 to 14 years,c_percent Aged 15 to 19 years,c_percent Aged 20 to 24 years,c_percent Aged 25 to 29 years,c_percent Aged 30 to 34 years,c_percent Aged 35 to 39 years,c_percent Aged 40 to 44 years,c_percent Aged 45 to 49 years,c_percent Aged 50 to 54 years,c_percent Aged 55 to 59 years,c_percent Aged 60 to 64 years,c_percent Aged 65 to 69 years,c_percent Aged 70 to 74 years,c_percent Aged 75 to 79 years,c_percent Aged 80 to 84 years,c_percent Aged 85 years and over,c_total population,c_percent never married and never registered a civil partnership,c_percent married or in a registered civil partnership,c_percent married or in a registered civil partnership married,c_percent married or in a registered civil partnership married opposite sex,c_percent married or in a registered civil partnership married same sex,c_percent married or in a registered civil partnership in a registered civil partnership,c_percent married or in a registered civil partnership in a registered civil partnership opposite sex,c_percent married or in a registered civil partnership in a registered civil partnership same sex,c_percent separated but still legally married or still legally in a civil partnership,c_percent separated but still legally married or still legally in a civil partnership separated but still married,c_percent separated but still legally married or still legally in a civil partnership separated but still in a registered civil partnership,c_percent divorced or civil partnership dissolved,c_percent divorced or civil partnership dissolved divorced,c_percent divorced or civil partnership dissolved formerly in a civil partnership now legally dissolved,c_percent widowed or surviving civil partnership partner,c_percent widowed or surviving civil partnership partner widowed,c_percent widowed or surviving civil partnership partner surviving partner from civil partnership,c_percent unemployed,c_percent very good health,c_percent good health,c_percent fair health,c_percent bad health,c_percent very bad health,c_percent  main language is english ,c_percent   can speak english very well,c_percent   can speak english well,c_percent   cannot speak english well,c_percent   cannot speak english,c_percent households not deprived in any dimension,c_percent households deprived in one dimension,c_percent households deprived in two dimensions,c_percent households deprived in three dimensions,c_percent households deprived in four dimensions,c_percent male,c_net annual income



c_net annual income

for some LSOA's in MedSat data is null, i.e. "c_net annual income": null
"""




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

#Test, Shouuld give islington 23 MSOACD = E02000576
print(lsoa_to_msoa["E01002704"].iloc[0])

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
    #Skip for non {Region} MSOA's
    if msoa not in msoa_london_tuple_lookup:
        continue
    if msoa not in msoa_scores_dict:
        msoa_scores_dict[msoa] = [{"income": row['c_net annual income']}]
    else:
        msoa_scores_dict[msoa].append({"income": row['c_net annual income']})
        

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

output_path = f"Models/Confound/{Region}_msoa_income_scores.csv"
df = pd.DataFrame.from_dict(msoa_avg_scores, orient='index')
df.index.name = 'msoa'
df.reset_index(inplace=True)

df.to_csv(output_path, index=False)

    
    






