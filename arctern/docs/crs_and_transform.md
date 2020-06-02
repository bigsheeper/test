# Arctern 坐标系统

本文档介绍 CRS（Coordinate Reference System，坐标参考系统）并引导你使用 Arctern 进行坐标系统转换。

## 坐标参考系统

在 Arctern 的 GeoSeries 中，几何体对象可以是任意空间中的坐标集合。然而在地理空间数据的处理过程中，常常需要知道地球上具体的坐标位置。坐标参考系统就可以表示地球上的坐标信息。

你可以在 <https://spatialreference.org> 中找到最常用的坐标参考系统。

在 Arctern 中，需使用 SRID（Spatial Reference System Identifier，空间参考系统标识符）格式的字符串来表示某个坐标参考系统。例如，最常用的坐标参考系统是经纬度坐标系统和墨卡托投影坐标系统。使用字符串 "EPSG:4326" 来表示经纬度坐标系统，使用字符串 "EPSG:3857" 来表示墨卡托投影坐标系统。

## 坐标系统转换

使用 Arctern 可以将每个几何体对象转换为不同的坐标参考系统。在转换之前必须先设置当前的坐标参考系统，最后返回坐标系统转换之后的几何体对象。

## 坐标系统转换示例

以下示例展示使用 Arctern 将纽约市出租车数据由经纬度坐标系统转换到墨卡托投影坐标系统。

### 1. 下载数据

我们需要下载 20 万条纽约出租车数据，默认将其下载至 `/tmp` 下：

```bash
$ cd /tmp
$ wget https://raw.githubusercontent.com/zilliztech/arctern-bootcamp/master/nytaxi/file/0_2M_nyc_taxi_and_building.csv
```

### 2. 数据加载

首先根据纽约出租车数据集中各个字段的名称和数据类型，构建数据的 `nyc_schema` 并导入数据。

```python
>>> import pandas as pd
>>> nyc_schema={
...     "VendorID":"string",
...     "tpep_pickup_datetime":"string",
...     "tpep_dropoff_datetime":"string",
...     "passenger_count":"int64",
...     "trip_distance":"double",
...     "pickup_longitude":"double",
...     "pickup_latitude":"double",
...     "dropoff_longitude":"double",
...     "dropoff_latitude":"double",
...     "fare_amount":"double",
...     "tip_amount":"double",
...     "total_amount":"double",
...     "buildingid_pickup":"int64",
...     "buildingid_dropoff":"int64",
...     "buildingtext_pickup":"string",
...     "buildingtext_dropoff":"string",
... }
>>> nyc_df=pd.read_csv("/tmp/0_2M_nyc_taxi_and_building.csv",
...                dtype=nyc_schema,
...                date_parser=pd.to_datetime,
...                parse_dates=["tpep_pickup_datetime","tpep_dropoff_datetime"])
```

### 3. 创建数据集

使用经纬度坐标（即 "EPSG:4326"），创建表示出租车辆的上车点的数据集 points_series。

```python
>>> import arctern
>>> from arctern import GeoSeries
>>> points = arctern.ST_Point(nyc_df.pickup_longitude,nyc_df.pickup_latitude)
>>> points_series = GeoSeries(points, crs="EPSG:4326")
>>> points_series
0         POINT (-73.993003 40.747594)
1         POINT (-73.959908 40.776353)
2         POINT (-73.955183 40.773459)
3         POINT (-73.985233 40.744682)
4         POINT (-73.997969 40.682816)
                      ...             
199994    POINT (-74.003698 40.732002)
199995     POINT (-73.958217 40.81653)
199996     POINT (-73.98807 40.700618)
199997    POINT (-74.003543 40.723708)
199998      POINT (-74.01205 40.70913)
Length: 199999, dtype: GeoDtype
```

### 4. 坐标转换

使用 arctern.GeoSeries 的 to_crs 接口将 points_series 由原先的经纬度坐标系统转换为墨卡托投影坐标系统（即 "EPSG:3857"）。

```python
>>> points_series = points_series.to_crs(crs="EPSG:3857")
>>> points_series
0         POINT (-8236863.41622516 4975182.82064036)
1         POINT (-8233179.29767736 4979409.53917853)
2         POINT (-8232653.31308336 4978984.12438949)
3          POINT (-8235998.4637817 4974754.94509358)
4         POINT (-8237416.22881644 4965669.06930105)
                             ...                    
199994     POINT (-8238053.9781792 4972892.02404985)
199995    POINT (-8232991.05641843 4985317.42936741)
199996    POINT (-8236314.27717708 4968282.67368993)
199997    POINT (-8238036.72365812 4971673.67768289)
199998     POINT (-8238983.7185663 4969532.61160051)
Length: 199999, dtype: GeoDtype
```

### 5. 结果验证

使用 arctern.GeoSeries 的 crs 接口查看 points_series 的坐标系统。

```python
>>> points_series.crs
'EPSG:3857'
```

由输出结果可知，现在 points_series 的坐标系统已经变成了墨卡托投影坐标系统。
