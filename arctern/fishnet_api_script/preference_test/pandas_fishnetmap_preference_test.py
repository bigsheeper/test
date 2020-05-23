import pandas as pd
import numpy as np
import arctern
import time
from arctern.util import save_png
from arctern.util.vega import vega_fishnetmap

# 读取 csv 文件并创建绘图数据
# test_data.csv下载链接: https://github.com/zilliztech/arctern-resources/raw/benchmarks/benchmarks/dataset/layer_rendering_test_data/test_data.csv
print("loading data...")

csv_data_type = {'car_id':np.float64, 'car_type':np.object, 'longitude':np.float64, 'latitude':np.float64, 'gps_time':np.object, 'gps_speed':np.float64, 'direction':np.float64, 'event':np.float64, 'alarm':np.object, 'gps_longitude':np.float64, 'gps_latitude':np.float64, 'altitude':np.float64, 'car_speed':np.float64, 'mileage':np.float64, 'error_type':np.float64, 'operation_code':np.float64, 'system_time':np.object}

# df = pd.read_csv("/tmp/out_20181011_1w.csv", delimiter=':')
df = pd.read_csv("/tmp/out_20181011.csv", dtype=csv_data_type, delimiter=':', header=None)
print(df)
region = arctern.ST_GeomFromText(pd.Series(['POLYGON ((112.10735 22.093627, 115.386668 22.093627, 115.386668 23.547547, 112.10735 23.547547, 112.10735 22.093627))']))
d=pd.DataFrame(region).T
# region = region.append([d]*(df.shape[0] - 1))

print("data filter...")
start_time = time.time()
in_region = arctern.ST_Within(arctern.ST_Point(df[2], df[3]), region[0])
df['in_region']=in_region
input1 = df[df.in_region == True].reset_index()

points = arctern.ST_Point(input1[2], input1[3])

# 根据 input1['color_weights'] 绘制鱼网图

print("start drawing...")
vega = vega_fishnetmap(1920, 1080, bounding_box=[112.10735,22.093627,115.386668,23.547547], cell_size=4, cell_spacing=1, opacity=1.0, coordinate_system="EPSG:4326")
png = arctern.fishnet_map_layer(vega, points, input1[5])
print("--- %s seconds ---" % (time.time() - start_time))
save_png(png, "/tmp/pandas_szx_vehicles_2800w.png")

# result

# 2800w line data, without data filter
# GPU version: 25.3814
# CPU version: 25.7866

# 2800w line data, with data filter
# GPU version: 97.7880