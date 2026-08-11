import pandas as pd
import plotly.express as px
from pathlib import Path

#Load the files in different variables first according to the folder chosen
data_dir = Path("data/raw")
processed_dir = Path("data/processed")
processed_dir.mkdir(parents=True, exist_ok=True) # Creates output folder if it doesn't exist


#example with Mungana and RD data
file_names = ['845.csv', '883.csv', '997.csv']
df_list = [pd.read_csv(DATA_DIR / f) for f in file_names]
df_merged = pd.concat(df_list, ignore_index=True)

# Save the merged dataset to be auditable

df_merged.to_csv(processed_dir / "merged_raw.csv", index=False)

# 3. CLEANING AND TRANSFORMING
# Picking elements relevant to Cu mineralisation (Cu, Fe, S) + As (penalty element)
cols = ['Cu_ppm', 'Fe_pct', 'S_pct', 'As_ppm']

# Remove NaNs
df_merged[cols] = df_merged[cols].apply(pd.to_numeric, errors='coerce')
df_clean = df_merged.dropna(subset=cols).copy()

# Convert Cu ppm to percentage as unpractical otherwise
df_clean['Cu_pct'] = df_clean['Cu_ppm'] / 10000

df_clean.drop('Cu_ppm', axis=1, inplace=True)

# Save the cleaned checkpoint
df_clean.to_csv(processed_dir / "merged_cleaned.csv", index=False)

# Picked 1.0 Cu_pct as a typical threshold for economic grade
df_economic = df_clean[df_clean['Cu_pct'] > 1.0]

CuFeS_mineral.to_csv(r"C:\Users\cesar\Documents\Mineral deposits PyTorch and Python\Mungana RD_report\files_unsup\scatter plot\merged_Cu_pct.csv", index=False)
#Picked 1.0 Cu_pct as a typical threshold for economic grade
CuFeS_mineral_filtered = CuFeS_mineral[
    CuFeS_mineral['Cu_pct'] > 1.0
]
"""Setting As limit (in yellow under range_color parameter) to 2000 pppm since it is the level at which is considered safe
thus the mineralised zone with As might present a significant processing risk.
Choosing to display on 4D plot Fe_pct and Cu_pct. with As (penalty) in color
and S content (data point size to identify sulphide vs oxide types)

to identify sulphide mineralisation vs. oxide mineralisation
"""
diagram = px.scatter(
    CuFeS_mineral_filtered,
    x='Fe_pct',
    y='Cu_pct',
    size='S_pct',
    color='As_ppm',
    range_x=[0, 15],
    range_y=[0, 25],
    range_color=[0, 2000],
    color_continuous_scale=px.colors.sequential.Inferno,
    title="Mungana and Red Dome Cu mineralisation. Color = As content (ppm), Size = S content (%)"
)

#Adding the Pyrite Tie line (From Escolme et. al, 2017)
""" USE ONLY WHEN S is x axis, and Fe is y axis,
x0, y0 = 3, 2.5


x1, y1 = 6, 5
slope = (y1 - y0) / (x1 - x0)
intercept = y0 - slope * x0
x_range = [0, 15]
y_extrapolated = [slope * x + intercept for x in x_range]

diagram.add_shape(
    type='line',
    x0=x_range[0], y0=y_extrapolated[0],
    x1=x_range[1], y1=y_extrapolated[1],
    line=dict(color='red', width=1, dash='dash')
)
"""
diagram.show()
