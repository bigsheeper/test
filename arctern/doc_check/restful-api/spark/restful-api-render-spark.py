import requests
import json

file_path = "/tmp/0_2M_nyc_taxi_and_building.csv"
payload = {
    "tables": [
        {
            "name": "raw_data",
            "format": "csv",
            "path": file_path,
            "options": {
                "header": "True",
                "delimiter": ","
            },
            "schema": [
                {"VendorID": "string"},
                {"tpep_pickup_datetime": "string"},
                {"tpep_dropoff_datetime": "string"},
                {"passenger_count": "long"},
                {"trip_distance": "double"},
                {"pickup_longitude": "double"},
                {"pickup_latitude": "double"},
                {"dropoff_longitude": "double"},
                {"dropoff_latitude": "double"},
                {"fare_amount": "double"},
                {"tip_amount": "double"},
                {"total_amount": "double"},
                {"buildingid_pickup": "long"},
                {"buildingid_dropoff": "long"},
                {"buildingtext_pickup": "string"},
                {"buildingtext_dropoff": "string"}
            ]
        }
    ]
}

r = requests.post(url="http://127.0.0.1:8080/loadfile", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
print(r.json())

r = requests.get(url="http://127.0.0.1:8080/table/schema?table=raw_data")
print(r.json())

#check pointmap
url = "http://localhost:8080/pointmap"
payload = {
    "input_data": {
        "sql": "select ST_Point(pickup_longitude, pickup_latitude) as point from raw_data"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "point_color": "#2DEF4A",
        "point_size": 3,
        "opacity": 0.5
    }
}
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("pointmap finished!")
import time
time.sleep(3)


#weighted pointmap
url = "http://localhost:8080/weighted_pointmap"

payload = {
    "input_data": {
        "sql": "select ST_Point(pickup_longitude, pickup_latitude) as point, fare_amount as count1, total_amount as count2 from raw_data"
    },
    "params": {
            "width": 1024,
            "height": 896,
            "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
            "color_gradient": ["#0000FF", "#FF0000"],
            "color_bound": [0, 2],
            "size_bound": [0, 10],
            "opacity": 1.0,
            "coordinate_system": "EPSG:4326"
    }
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("weighted pointmap finished!")
import time
time.sleep(3)

# heatmap
url = "http://localhost:8080/heatmap"

payload = {
    "input_data": {
        "sql": "select ST_Point(pickup_longitude, pickup_latitude) as point, fare_amount as weights from raw_data"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "map_zoom_level": 10,
        "aggregation_type": "sum"
    }
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("heatmap finished!")
import time
time.sleep(3)

# choroplethmap
url = "http://localhost:8080/choroplethmap"

payload  = {
    "input_data": {
        "sql": "select ST_GeomFromText(buildingtext_pickup) as polygon, fare_amount as count from raw_data where buildingtext_pickup!=''"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "color_gradient": ["#0000FF", "#FF0000"],
        "color_bound": [2.5, 5],
        "opacity": 1,
        "aggregation_type": "mean"
    }
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("choroplethmap finished!")
import time
time.sleep(3)

# iconviz
url = "http://localhost:8080/icon_viz"

payload  = {
    "input_data": {
        "sql": "select ST_Point(pickup_longitude, pickup_latitude) as point from raw_data"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "icon_path": "/home/sheep/Pictures/taxi.png",
        "coordinate_system": "EPSG:4326"
    }
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("iconviz finished!")
import time
time.sleep(3)

# fishnet
url = "http://localhost:8080/fishnetmap"

payload = {
    "input_data": {
        "sql": "select ST_Point(pickup_longitude, pickup_latitude) as point, fare_amount as count from raw_data"
    },
    "params": {
            "width": 1024,
            "height": 896,
            "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
            "color_gradient": ["#0000FF", "#FF0000"],
            "cell_size": 4,
            "cell_spacing": 1,
            "opacity": 1.0,
            "coordinate_system": "EPSG:4326",
            "aggregation_type": "sum"
    }
}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(response.text.encode('utf8'))
print("fishnet finished!")
