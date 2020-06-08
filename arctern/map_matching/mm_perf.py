import pandas as pd
import arctern
import time

def delete_file():
    import os
    if os.path.exists("/tmp/perf_res_mm.txt"):
        print("delete file /tmp/perf_res_mm.txt")
        os.remove("/tmp/perf_res_mm.txt")

def load_points():
    nyc_schema = {
        "VendorID":"string",
        "pickup_datetime":"string",
        "dropoff_datetime":"string",
        "passenger_count":"int64",
        "trip_distance":"double",
        "pickup_longitude":"double",
        "pickup_latitude":"double",
        "dropoff_longitude":"double",
        "dropoff_latitude":"double",
        "fare_amount":"double",
        "tip_amount":"double",
        "total_amount":"double",
    }
    nyc_df = pd.read_csv("/tmp/10m_nyc_taxi.csv", dtype=nyc_schema)
    print(nyc_df)
    points = arctern.ST_Point(nyc_df['pickup_longitude|double|data|nullable'],nyc_df['pickup_latitude|double|data|nullable'])
    print(points)
    return points

def load_roads():
    nyc_road = pd.read_csv("/tmp/nyc_road.csv", dtype={"roads":"string"}, delimiter='|')
    roads = arctern.ST_GeomFromText(nyc_road.roads)
    roads = roads.head(90000)
    return roads

def run_nearest_location_on_road(points, roads):
    start_time = time.time()

    projectioned = arctern.nearest_location_on_road(roads, points)

    cost_time = time.time() - start_time
    print("--- %s seconds ---" % cost_time)
    return cost_time

def run_near_road(points, roads):
    start_time = time.time()

    projectioned = arctern.near_road(roads, points)

    cost_time = time.time() - start_time
    print("--- %s seconds ---" % cost_time)
    return cost_time

def run_nearest_road(points, roads):
    start_time = time.time()

    projectioned = arctern.nearest_road(roads, points)

    cost_time = time.time() - start_time
    print("--- %s seconds ---" % cost_time)
    return cost_time

def write_res(t1, t2, t3):
    res_file = open("/tmp/perf_res_mm.txt", "a")
    res_str = str("%s,%s,%s\n" % (t1, t2, t3))
    print(res_str)
    res_file.write(res_str) 
    res_file.close()

if __name__ == "__main__":
    # run
    delete_file()
    points = load_points()
    roads = load_roads()
    for i in range(0, 11):
        print("running, data amount = %d", i)
        t1 = run_nearest_location_on_road(points.head(i * 1000000), roads)
        t2 = run_near_road(points.head(i * 1000000), roads)
        t3 = run_nearest_road(points.head(i * 1000000), roads)
        write_res(t1, t2, t3)
