from arctern.util import save_png
from arctern.util.vega import vega_fishnetmap
from arctern_pyspark import register_funcs
from arctern_pyspark import fishnetmap
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Python Arrow-in-Spark example").getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

table_df = spark.read.format("csv").option("header", True).option("delimiter", ",").schema("longitude double, latitude double, color_weights double, size_weights double, region_boundaries string").load("file:///tmp/test_data.csv").cache()
table_df.createOrReplaceTempView("test_table")

register_funcs(spark)
    
df = spark.sql("select ST_Point(longitude, latitude) as point, color_weights from test_table where ST_Within(ST_Point(longitude, latitude), ST_GeomFromText('POLYGON ((-74.01424568752932 40.72759334104623, -74.01424568752932 40.76721122683304, -73.96056823889673 40.76721122683304, -73.96056823889673 40.72759334104623, -74.01424568752932 40.72759334104623))'))")
vega = vega_fishnetmap(1824, 1777, bounding_box=[-74.01424568752932, 40.72759334104623, -73.96056823889673, 40.76721122683304], cell_size=8, cell_spacing=1, opacity=1.0, coordinate_system="EPSG:4326")
res = fishnetmap(vega, df)
save_png(res, '/tmp/fishnetmap.png')

spark.sql("show tables").show()
spark.catalog.dropGlobalTempView("test_table")