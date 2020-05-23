/*
 * Copyright (C) 2019-2020 Zilliz. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import org.apache.spark.sql.Row
import org.apache.spark.sql.types._
import org.apache.spark.sql.arctern._

class FunctionsTest extends AdapterTest {

  test("ST_Within preference") {
    println("preference test ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    val conf_array = spark.sparkContext.getConf.getAll
    for( x <- conf_array ){
      println(x)
    }

    val df = spark.read.format("csv")
      .option("sep", ";")
      .option("header", "false")
      .load("/tmp/data.csv")
    df.createOrReplaceTempView("data")
    spark.sql("cache table data")
    df.show(20, 0)

    val t1 = System.currentTimeMillis

    println("start ST_Within...")
    val rst = spark.sql("select count(*) from data where ST_Within(ST_GeomFromText(data._c0), ST_GeomFromText(data._c1))")
    rst.createOrReplaceTempView("rst")
    spark.sql("cache table rst")

    val t2 = System.currentTimeMillis
    println((t2 - t1)/1000.0 + " secs")
    rst.show(20, 0)
    println("preference test done ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
  }

}

// preference test ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// (spark.app.name,arctern scala test)
// (spark.app.id,local-1590057313829)
// (spark.master,local[*])
// (spark.executor.id,driver)
// (spark.driver.host,infini)
// (spark.executor.memory,5g)
// (spark.executor.memoryOverhead,5g)
// (spark.driver.memory,5g)
// (spark.driver.port,38805)
// +-------------+---------------------------------------+
// |_c0          |_c1                                    |
// +-------------+---------------------------------------+
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// |POINT (20 20)|POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))|
// +-------------+---------------------------------------+
// only showing top 20 rows

// start ST_Within...
// 38.373 secs
// +---------+
// |count(1) |
// +---------+
// |100000000|
// +---------+

// preference test done ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
