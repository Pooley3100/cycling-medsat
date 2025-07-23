"""

Takes results in london_msoa_medsat_scores.csv and normalizes each = result_norm

standard scaler should do z scores

output: msoa__medsat_scores_zscaled

not sure this is strictly necessary but does help a lot with visualising

"""


import pandas as pd
from sklearn.preprocessing import StandardScaler
import os
import sys

Region = sys.argv[1]

csv_path = f"MedSat/{Region}/msoa_medsat_scores.csv"
df = pd.read_csv(csv_path)

id_col = "msoa"
numeric_cols = df.columns.difference([id_col])

# Fit the StandardScaler column‑wise
scaler = StandardScaler()
df_z_vals = scaler.fit_transform(df[numeric_cols])

df_z = pd.concat(
    [df[id_col],                       
     pd.DataFrame(df_z_vals,
                  columns=numeric_cols,
                  index=df.index)],
    axis=1
)

df_z.to_csv(f"MedSat/{Region}/msoa_medsat_scores_zscaled.csv", index=False)
print(df_z.head())
