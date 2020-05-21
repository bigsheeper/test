# Copyright (C) 2019-2020 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyspark.sql import SparkSession
from arctern_pyspark import register_funcs
import time

def run_st_within(spark):
    print("loading data...")
    df = spark.read.format("csv").option("header", False).option("delimiter", ";").load("file:///tmp/data.csv")
    df.createOrReplaceTempView("data")
    spark.sql("cache table data")
    df.show(20, 0)

    print("start ST_Within...")
    start_time = time.time()
    rs = spark.sql("select count(*) from data where ST_Within(ST_GeomFromText(data._c0), ST_GeomFromText(data._c1))")
    rs.show()
    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == "__main__":
    spark_session = SparkSession \
        .builder \
        .appName("Python Arrow-in-Spark example") \
        .getOrCreate()

    spark_session.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    print(spark_session.sparkContext._conf.getAll())

    register_funcs(spark_session)

    run_st_within(spark_session)

    print("\033[1;32;40mAll tests of arctern have passed!\033[0m")

    spark_session.stop()

# [('spark.app.name', 'Python Arrow-in-Spark example'), ('spark.executorEnv.GDAL_DATA', '/home/sheep/miniconda3/envs/arctern_env/share/gdal'), ('spark.executor.id', 'driver'), ('spark.driver.host', 'infini'), ('spark.executor.memory', '5g'), ('spark.driver.memory', '5g'), ('spark.executorEnv.PROJ_LIB', '/home/sheep/miniconda3/envs/arctern_env/share/proj'), ('spark.rdd.compress', 'True'), ('spark.driver.port', '45507'), ('spark.serializer.objectStreamReset', '100'), ('spark.master', 'local[*]'), ('spark.submit.pyFiles', ''), ('spark.submit.deployMode', 'client'), ('spark.app.id', 'local-1590057798283'), ('spark.executor.memoryOverhead', '5g')]
# loading data...
# +-------------+---------------------------------------+
# |_c0          |_c1                                    |
# +-------------+---------------------------------------+
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
# +-------------+---------------------------------------+
# only showing top 20 rows

# start ST_Within...
# +---------+
# | count(1)|
# +---------+
# |100000000|
# +---------+

# --- 103.06758499145508 seconds ---
# All tests of arctern have passed!
