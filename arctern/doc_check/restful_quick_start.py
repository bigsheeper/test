import requests

# create scope
payload = {"scope": "nyc_taxi"}

r = requests.post(url="http://192.168.2.26:8080/scope", json=payload)
print(r.json())

# load data
payload = {\
    "scope": "nyc_taxi",\
    "tables": [\
        {\
            "name": "raw_data",\
            "format": "csv",\
            "path": "/tmp/0_5M_nyc_taxi_and_building.csv",\
            "options": {\
                "header": "True",\
                "delimiter": ","\
            },\
            "schema": [\
                {"VendorID": "string"},\
                {"tpep_pickup_datetime": "string"},\
                {"tpep_dropoff_datetime": "string"},\
                {"passenger_count": "long"},\
                {"trip_distance": "double"},\
                {"pickup_longitude": "double"},\
                {"pickup_latitude": "double"},\
                {"dropoff_longitude": "double"},\
                {"dropoff_latitude": "double"},\
                {"fare_amount": "double"},\
                {"tip_amount": "double"},\
                {"total_amount": "double"},\
                {"buildingid_pickup": "long"},\
                {"buildingid_dropoff": "long"},\
                {"buildingtext_pickup": "string"},\
                {"buildingtext_dropoff": "string"}\
            ]\
        }\
    ]\
}

r = requests.post(url="http://192.168.2.26:8080/loadfile", json=payload)
print(r.json())


# # draw point map
# payload = {\
#     "scope": "nyc_taxi",\
#     "sql": "select ST_Point(pickup_longitude, pickup_latitude) as point from raw_data where ST_Within(ST_Point(pickup_longitude, pickup_latitude), ST_GeomFromText('POLYGON ((-73.998427 40.730309, -73.954348 40.730309, -73.954348 40.780816 ,-73.998427 40.780816, -73.998427 40.730309))'))",\
#     "params": {\
#          "width": 1024,\
#          "height": 896,\
#         "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],\
#         "coordinate_system": "EPSG:4326",\
#         "point_color": "#2DEF4A",\
#         "point_size": 3,\
#         "opacity": 0.5\
#     }\
# }

# r = requests.post(url="http://192.168.2.26:8080/pointmap", json=payload)
# # print(r.json())
# # 保存为png

# import base64
# with open("/tmp/pointmap.png", "wb") as f:
#     f.write(base64.b64decode(r.json()['result']))



# >>> payload = {\
#     "scope": "scope1",\
#     "session": "spark",\
#     "sql": "SELECT ST_Point (dropoff_longitude, dropoff_latitude) AS point, avg(fare_amount) AS w FROM nyc_taxi GROUP BY point",\
#     "params": {\
#         "width": 512,\
#         "height": 448,\
#         "bounding_box": [\
#             -74.01556543545699,\
#             40.69354738164881,\
#             -73.9434424136598,\
#             40.780921656427836\
#         ],\
#         "coordinate_system": "EPSG:4326",\
#         "map_zoom_level": 10,\
#         "aggregation_type": "sum"\
#     }\
# }



# payload = {\
#     "scope": "nyc_taxi",\
#     "sql": "SELECT ST_Point (pickup_longitude, pickup_latitude) AS point, total_amount AS color FROM raw_data",\
#     "type": "weighted",\
#     "params": {\
#         "width": 512,\
#         "height": 448,\
#         "bounding_box": [\
#             -73.9616334766551,\
#             40.704739019597156,\
#             -73.94232850242967,\
#             40.728133570887906\
#         ],\
#         "opacity": 0.8,\
#         "coordinate_system": "EPSG:4326",\
#         "size_bound": [\
#             10\
#         ],\
#         "color_bound": [\
#             2.5,\
#             20\
#         ],\
#         "color_gradient": [\
#             "#115f9a",\
#             "#d0f400"\
#         ]\
#     }\
# }

# r = requests.post(url="http://192.168.2.26:8080/weighted_pointmap", json=payload)
# print(r.json())
# import base64
# with open("/tmp/weighted_pointmap.png", "wb") as f:
#     f.write(base64.b64decode(r.json()['result']))


# # draw iconviz
# payload = {\
#     "scope": "nyc_taxi",\
#     "sql": "select ST_Point(pickup_longitude, pickup_latitude) as point from raw_data where ST_Within(ST_Point(pickup_longitude, pickup_latitude), ST_GeomFromText('POLYGON ((-73.9616334766551 40.704739019597156, -73.94232850242967 40.704739019597156, -73.94232850242967 40.728133570887906 ,-73.9616334766551 40.728133570887906, -73.9616334766551 40.704739019597156))')) limit 25",\
#     "params": {\
#         "width": 512,\
#         "height": 448,\
#         "bounding_box": [\
#             -73.9616334766551,\
#             40.704739019597156,\
#             -73.94232850242967,\
#             40.728133570887906\
#         ],\
#         "coordinate_system": "EPSG:4326",\
#         "icon_path": "/tmp/output-onlinepngtools.png"\
#     }\
# }

# r = requests.post(url="http://192.168.2.26:8080/icon_viz", json=payload)

# import base64
# with open("/tmp/icon_viz.png", "wb") as f:
#     f.write(base64.b64decode(r.json()['result']))


# draw fishnetmap
payload = {\
    "scope": "nyc_taxi",\
    "sql": "SELECT ST_Point (pickup_longitude, pickup_latitude) AS point, total_amount AS color FROM raw_data where ST_Within(ST_Point(pickup_longitude, pickup_latitude), ST_GeomFromText('POLYGON ((-73.9616334766551 40.704739019597156, -73.94232850242967 40.704739019597156, -73.94232850242967 40.728133570887906 ,-73.9616334766551 40.728133570887906, -73.9616334766551 40.704739019597156))'))",\
    "params": {\
        "width": 512,\
        "height": 448,\
        "bounding_box": [\
            -73.9616334766551,\
            40.704739019597156,\
            -73.94232850242967,\
            40.728133570887906\
        ],\
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

r = requests.post(url="http://192.168.2.26:8080/fishnetmap", json=payload)

import base64
with open("/tmp/fishnetmap.png", "wb") as f:
    f.write(base64.b64decode(r.json()['result']))