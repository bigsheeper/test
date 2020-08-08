import pandas as pd
import numpy as np
import random
import arctern
import matplotlib.pyplot as plt

df = pd.read_csv(filepath_or_buffer="test_data.csv", dtype={'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object})
input = df[pd.notna(df['region_boundaries'])].groupby(['region_boundaries']).mean().reset_index()
polygon = arctern.GeoSeries(input['region_boundaries'])

value_data = []
for i in range(len(polygon)):
  value_data.append(random.randint(0, 6))

values = pd.Series(value_data)

fig, ax = plt.subplots(figsize=(10, 6), dpi=200)

unique_value_infos = {1: "#FF0000", 2: "#00FF00", 3: "#0000FF", 4: "#00FFFF", 5: "#FF0000"}
arctern.plot.unique_value_choroplethmap(ax, polygon, values, bounding_box=[-74.01124953254566,40.73413446570038,-73.96238859103838,40.766161712662296], unique_value_infos=unique_value_infos, opacity=1.0, coordinate_system='EPSG:4326')
plt.show()


