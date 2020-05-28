# move 60.931847
import pandas as pd
import numpy as np

print("loading data...")
df = pd.read_csv("/tmp/sz_simple_2800w.csv", delimiter=',', header=0)
df = df.head(1200 * 10000)

dst_longi = []
for i in df.longitude:
	i = i - 60.931847
	dst_longi.append(i)

df_new = pd.DataFrame({'longitude': dst_longi, 'latitude': df.latitude.tolist()})
print(df_new)
df_new.to_csv('/tmp/sz_moved_1200w.csv', index=False)
print("Done")
