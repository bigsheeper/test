import pandas as pd
import numpy as np
from osgeo import ogr
import arctern
import time

def write_csv(rows):
	print("writing csv...")
	f = open("/tmp/data.csv", "w")
	for i in range(rows):
		f.write("POINT (20 20);POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))\n")
	f.close()
	print("wrote")

def run_test():
	print("loading data...")
	csv_data_type = {'point':np.object, 'polygon':np.object}
	df = pd.read_csv("/tmp/data.csv", dtype=csv_data_type, delimiter=';', header=None)
	print(df)

	print("start ST_Within...")
	start_time = time.time()
	rst = arctern.ST_Within(arctern.ST_GeomFromText(df[0]), arctern.ST_GeomFromText(df[1]))
	print("--- %s seconds ---" % (time.time() - start_time))
	print(rst)

if __name__ == '__main__':
	# write_csv(10000 * 10000)
	run_test()

# ====================================================================
# loading data...
#                       0                                        1
# 0         POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))
# 1         POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))
# 2         POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))
# 3         POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))
# 4         POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))
# ...                 ...                                      ...
# 99999995  POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))
# 99999996  POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))
# 99999997  POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))
# 99999998  POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))
# 99999999  POINT (20 20)  POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))

# [100000000 rows x 2 columns]
# start ST_Within...
# --- 342.1104509830475 seconds ---
# 0           True
# 1           True
# 2           True
# 3           True
# 4           True
#             ... 
# 99999995    True
# 99999996    True
# 99999997    True
# 99999998    True
# 99999999    True
# Length: 100000000, dtype: bool
# ====================================================================
