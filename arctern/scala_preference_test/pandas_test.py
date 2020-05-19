import pandas as pd
import numpy as np
from osgeo import ogr
import arctern
import time

def write_csv(rows):
	print("writing csv...")
	f = open("/tmp/data.csv", "w")
	for i in range(rows):
		f.write("POINT (20 20),POLYGON ((0 0, 40 0, 40 40, 0 40, 0 0))\n")
	f.close()
	print("wrote")

def run_test():
	print("loading data...")
	csv_data_type = {'point':np.object, 'polygon':np.object}
	df = pd.read_csv("/tmp/data.csv", dtype=csv_data_type, delimiter=',', header=None)
	print(df)

	print("start ST_Within...")
	start_time = time.time()
	rst = arctern.ST_Within(arctern.ST_GeomFromText(df[0]), arctern.ST_GeomFromText(df[1]))
	print("--- %s seconds ---" % (time.time() - start_time))
	print(rst)

if __name__ == '__main__':
	write_csv(10000 * 10000)
	# run_test()

# ====================================================================
# loading data...
#                       0              1      2       3      4       5
# 0         POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))
# 1         POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))
# 2         POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))
# 3         POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))
# 4         POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))
# ...                 ...            ...    ...     ...    ...     ...
# 99999995  POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))
# 99999996  POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))
# 99999997  POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))
# 99999998  POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))
# 99999999  POINT (20 20)  POLYGON ((0 0   40 0   40 40   0 40   0 0))

# [100000000 rows x 6 columns]
# --- 68.92285108566284 seconds ---
# 0           False
# 1           False
# 2           False
# 3           False
# 4           False
#             ...  
# 99999995    False
# 99999996    False
# 99999997    False
# 99999998    False
# 99999999    False
# Length: 100000000, dtype: boo
# ====================================================================
