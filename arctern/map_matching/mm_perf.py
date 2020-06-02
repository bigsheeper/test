import pandas as pd
nyc_schema={
    "VendorID":"string",
    "tpep_pickup_datetime":"string",
    "tpep_dropoff_datetime":"string",
    "passenger_count":"int64",
    "trip_distance":"double",
    "pickup_longitude":"double",
    "pickup_latitude":"double",
    "dropoff_longitude":"double",
    "dropoff_latitude":"double",
    "fare_amount":"double",
    "tip_amount":"double",
    "total_amount":"double",
    "buildingid_pickup":"int64",
    "buildingid_dropoff":"int64",
    "buildingtext_pickup":"string",
    "buildingtext_dropoff":"string",
}
nyc_df=pd.read_csv("/tmp/0_2M_nyc_taxi_and_building.csv",
               dtype=nyc_schema,
               date_parser=pd.to_datetime,
               parse_dates=["tpep_pickup_datetime","tpep_dropoff_datetime"])

import arctern
import time
nyc_road=pd.read_csv("/tmp/nyc_road.csv", dtype={"roads":"string"}, delimiter='|')
roads=arctern.ST_GeomFromText(nyc_road.roads)
roads = roads.head(90000)

pickup_points = arctern.ST_Point(in_nyc_df.pickup_longitude,in_nyc_df.pickup_latitude)
dropoff_points = arctern.ST_Point(in_nyc_df.dropoff_longitude,in_nyc_df.dropoff_latitude)
is_pickup_near_road = arctern.near_road(roads, pickup_points)
is_dropoff_near_road = arctern.near_road(roads, dropoff_points)
is_resonable = [is_pickup_near_road[idx] & is_dropoff_near_road[idx] for idx in range(0,len(is_dropoff_near_road)) ]
in_nyc_df=in_nyc_df.reset_index()
on_road_nyc_df=in_nyc_df[pd.Series(is_resonable)]

pickup_points = arctern.ST_Point(on_road_nyc_df.pickup_longitude,on_road_nyc_df.pickup_latitude)
projectioned_pickup = arctern.nearest_location_on_road(roads, pickup_points)

dropoff_points = arctern.ST_Point(on_road_nyc_df.dropoff_longitude,on_road_nyc_df.dropoff_latitude)
projectioned_dropoff = arctern.nearest_location_on_road(roads, dropoff_points)

