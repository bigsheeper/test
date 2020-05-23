import pandas as pd
import arctern

road1 = 'LINESTRING (-73.996324 40.753388, -73.972088 40.743215)'
road2 = 'LINESTRING (-73.989555 40.741531, -73.973952 40.762962)'

# 使用 arctern.ST_Intersection 找到帝国大厦附近的十字路口，即道路 1 与道路 2 相交的位置。
rst = arctern.ST_Intersection(arctern.ST_GeomFromText(road1), arctern.ST_GeomFromText(road2))
empire_state_building = arctern.ST_AsText(rst[0])[0]

d = {'geos': [road1, road2, empire_state_building]}
df = pd.DataFrame(data=d)

# 使用 wget <TODO: add config download url> 下载 kepler 配置文件
# 将 file_path 变量修改为下载的配置文件所在的绝对路径
file_path = </path/to/conf.json>"

from keplergl import KeplerGl
import json
with open(file_path) as f:
    config = json.load(f)

# 使用 keplergl 绘制地图
map_1 = KeplerGl(height=600, data={"data_1": df}, config=config)
map_1
