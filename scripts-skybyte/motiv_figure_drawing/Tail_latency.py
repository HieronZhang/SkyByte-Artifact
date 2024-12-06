
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import re
import copy
import os, sys
import subprocess
import argparse
import json
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from statsFiguresUtil import *
from figureUtils import *

parser = argparse.ArgumentParser()
# parser.add_argument()
colors = colors_roller_2
colors = colors_custom1
colors = colors_roller_6
plt.rc("font", size=11)
plt.rc("xtick", labelsize=18)
plt.rc("ytick", labelsize=15)
plt.rc("legend", fontsize=18)
plt.rc("hatch", color="white")
mpl.rcParams["axes.labelsize"] = 22
mpl.rcParams["hatch.linewidth"] = 0.5
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams.update({'font.size': 16})
mpl.rcParams.update({'font.family': 'serif'})


output_dir = "../../output/"

workloads = ["bfs-4", "bc-4", "dlrm-4", "fft-4", "radix-4", "ycsb-4", "tpcc-4"]
# workloads = ["ycsb-4", "tpcc-4"]

workload_names = ["bfs-twitter", "bc-twitter", "dlrm-inference", "fft", "radix", "ycsb-nstore", "tpcc-nstore"]
# workload_names = ["ycsb-nstore"]

settings = ["baseType3", "flatflash", "assd-W", "assd-WP", "assd-Full"]
# settings = ["baseType3"]

setting_names = ["BaseType3", "FlatFlash-CXL", "SkyByte-W", "SkyByte-WP", "SkyByte-Full"]


# benchmark_names = ["bfs-Twitter", 'bc-Twitter', 'FFT', 'Radix']
# benchmark_names = ["bfs-v-wm"]
# benchmark_display_names = copy.copy(benchmark_names)
# settings = ["lru", "FlashNeuron", "deepUM", "prefetch_lru"]
# benchmark_dir_translation = {
#     "bfs-Twitter" : 'bfs_twitter_v_RW_sample',
#     'bc-Twitter' : 'bc_twitter_v_RW_sample',
#     'FFT' : 'fft_v_wm_RW_sample',
#     'Radix' : 'radix_v_wm_RW_sample'
# }
# settings = ['256MB','512MB','1GB','2GB']
# with open('PageLocalityCDF_benchmark_spec.json','r') as spec:
#     benchmark_dir_translation = json.load(spec)
# benchmark_names = list(benchmark_dir_translation.keys())
# benchmark_display_names = copy.copy(benchmark_names)


def read_ltc_d(data_dir_path :str):
    # def parse_split(ln:str) -> dict:
    #     ln.strip()
    #     return {
    #         'k' : float(ln.split(':')[0]),
    #         'cnt' : int(ln.split(':')[1])
    #     }
    # def is_numeric(string):
    #     try:
    #         float(string)  # Try converting the string to a float
    #         return True
    #     except ValueError:
    #         return False
    # numeric_part = dram_size_setting[:-2]
    # unit = 2**20 if dram_size_setting[-2:] == 'MB' else 2**30
    # ds = int(numeric_part) * unit
    # is_bench_finished = is_finished(benchName,ds) # whether this benchmark has completed
    # if is_read_amp:
    #     data_dir_path = os.path.join('input_PageLocalityCDF', data_dir_path, f'DRAM={ds}_R_amp.txt')
    # else:
    #     data_dir_path = os.path.join('input_PageLocalityCDF', data_dir_path, f'DRAM={ds}_W_amp.txt')
    # try:
    tmp = []
    with open(data_dir_path,'r') as ltf:
        find = False
        timestamp_arr = []
        cnt_arr = []
        for line in ltf:
            if line.find(':') == -1: continue
            terms = line.split(":")
            if terms[0]=="Latency_CDF_Timestamp":
                find = True
                timestamp_arr = [int(item) for item in terms[1].strip().split(' ')]
                # print(len(timestamp_arr))
            if terms[0]=="Latency_CDF_Data":
                cnt_arr = [int(item) for item in terms[1].strip().split(' ')]
                # print(len(cnt_arr))
        if find:
            for i in range(len(timestamp_arr)):
                dict_i = {
                    'data_range' : timestamp_arr[i],
                    'cnt' : cnt_arr[i]
                }
                tmp.append(dict_i)
    return tmp
    # except:
    #     print(f'no such file {data_dir_path}', file=sys.stderr)




def get_tail_ltc_cdf():

    output_file = f"tail_latency.txt"
    fout = open(output_file, 'w')
    fout.write("BaseType3 | FlatFlash-CXL | SkyByte-W | SkyByte-WP\n\n")   

    for bm_idx, bm_name in enumerate(workload_names):
        
        fout.write(bm_name+"\n")
        for setting in settings:
            
            data_file = output_dir + workloads[bm_idx] + "-" + setting
            # print(f"bm_name: {bm_name}, dram_size: {dram_sz_setting}, translation: {benchmark_dir_translation[bm_name]}, read: {is_read_amp}")
            latency_lst = read_ltc_d(data_file)
            # print(len(latency_lst))
            # print(latency_lst)
            
            sorted_data = []
            for i in range(len(latency_lst)):
                # if len(latency_lst)
                element = latency_lst[i]
                cnt = element['cnt']
                range_base = element['data_range']
                range_upper = range_base
                if i+1 < len(latency_lst):
                    range_upper = latency_lst[i+1]['data_range']
                for j in range(cnt):
                    val = range_base + ((range_upper - range_base) / cnt) * j
                    sorted_data.append(val)
            
            index_999 = (int)(len(sorted_data) * 0.999)
            fout.write(str(sorted_data[index_999])+" ")
        fout.write("\n\n")
        
        # plot_search_trace(lsts, settings, ax, color_list=colors, labels=workload_names, title=f"({chr(ord('a') + bm_idx)}) {workload_names[bm_idx]}", ylabel=ylabel if bm_idx == 0 else "")

    




get_tail_ltc_cdf()
