"""

Takes results in msoa_scores.csv and normalizes each = result_norm

standard scaler should do z scores

output: msoa_scores_zscaled

"""


import pandas as pd
from sklearn.preprocessing import StandardScaler
import sys

Region = sys.argv[1]

csv_path = f"Score Scripts/{Region}Datasets/{Region}_msoa_scores.csv"
csv_out_path = f"Score Scripts/{Region}Datasets/{Region}_msoa_scores_zscaled.csv"
df = pd.read_csv(csv_path)

id_col = "msoa"
numeric_cols = df.columns.difference([id_col])

# Fit the StandardScaler column‑wise
scaler = StandardScaler()
df_z_vals = scaler.fit_transform(df[numeric_cols])

df_z = pd.concat(
    [df[id_col],                          # keep IDs intact
     pd.DataFrame(df_z_vals,
                  columns=numeric_cols,
                  index=df.index)],
    axis=1
)

df_z.to_csv(csv_out_path, index=False)
print(df_z.head())
