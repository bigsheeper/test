curl --location --request POST 'http://localhost:8080/pointmap' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)"
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
}'
echo "pointmap finished!"
sleep 3

curl --location --request POST 'http://localhost:8080/weighted_pointmap' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)",
        "color_weights": "raw_data.fare_amount",
        "size_weights": "raw_data.total_amount"
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
}'
echo "weighted_pointmap finished!"
sleep 3

curl --location --request POST 'http://localhost:8080/heatmap' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)",
        "weights": "raw_data.fare_amount"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "coordinate_system": "EPSG:4326",
        "map_zoom_level": 10,
        "aggregation_type": "sum"
    }
}'
echo "heatmap finished!"
sleep 3

curl --location --request POST 'http://localhost:8080/choroplethmap' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_data": {
        "region_boundaries": "ST_GeomFromText(raw_data.dropna().buildingtext_pickup)",
        "weights": "raw_data.dropna().fare_amount"
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
}'
echo "choroplethmap finished!"
sleep 3

curl --location --request POST 'http://localhost:8080/icon_viz' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)"
    },
    "params": {
        "width": 1024,
        "height": 896,
        "bounding_box": [-75.37976, 40.191296, -71.714099, 41.897445],
        "icon_path": "/home/sheep/Pictures/taxi.png",
        "coordinate_system": "EPSG:4326"
    }
}'
echo "icon_viz finished!"
sleep 3

curl --location --request POST 'http://localhost:8080/fishnetmap' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_data": {
        "points": "ST_Point(raw_data.pickup_longitude, raw_data.pickup_latitude)",
        "weights": "raw_data.fare_amount"
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
}'
echo "fishnetmap finished!"