import os
import numpy
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

def get_perf_data(log):
    import re
    arr_kepler = []
    arr_arctern_cpu = []
    arr_arctern_gpu = []
    with open(log,'r') as f :
        for line in f :
            line = re.split('[, ]',line.strip())
            assert len(line) == 3
            arr_kepler.append(line[0])
            arr_arctern_cpu.append(line[1])
            arr_arctern_gpu.append(line[2])
    return arr_kepler,arr_arctern_cpu,arr_arctern_gpu

def plot_line_chart2(arr_kepler,arr_arctern_cpu,arr_arctern_gpu):
    perf_picture = plot_dir +'perf.png'
    perf_fig_title = ' Performance Fig (arctern vs kepler)'
    index1 = list(range(1, len(arr_kepler) - 2))
    index2 = list(range(1, len(arr_arctern_cpu) - 2))
    plt.plot(index1, arr_kepler[1:11], label="$kepler$", color="blue", linewidth=1)
    plt.plot(index2, arr_arctern_cpu[1:11], label="$arctern  CPU$", color="red", linestyle='--', linewidth=1)
    plt.plot(index2, arr_arctern_gpu[1:11], label="$arctern  GPU$", color="green", linestyle='-.', linewidth=1)
    plt.xlabel("data amount (million)")  # X label
    plt.ylabel("time (second)")  # Y label
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

def print_form(arr_kepler,arr_arctern_cpu,arr_arctern_gpu):
    for i in arr_kepler:
        print("{:.2f}".format(i), end ="|")
    print('\n==================================================')
    for i in arr_arctern_cpu:
        print("{:.2f}".format(i), end ="|")
    print('\n==================================================')
    for i in arr_arctern_gpu:
        print("{:.2f}".format(i), end ="|")
    print('\n==================================================')

def calculate_mean(arr_kepler,arr_arctern_cpu,arr_arctern_gpu):
    acc_cpu = []
    acc_gpu = []
    for i in range(1, 11):
        print(i)
        acc_cpu.append((arr_kepler[i]) / arr_arctern_cpu[i])
        acc_gpu.append((arr_kepler[i]) / arr_arctern_gpu[i])
    print(acc_cpu)
    print(acc_gpu)
    print("cpu accelerate: %f", sum(acc_cpu) / len(acc_cpu))
    print("gpu accelerate: %f", sum(acc_gpu) / len(acc_gpu))

log_file = 'results.txt'
plot_dir = '/tmp/'
# main invocation
if __name__ == "__main__":
     arr_kepler,arr_arctern_cpu,arr_arctern_gpu = get_perf_data(log_file)
     # calculate_mean(list(map(float,arr_kepler)),list(map(float,arr_arctern_cpu)),list(map(float,arr_arctern_gpu)))
     # print_form(list(map(float,arr_kepler)),list(map(float,arr_arctern_cpu)),list(map(float,arr_arctern_gpu)))
     plot_line_chart2(list(map(float,arr_kepler)),list(map(float,arr_arctern_cpu)),list(map(float,arr_arctern_gpu)))
