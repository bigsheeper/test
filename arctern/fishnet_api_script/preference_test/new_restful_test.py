import requests, json
import time

file_path = "/tmp/out_20181011.csv"
payload = {
    "tables": [
        {
            "name": "raw_data",
            "format": "csv",
            "path": file_path,
            "options": {
                "header": "False",
                "delimiter": ":"
            },
            "schema": [
                {"car_id": "long"},
                {"car_type": "string"},
                {"longitude": "double"},
                {"latitude": "double"},
                {"gps_time": "string"},
                {"gps_speed": "long"},
                {"direction": "float"},
                {"event": "long"},
                {"alarm": "string"},
                {"gps_longitude": "double"},
                {"gps_latitude": "double"},
                {"altitude": "float"},
                {"car_speed": "float"},
                {"mileage": "long"},
                {"error_type": "long"},
                {"operation_code": "long"},
                {"system_time": "string"}
            ]
        }
    ]
}

print("loading data...")
r = requests.post(url="http://127.0.0.1:8080/loadfile", headers={"Content-Type": "application/json"}, data=json.dumps(payload))
print(r.json())

print("creating table...")
r = requests.get(url="http://127.0.0.1:8080/table/schema?table=raw_data")
print(r.json())


# draw fishnetmap
print("running draw fishnetmap...")
url = "http://localhost:8080/fishnetmap"

payload = {
    "input_data": {
        "points": "ST_Point(raw_data[2], raw_data[3])",
        "weights": "raw_data[5]"
    },
    "params": {
            "width": 1920,
            "height": 1080,
            "bounding_box": [112.10735,22.093627,115.386668,23.547547],
            "color_gradient": ["#115f9a", "#d0f400"],
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

start_time = time.time()
response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
print(response.json())
print("--- %s seconds ---" % (time.time() - start_time))

import base64
with open("/tmp/restful_szx_vehicles_2800w.png", "wb") as f:
    f.write(base64.b64decode(response.json()['result']))
print("fishnet finished!")

# result

# 2800w line data
# GPU version: 39
# CPU version: 
