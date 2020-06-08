def get_perf_data(log):
    times = []
    with open(log,'r') as f:
        for line in f:
            line = [float(i) for i in line.split(",") if i.strip()]
            times.append(line)
    return times

def time_handle(times):
    res_times = []
    length = len(times[0])
    for i in range(length):
        res_time = []
        for time in times:
            res_time.append(time[i])
        res_times.append(res_time)
    return res_times

def print_perf_data(times):
    for time in times:
        for i in time:
            print("{:.2f}".format(i), end ="|")
        print('\n==================================================')

def plot_line_chart(times):
    perf_fig_title = ' Performance Fig (arctern map matching)'
    x_label = 'data amount'
    y_label = 'cost time(s)'
    perf_picture = '/tmp/perf_mm.png'

    import matplotlib.pyplot as plt
    from matplotlib.pyplot import MultipleLocator

    index = list(range(0, len(times[0])))
    ## general x
    # for time in times:
    #     plt.plot(index, time, linewidth=1)

    # Specific x
    plt.plot(index, times[0], label="nearest_location_on_road", color="red", linestyle='--', linewidth=1)
    plt.plot(index, times[1], label="near_road", color="blue", linestyle='-.', linewidth=1)
    plt.plot(index, times[2], label="nearest_road", color="green", linestyle='-', linewidth=1)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(perf_fig_title)
    x_major_locator = MultipleLocator(1)
    y_major_locator = MultipleLocator(10)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)
    ax.set_ylim(ymin=0)
    ax.set_xlim(xmin=0)
    plt.legend()
    # plt.show()
    plt.savefig(perf_picture)
    plt.close('all')

if __name__ == "__main__":
    times = get_perf_data('/tmp/perf_res_mm.txt')
    times = time_handle(times)
    plot_line_chart(times)
