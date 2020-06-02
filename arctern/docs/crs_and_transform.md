# Arctern 坐标系统

本文档介绍 CRS（Coordinate Reference System，坐标参考系统）和如何使用 Arctern 进行坐标系统转换。

## 坐标参考系统

在 Arctern 的 GeoSeries 中，几何体对象可以是任意空间中的坐标集合。然而在地理空间数据的处理过程中，常常需要知道地球上具体的坐标位置。坐标参考系统就可以表示地球上的坐标信息。

你可以在 <https://spatialreference.org> 中找到最常用的坐标参考系统。

在 Arctern 中，需使用 SRID（Spatial Reference System Identifier，空间参考系统标识符）格式的字符串来表示某个坐标参考系统。例如，最常用的坐标参考系统是经纬度坐标系统和墨卡托投影坐标系统。使用字符串 "EPSG:4326" 来表示经纬度坐标系统，使用字符串 "EPSG:3857" 来表示墨卡托投影坐标系统。

## 坐标系统转换

使用 Arctern 可以将几何体对象在不同的坐标参考系统之间进行转换。在转换之前必须先设置当前几何体对象的坐标参考系统，最后返回坐标转换之后的几何体对象。

以下展示使用 Arctern 将几何体对象由经纬度坐标系统转换到墨卡托投影坐标系统。

### 1. 创建数据集

使用 WKT 表示几何体对象——点、线、多边形，并创建 arctern.GeoSeries 类型的 geos 。

```python
>>> from arctern import GeoSeries
>>> point = 'POINT (-73.993003 40.747594)'
>>> linestring = 'LINESTRING (-73.9594166 40.7593773,-73.9593736 40.7593593)'
>>> polygon = 'POLYGON ((-73.97324 40.73747, -73.96524 40.74507, -73.96118 40.75890, -73.95556 40.77654, -73.97324 40.73747))'
>>> geos = GeoSeries([point, linestring, polygon])
>>> geos
0                         POINT (-73.993003 40.747594)
1    LINESTRING (-73.9594166 40.7593773,-73.9593736...
2    POLYGON ((-73.97324 40.73747,-73.96524 40.7450...
dtype: GeoDtype
```

### 2. 设置坐标系统

使用 arctern.GeoSeries 的 set_crs 接口，设置 geos 当前所属的坐标参考系统。

```python
>>> geos.set_crs("EPSG:4326")
>>> geos.crs
'EPSG:4326'
```

### 3. 坐标转换

使用 arctern.GeoSeries 的 to_crs 接口，将 geos 的经纬度坐标系统转换为墨卡托投影坐标系统（即 "EPSG:3857"）。

```python
>>> geos = geos.to_crs(crs="EPSG:3857")
>>> geos
0           POINT (-8236863.41622516 4975182.82064036)
1    LINESTRING (-8233124.59527958 4976914.39450424...
2    POLYGON ((-8234663.40912862 4973695.32847375,-...
dtype: GeoDtype
```

### 4. 结果验证

使用 arctern.GeoSeries 的 crs 接口，查看 geos 当前所属的坐标系统。

```python
>>> geos.crs
'EPSG:3857'
```

由输出结果可知，geos 的坐标系统已经变成了墨卡托投影坐标系统。
