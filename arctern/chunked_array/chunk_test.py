from arctern import *
from arctern.util import save_png
from arctern.util.vega import vega_pointmap

import pandas as pd

data = []
wkb = arctern.ST_GeomFromText('POINT (-73.959980 40.776353)')[0]
for i in range(120000000 - 1):
	data.append(wkb)

df = pd.DataFrame({'points': data})
print(df.memory_usage())

pos1=(-73.991504, 40.770759)
pos2=(-73.945155, 40.783434)

vega = vega_pointmap(1024, 384, bounding_box=[pos1[0], pos1[1], pos2[0], pos2[1]], point_size=10, point_color="#2DEF4A", opacity=1, coordinate_system="EPSG:4326")
png = point_map_layer(vega, df.points)
save_png(png, '/tmp/arctern_pointmap_pandas.png')