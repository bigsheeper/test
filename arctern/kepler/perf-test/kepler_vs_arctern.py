def get_perf_data(log):
    import re
    arr_kepler = []
    arr_arctern = []
    with open(log,'r') as f :
        for line in f :
            line = re.split('[, ]',line.strip())
            assert len(line) == 2
            arr_kepler.append(line[0])
            arr_arctern.append(line[1])
    return arr_kepler,arr_arctern


def plot_line_chart(arr_kepler,arr_arctern):
    for k in arr_kepler:
        print("{:.2f}".format(k))
    print("=========================================================")
    for a in arr_arctern:
        print("{:.2f}".format(a))

    import matplotlib.pyplot as plt
    from matplotlib.pyplot import MultipleLocator
    perf_picture = '/tmp/perf.png'
    perf_fig_title = ' Performance Fig (arctern vs kepler)'
    index1 = list(range(1, len(arr_kepler) + 1))
    index2 = list(range(1, len(arr_arctern) + 1))
    plt.plot(index1, arr_kepler, label="$kepler$", color="blue", linewidth=1)
    plt.plot(index2, arr_arctern, label="$arctern$", color="red", linestyle='--', linewidth=1)
    plt.xlabel("data amount")  # X label
    plt.ylabel("Cost /s")  # Y label
    plt.title(perf_fig_title)
    x_major_locator = MultipleLocator(1)
    y_major_locator = MultipleLocator(10)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    plt.xlim(0, len(arr_kepler) + 2)
    plt.legend()
    # plt.show()
    plt.savefig(perf_picture)
    plt.close('all')


def delete_file():
    print("delete file /tmp/vs_result.txt")
    import os
    if os.path.exists("/tmp/vs_result.txt"):
        os.remove("/tmp/vs_result.txt")


def data_handler():
    import pandas as pd
    import numpy as np

    print("loading data...")
    csv_data_type = {'car_id':np.float64, 'car_type':np.object, 'longitude':np.float64, 'latitude':np.float64, 'gps_time':np.object, 'gps_speed':np.float64, 'direction':np.float64, 'event':np.float64, 'alarm':np.object, 'gps_longitude':np.float64, 'gps_latitude':np.float64, 'altitude':np.float64, 'car_speed':np.float64, 'mileage':np.float64, 'error_type':np.float64, 'operation_code':np.float64, 'system_time':np.object}
    df = pd.read_csv("/tmp/sz_2800w.csv", dtype=csv_data_type, delimiter=':', header=None)
    print(df)

    print("create new csv")
    long = df[2]
    lati = df[3]
    new_df = pd.DataFrame({"longitude":long, "latitude":lati})
    new_df.to_csv('/tmp/sz_simple_2800w.csv', index=False)
    print("Done")


def load_data(num_rows):
    import pandas as pd
    import numpy as np

    print("loading data, num rows = %d" % num_rows)
    df = pd.read_csv("/tmp/sz_simple_2800w.csv", delimiter=',', header=0)
    df = df.head(num_rows)
    return df


def run_kepler(df, num_rows):
    from keplergl import KeplerGl
    import time
    print("kepler start drawing, num rows = %d" % num_rows)
    
    start_time = time.time()
    map_1 = KeplerGl(height=400, data={"data_1": df})
    cost_time = time.time() - start_time
    # map_1.save_to_html(file_name='/tmp/map_%s.html' % num_rows)
    print("--- %s seconds ---" % cost_time)
    return cost_time


def run_arctern(df, num_rows):
    import time
    from arctern import point_map_layer, ST_Point
    from arctern.util import save_png
    from arctern.util.vega import vega_pointmap

    import sys, os
    os.environ["GDAL_DATA"] = sys.prefix + "/share/gdal"
    os.environ["PROJ_LIB"] = sys.prefix + "/share/proj"

    vega = vega_pointmap(600, 400, bounding_box=[112.10735,22.093627,115.386668,23.547547], point_size=3, point_color="#2DEF4A", opacity=1, coordinate_system="EPSG:4326")
    
    print("arctern start drawing, num rows = %d" % num_rows)

    start_time = time.time()
    png = point_map_layer(vega, ST_Point(df.longitude, df.latitude))
    cost_time = time.time() - start_time
    print("--- %s seconds ---" % cost_time)
    save_png(png, '/tmp/arctern_pointmap_pandas.png')
    return cost_time


def run_test(num_rows):
    df = load_data(num_rows)
    kepler_time = run_kepler(df, num_rows)
    arctern_time = run_arctern(df, num_rows)
    res_file = open("/tmp/vs_result.txt", "a")
    res_str = str("%s,%s\n" % (kepler_time, arctern_time))
    print(res_str)
    res_file.write(res_str) 
    res_file.close()


if __name__ == "__main__":
    ## run
    delete_file()
    for i in range(1, 29):
        run_test(i * 1000000)

    # plot
    # log_file = '/tmp/vs_result.txt'
    # arr_kepler,arr_arctern = get_perf_data(log_file)
    # plot_line_chart(list(map(float,arr_kepler)),list(map(float,arr_arctern)))
