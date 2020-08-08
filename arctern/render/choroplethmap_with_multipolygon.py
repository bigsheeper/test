import pandas as pd
import arctern
import random
import timeit

from arctern.util import save_png
from arctern.util.vega import vega_choroplethmap

count_data = []

wkt_df_muitipolygon = pd.read_csv('/home/sheep/csv/nyc_elections_districts.csv')
wkt_df_polygon = pd.read_csv('/home/sheep/csv/0_2M_nyc_taxi_and_building.csv')

wkt_series_muitipolygon = wkt_df_muitipolygon['the_geom']
wkt_series_polygon = wkt_df_polygon['buildingtext_dropoff']

for i in range(len(wkt_series_muitipolygon) + len(wkt_series_polygon)):
  count_data.append(random.randint(5, 50))

wkt_series = wkt_series_muitipolygon.append(wkt_series_polygon.dropna())
print(wkt_series)
arr_wkb = arctern.ST_GeomFromText(wkt_series)
arr_count = pd.Series(count_data)

# ["#0000ff", "#34baeb"]
start = timeit.default_timer()

vega = vega_choroplethmap(1920 * 2, 1080 * 2, bounding_box=[-74.416489, 40.445226, -73.381641, 40.949324], color_gradient=["#0000ff", "#ff0000"], color_bound=[5, 50], opacity=1.0, coordinate_system='EPSG:4326')
choropleth_map1 = arctern.choropleth_map_layer(vega, arr_wkb, arr_count)

stop = timeit.default_timer()
print('Time: ', stop - start)  

save_png(choropleth_map1, "/tmp/test_choropleth_map1.png")