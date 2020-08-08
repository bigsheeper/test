import pandas as pd
import arctern
import random
import timeit

from arctern.util import save_png
from arctern.util.vega import vega_unique_value_choroplethmap

count_data = []

wkt_df_muitipolygon = pd.read_csv('/home/sheep/csv/nyc_elections_districts.csv')
wkt_df_polygon = pd.read_csv('/home/sheep/csv/0_2M_nyc_taxi_and_building.csv')

wkt_series_muitipolygon = wkt_df_muitipolygon['the_geom']
wkt_series_polygon = wkt_df_polygon['buildingtext_dropoff']

for i in range(len(wkt_series_muitipolygon) + len(wkt_series_polygon)):
  count_data.append(random.randint(0, 6))

wkt_series = wkt_series_muitipolygon.append(wkt_series_polygon.dropna())
arr_wkb = arctern.ST_GeomFromText(wkt_series)
arr_count = pd.Series(count_data)

start = timeit.default_timer()

unique_value_infos = {
		0: "#32a836",
        1: "#FF0000",
        2: "#00FF00",
        3: "#0000FF",
        4: "#a8328b",
        5: "#a85932"
    }
vega = vega_unique_value_choroplethmap(1920 * 2, 1080 * 2, bounding_box=[-74.416489, 40.445226, -73.381641, 40.949324], unique_value_infos=unique_value_infos, opacity=1.0, coordinate_system="EPSG:4326")
map1 = arctern.unique_value_choropleth_map_layer(vega, arr_wkb, arr_count)

stop = timeit.default_timer()
print('Time: ', stop - start)  

save_png(map1, "/tmp/test_unique_value_choropleth_map1.png")