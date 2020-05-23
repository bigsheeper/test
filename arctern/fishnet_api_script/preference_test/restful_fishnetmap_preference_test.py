import requests
import time

# create scope
payload = {"scope": "fishnetmap_preference_test"}

print("creating scope...")
r = requests.post(url="http://192.168.2.26:8080/scope", json=payload)
print(r.json())

# load data
payload = {\
    "scope": "fishnetmap_preference_test",\
    "tables": [\
        {\
            "name": "szx_vehicles",\
            "format": "csv",\
            "path": "/tmp/out_20181011.csv",\
            "options": {\
                "header": "False",\
                "delimiter": ":"\
            },\
            "schema": [\
                {"car_id": "int"},\
                {"car_type": "string"},\
                {"longitude": "double"},\
                {"latitude": "double"},\
                {"gps_time": "string"},\
                {"gps_speed": "int"},\
                {"direction": "float"},\
                {"event": "int"},\
                {"alarm": "string"},\
                {"gps_longitude": "double"},\
                {"gps_latitude": "double"},\
                {"altitude": "float"},\
                {"car_speed": "float"},\
                {"mileage": "long"},\
                {"error_type": "int"},\
                {"operation_code": "long"},\
                {"system_time": "string"}\
            ]\
        }\
    ]\
}

print("loading data...")
r = requests.post(url="http://192.168.2.26:8080/loadfile", json=payload)
print(r.json())

# draw fishnetmap
payload = {\
    "scope": "fishnetmap_preference_test",\
    "sql": "SELECT ST_Point (longitude, latitude) AS point, gps_speed AS color FROM szx_vehicles where ST_Within(ST_Point(longitude, latitude), ST_GeomFromText('POLYGON ((112.10735 22.093627, 115.386668 22.093627, 115.386668 23.547547, 112.10735 23.547547, 112.10735 22.093627))'))",\
    "params": {\
        "width": 1920,\
        "height": 1080,\
        "bounding_box": [112.10735,22.093627,115.386668,23.547547],\
        "opacity": 1,\
        "coordinate_system": "EPSG:4326",\
        "cell_size": 4,\
        "cell_spacing": 1,\
        "color_gradient": [\
            "#115f9a",\
            "#d0f400"\
        ],\
        "aggregation_type": "sum"\
    }\
}

# payload = {\
#     "scope": "fishnetmap_preference_test",\
#     "sql": "SELECT ST_Point (longitude, latitude) AS point, gps_speed AS color FROM szx_vehicles where ST_Within(ST_Point(longitude, latitude), ST_GeomFromText('POLYGON ((112.10735 22.093627, 115.386668 22.093627, 115.386668 23.547547, 112.10735 23.547547, 112.10735 22.093627))'))",\
#     "params": {\
#         "width": 1920,\
#         "height": 1080,\
#         "bounding_box": [113.728037,22.455366,115.386668,23.547547],\
#         "opacity": 1,\
#         "coordinate_system": "EPSG:4326",\
#         "cell_size": 4,\
#         "cell_spacing": 1,\
#         "color_gradient": [\
#             "#115f9a",\
#             "#d0f400"\
#         ],\
#         "aggregation_type": "sum"\
#     }\
# }

print("running draw fishnetmap...")
start_time = time.time()
r = requests.post(url="http://192.168.2.26:8080/fishnetmap", json=payload)
print(r.json())
print("--- %s seconds ---" % (time.time() - start_time))

import base64
with open("/tmp/restful_szx_vehicles_2800w.png", "wb") as f:
    f.write(base64.b64decode(r.json()['result']))

# result

# 2800w line data
# GPU version: 87.4398
# CPU version: 92.3455
