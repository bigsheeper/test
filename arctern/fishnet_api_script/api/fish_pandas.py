import pandas as pd
import numpy as np
import arctern
from arctern.util import save_png
from arctern.util.vega import vega_fishnetmap

# 读取 csv 文件并创建绘图数据
# test_data.csv下载链接: https://github.com/zilliztech/arctern-resources/raw/benchmarks/benchmarks/dataset/layer_rendering_test_data/test_data.csv
csv_data_type = {'longitude':np.float64, 'latitude':np.float64, 'color_weights':np.float64, 'size_weights':np.float64, 'region_boundaries':np.object}
df = pd.read_csv("/tmp/test_data.csv", dtype=csv_data_type, delimiter=',')
print(df)
region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))']))
d=pd.DataFrame(region).T
region = region.append([d]*(df.shape[0] - 1))
in_region = arctern.ST_Within(arctern.ST_Point(df['longitude'], df['latitude']), region[0])
df['in_region']=in_region
input1 = df[df.in_region == True].reset_index()

points = arctern.ST_Point(input1['longitude'], input1['latitude'])

# 根据 input1['color_weights'] 绘制鱼网图
vega = vega_fishnetmap(1824, 1777, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], cell_size=8, cell_spacing=1, opacity=1.0, coordinate_system="EPSG:4326")
png = arctern.fishnet_map_layer(vega, points, input1['color_weights'])
save_png(png, "/tmp/python_fishnet_map.png")